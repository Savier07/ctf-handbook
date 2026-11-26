# REV — Reverse Engineering

> Kekuatan kamu — jaga momentum. Tujuan: paham logika program buat nemu/bikin flag.

## Triage
```bash
file ./chall                 # tipe: ELF/PE/.NET/.pyc/APK? stripped?
strings -n 6 ./chall | less  # flag, kunci, pesan, format string
./chall                      # jalanin, amati behavior
nm ./chall ; readelf -h ./chall
upx -d ./chall               # kalau packed (strings keliatan "UPX!")
```

## Tool per tipe file
| File | Tool |
|------|------|
| ELF / PE (C/C++) | **Ghidra** (decompile), gdb/pwndbg, radare2 |
| .NET (C#) | **dnSpy** / ILSpy (decompile hampir sempurna) |
| Java `.jar` / Android `.apk` | **jadx**, `jadx-gui` |
| Python `.pyc` | **decompyle3** / **uncompyle6** / pycdc |
| Go | Ghidra + `GoReSym`, string recovery susah (stripped) |
| Rust | Ghidra, banyak noise — fokus `main` |
| WASM | `wasm2wat`, `wabt` |

## Workflow Ghidra
1. Import → Analyze (default ok).
2. Cari `main` (atau entry). Baca decompile window.
3. Rename variabel/fungsi biar kebaca (tekan `L`).
4. Cari pembanding flag: `strcmp`, `memcmp`, loop char-by-char, XOR, tabel lookup.
5. Kalau flag dibentuk runtime → tiru logikanya di Python.

## Pola umum
- **String compare langsung** → flag ada di strings / decompile.
- **XOR / transform** → ambil data + kunci, tiru di Python:
  ```python
  enc = bytes.fromhex('....'); key = b'....'
  print(bytes(c ^ key[i%len(key)] for i,c in enumerate(enc)))
  ```
- **Checker per karakter** (cek `input[i]` satu-satu) → brute per posisi, atau pakai **angr**.
- **Anti-debug / ptrace** → patch jump di Ghidra/gdb, atau `LD_PRELOAD` stub.
- **VM/bytecode custom** → pahami opcode handler-nya, tulis disassembler kecil.

## angr (solver simbolik — buat checker rumit)
```python
import angr, claripy
proj = angr.Project('./chall', auto_load_libs=False)
sm = proj.factory.simulation_manager(proj.factory.entry_state())
sm.explore(find=0x401337, avoid=0x401300)   # alamat "Correct" vs "Wrong"
print(sm.found[0].posix.dumps(0))            # input yang bikin flag
```

## gdb cepat (dynamic)
```
b *main+0x40      # breakpoint
r                 # run
x/20xg $rsp       # periksa memori
p $rax            # nilai register
set {int}0x.. = 1 # patch nilai live
```

## Checklist stuck
- [ ] Udah coba `strings`, unpack UPX, cek tipe file bener?
- [ ] Flag dibandingkan sama apa & di mana?
- [ ] Bisa tiru transform-nya di Python?
- [ ] Checker per-char → angr / brute.
- [ ] Patch cek-nya biar jalan ke jalur sukses (dynamic).
