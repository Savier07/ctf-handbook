# REV — Reverse Engineering

> Kekuatan kamu — jaga momentum. Tujuan: paham logika program buat nemu/bikin flag.

## Triage
```bash
file ./chall                 # ELF/PE/.NET/.pyc/APK/Go/Rust? stripped?
strings -n 6 ./chall | less  # flag, kunci, pesan, format string
strings -el ./chall          # string UTF-16 (PE Windows)
./chall                      # jalanin, amati behavior
nm ./chall ; readelf -hsd ./chall
upx -d ./chall               # unpack kalau strings nunjuk "UPX!"
rabin2 -zzqo - ./chall       # (radare) semua string + offset
```
Deteksi packer/obfuscator: entropy tinggi (`binwalk -E`), section aneh, import minim.

## Tool per tipe file
| File | Tool |
|------|------|
| ELF / PE (C/C++) | **Ghidra** (decompile), gdb/pwndbg, radare2/Cutter, IDA |
| .NET (C#) | **dnSpy** / ILSpy — decompile hampir sempurna, bisa edit & jalanin |
| Java `.jar` / Android `.apk` | **jadx-gui**, apktool (resource), bytecode-viewer |
| Python `.pyc` | **decompyle3** / uncompyle6 / **pycdc**; cek versi magic byte |
| PyInstaller `.exe` | `pyinstxtractor.py` → ekstrak `.pyc` → decompile |
| Go | Ghidra + **GoReSym**/`golang_loader_assist`, string recovery |
| Rust | Ghidra, banyak noise — fokus `main`, cari `panic`/string |
| WASM | `wasm2wat`, wabt, Ghidra plugin |
| Native lib (.so/.dll) | Ghidra; cari export yang kepanggil |

## Workflow Ghidra
1. Import → Analyze (default ok). Tunggu selesai.
2. Symbol Tree → cari `main`/`entry`/`WinMain`. Baca Decompiler window (kanan).
3. **Rename** variabel/fungsi (`L`), **retype** (`Ctrl+L`), **comment** (`;`) biar kebaca.
4. Cari pembanding flag: `strcmp`/`memcmp`/`strncmp`, loop char-by-char, XOR, tabel lookup, hash.
5. Flag dibentuk runtime → **tiru logikanya di Python**.
6. Patch: `Ctrl+Shift+G` (patch instruction) / export biner yang udah dipatch.

## Pola umum & solusi
- **String compare langsung** → flag ada di strings/decompile.
- **XOR / transform sederhana**:
  ```python
  enc = bytes.fromhex('....'); key = b'....'
  print(bytes(c ^ key[i%len(key)] for i,c in enumerate(enc)))
  ```
- **Checker per karakter** (cek `input[i]` satu-satu, masing-masing independen) → brute per posisi:
  ```python
  import string, subprocess
  flag=''
  while True:
      for ch in string.printable:
          # jalanin & cek apakah posisi ini bener (timing / output)
          ...
  ```
  atau pakai **angr** (bawah).
- **Transform kompleks** (matematika, state machine) → tiru di Python, atau balik operasinya (inverse).
- **VM / bytecode custom** (interpreter opcode) → pahami tiap handler opcode, tulis disassembler kecil, lalu pahami "program"-nya.
- **Hash check** → kalau input pendek, brute; kalau dibandingin hash → crack.
- **Self-modifying / packed** → dump memori saat runtime (gdb `dump memory`).

## angr (symbolic execution — buat checker rumit)
```python
import angr, claripy
proj = angr.Project('./chall', auto_load_libs=False)
# input simbolik (opsional panjang fix):
# flag = claripy.BVS('flag', 8*20); state = proj.factory.entry_state(stdin=flag)
sm = proj.factory.simulation_manager(proj.factory.entry_state())
sm.explore(find=0x401337, avoid=[0x401300, 0x4012f0])   # addr "Correct" vs "Wrong"
if sm.found:
    print(sm.found[0].posix.dumps(0))   # input ke stdin
```
Tips angr: batasi dengan `avoid`, constraint char printable, hindari fungsi berat (hook `scanf`/`printf`).

## gdb cepat (dynamic)
```
b *main+0x40      breakpoint ; r run ; c continue
x/20xg $rsp       dump memori ; x/8i $rip disasm
p $rax ; p/x $rdi register
set {int}0x.. = 1 patch nilai live (lewatin cek)
```
Patch jump biar selalu ke jalur "Correct": ubah `jne`→`je` / NOP-in cek (di Ghidra atau gdb).

## Anti-debug / anti-analisis
- `ptrace(PTRACE_TRACEME)` → patch jadi NOP, atau `LD_PRELOAD` stub ptrace yang return 0.
- Timing check (`rdtsc`) → patch.
- Cek `/proc/self/status` TracerPid → spoof.
- Junk/opaque predicates → fokus jalur yang beneran kepake.

## .NET / Java shortcut
- dnSpy: buka, cari string flag, set breakpoint, **edit method** jadi `return true`, jalanin.
- jadx: cari `MainActivity`/`checkFlag`, baca logic, tiru di Python.

## Checklist stuck
- [ ] `strings` / unpack UPX / cek tipe file bener?
- [ ] Flag dibandingkan sama apa & di mana (strcmp/loop/hash)?
- [ ] Bisa tiru/inverse transform-nya di Python?
- [ ] Checker per-char → brute / angr.
- [ ] Patch cek-nya biar jalan ke jalur sukses (Ghidra/gdb/dnSpy)?
- [ ] Packed/self-modifying → dump memori runtime.
- [ ] VM custom → disassemble opcode dulu.
