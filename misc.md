# MISC — Miscellaneous

> Campur: pyjail, bash, scripting, logic/game, sanity. Sering butuh otak-atik kreatif + script cepat.

## Sanity / free flag
- Flag ada di deskripsi, Discord, rules, atau `Ctrl+F "flag{"` di guidebook.
- Cek komentar HTML, source, QR code, footer.

## nc service / scripting (jawab cepat & berulang)
Kayak soal kuis: server kasih N pertanyaan, harus dijawab cepat sebelum timeout.
```python
from pwn import *
p = remote('host', port)
import base64, codecs
while True:
    line = p.recvline().decode(errors='ignore')
    # parse soal, hitung jawaban, kirim
    # p.sendline(str(ans).encode())
p.interactive()
```
Pola jawaban: decode (base64/hex/rot), hitung ekspresi (`eval` hati-hati), konversi basis.

## Pyjail (escape Python sandbox)
```python
# kalau builtins diblok, cari jalan lewat:
().__class__.__bases__[0].__subclasses__()        # cari os/subprocess
__import__('os').system('sh')
breakpoint()                                       # kadang lolos → pdb → !import os
# bypass filter kata: getattr, chr(), string concat, \x encoding
print(open('flag.txt').read())
```
- Diblok `import`? → `__builtins__`, `__class__` chain, `lambda`.
- Diblok kurung `()`? → decorator trick, `@exec` dkk.

## Bash / shell jail
- `${IFS}` buat spasi, `cat<flag`, `/???/flag`, glob `*`, `$(...)`.
- Restricted shell (rbash): cari command yg bisa spawn shell (`vi`, `awk`, `find -exec`).

## Esoteric / encoding aneh
- Brainfuck, Whitespace, Ook!, Malbolge → decoder online (dcode).
- QR / barcode: `zbarimg code.png`.
- Emoji/unicode stego: cek zero-width chars (`U+200B`), variation selectors.

## Game / logic (mis. catur, puzzle)
- Kasus "The Last Move": kadang jawaban bukan di main logic, tapi di tombol/endpoint "verifikasi" (cek request yg dikirim).
- Chess: cari checkmate; perhatiin siapa yang di-mate (putih/hitam).
- Cek **semua tombol/aksi** di UI — kadang ada yang kelewat.

## Scripting util cepat
```python
# bruteforce / generate
import itertools, string, hashlib
for c in itertools.product(string.ascii_lowercase, repeat=4): ...
# requests berulang
import requests; requests.post(url, json={...})
```

## Checklist stuck
- [ ] Baca deskripsi literal — flag/clue sering di depan mata.
- [ ] Service berulang → script pwntools.
- [ ] Jail → cari chain bypass (`__class__`, `${IFS}`).
- [ ] Encoding aneh → identify dulu (dcode).
- [ ] UI game → cek semua tombol/endpoint, bukan cuma logic utama.
