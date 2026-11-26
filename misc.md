# MISC — Miscellaneous

> Campur: pyjail, bash jail, scripting, logic/game, esolang, sanity. Butuh kreatif + script cepat. Penyisihan: cleared Sanity/Cinnamoroll/Last Move/Pompompurin; miss minefields/archive/Simple chall.

## Sanity / free flag
- Flag di deskripsi, Discord, rules/guidebook, QR, footer. `Ctrl+F "flag{"` / `grep -ar 'flag{'`.
- Cek komentar HTML, EXIF, QR code, base64 di mana-mana.

## nc service / scripting cepat (jawab beruntun)
Kasus kuis: server kasih N soal, jawab cepat sebelum timeout → otomatis pakai pwntools.
```python
from pwn import *
import base64, codecs, re
p = remote('host', port)
while True:
    line = p.recvline().decode(errors='ignore').strip()
    log.info(line)
    # parse soal → hitung jawaban → kirim
    if 'base64' in line: ans = base64.b64decode(data).decode()
    elif '+' in line:    ans = str(eval(re.search(r'[\d +\-*/]+', line).group()))
    # ...
    p.sendline(ans.encode())
```
Pola jawaban umum: decode (base64/hex/rot/morse), hitung ekspresi, konversi basis, urutan/deret.

## Pyjail (escape Python sandbox)
```python
# jalan umum kalau builtins diblok:
().__class__.__bases__[0].__subclasses__()          # cari Popen/os._wrap_close
[x for x in ().__class__.__base__.__subclasses__() if 'wrap_close' in str(x)][0]\
  .__init__.__globals__['system']('sh')
__import__('os').system('sh')
breakpoint()                                         # kadang lolos → pdb → import os
# baca flag langsung:
print(open('flag.txt').read())
# builtins recovery:
__builtins__.__import__('os').system('sh')
```
- Diblok `import`? → `__builtins__`, `__class__` chain, `__loader__.load_module`.
- Diblok kurung `()`? → decorator (`@exec`\n`@input`), atau `help()`.
- Diblok titik `.`? → `getattr`, `__getattribute__`, `vars()`.
- Filter kata ('os','system','eval'): `getattr`, `chr()` concat, `"sy"+"stem"`, `\x` escape, unicode.
- Audit hook (3.8+) susah → cari syscall lewat ctypes.

## Bash / shell jail
- `${IFS}` buat spasi, `cat<flag`, `/???/flag`, glob `/f???`, `$(...)`, `` `...` ``.
- Karakter diblok: `${PATH:0:1}`=`/`, `${IFS}`=spasi, brace `{cat,flag}`.
- Restricted shell (rbash): escape lewat `vi`→`:!sh`, `awk 'BEGIN{system("sh")}'`, `find . -exec sh \;`, `python -c`, `less`→`!sh`.
- Env: `export`, `declare` buka var tersembunyi.

## Esoteric / encoding aneh
- **Brainfuck, Whitespace, Ook!, Malbolge, Piet (gambar)** → decoder online (dcode, tio.run).
- **QR / barcode**: `zbarimg code.png`. DataMatrix/Aztec.
- **Zero-width / unicode stego**: cek `U+200B/200C/200D/FEFF`, variation selectors, tag chars → unicode steganography decoder.
- **Emoji cipher**, **Braille**, **semaphore/flag**, **Base65536**.

## Game / logic / puzzle
- Kasus "The Last Move": jawaban bukan di logic utama, tapi di **endpoint/tombol "verifikasi"** — cek request yang dikirim (intercept).
- Chess: cari checkmate; perhatiin **siapa** yang di-mate (putih/hitam), notasi langkah.
- Cek **SEMUA tombol/aksi/endpoint** di UI — sering ada yang kelewat/hidden.
- Game web: baca JS, ubah variable (skor/health) di console, cheat via devtools, intercept API.

## Scripting util cepat
```python
import itertools, string, hashlib, requests
# bruteforce kombinasi
for c in itertools.product(string.ascii_lowercase, repeat=4):
    s=''.join(c); ...
# request berulang / fuzzing
for i in range(1000): requests.get(f'http://host/?id={i}')
# proof-of-work (sering di awal nc): cari suffix biar hash prefix cocok
import itertools, hashlib
pre = b'...'
for n in itertools.count():
    if hashlib.sha256(pre+str(n).encode()).hexdigest().startswith('00000'): print(n); break
```

## Checklist stuck
- [ ] Baca deskripsi literal — flag/clue di depan mata?
- [ ] Service berulang → script pwntools (decode/eval/convert).
- [ ] Jail → cari chain bypass (`__class__`, `${IFS}`, getattr).
- [ ] Encoding aneh → identify dulu (dcode / CyberChef Magic).
- [ ] Game/UI → cek semua tombol/endpoint & JS, bukan cuma logic utama.
- [ ] Ada PoW di awal → script dulu.
