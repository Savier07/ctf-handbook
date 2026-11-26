# Templates

Copy ke folder kerja soal, isi bagian config, jalanin. `args.REMOTE` → `python3 x.py REMOTE`.

| File | Buat |
|------|------|
| `exploit.py` | Skeleton pwntools serbaguna (local/remote/gdb, ret2win) |
| `ret2libc.py` | Leak libc (puts) → `system("/bin/sh")` |
| `fmtstr.py` | Format string: cari offset → leak → write GOT |
| `canary_rop.py` | Leak canary → ROP ret2libc |
| `shellcode.py` | Shellcode execve + varian ORW (seccomp) |
| `web_req.py` | requests session: blind SQLi, fuzzing |
| `rsa.py` | RSA: fermat, small-e root, common modulus |

Tips: `context.log_level='debug'` buat liat byte. `gdb.debug()` buat step. Simpan tiap solve jadi `solve_<chall>.py`.
