# CRYPTO — Cryptography

> Area yang bisa dikuatin. Tool andalan: **CyberChef (offline)**, Python `pycryptodome`, `RsaCtfTool`, dCode.

## Identifikasi cepat
| Ciri | Kemungkinan |
|------|-------------|
| Base64 (`A-Za-z0-9+/=`) | base64 → decode |
| Hex | `bytes.fromhex` |
| `n`, `e`, `c` gede | RSA |
| Cuma angka 0-7 | octal |
| Huruf acak panjang = plaintext | substitusi / vigenere |
| `.-` / titik-garis | Morse |
| Banyak layer | multi-encode (pakai CyberChef Magic) |

**CyberChef "Magic"** operation = auto-detect layer encoding. Coba ini duluan buat multi-encode.

## Encoding (bukan enkripsi — tinggal dibalik)
```python
import base64
base64.b64decode(s); bytes.fromhex(s); s.encode().hex()
# ROT13: codecs.encode(s,'rot_13') ; URL: urllib.parse.unquote
```
Base: base32/base58/base85/base91 — CyberChef punya semua.

## Classical cipher (pakai dCode / CyberChef)
- **Caesar/ROT-n**: brute 25 shift.
- **Vigenère**: butuh key (kadang di deskripsi); kasus kuis: key `padi`, a=0.
- **Substitution**: frequency analysis (quipqiup.com).
- **Atbash**: `a<->z`. **Morse**: dCode. **Baconian**, **Rail fence**, **Playfair**.

## XOR
```python
from pwn import xor           # pwntools
xor(ct, key)
# single-byte XOR brute:
for k in range(256):
    out = bytes(c^k for c in ct)
    if b'flag' in out or out.isascii(): print(k, out)
# known-plaintext: key = xor(ct[:len(pt)], pt)
```

## RSA ⭐ (paling sering)
```python
from Crypto.Util.number import long_to_bytes, inverse
# dasar: d = inverse(e, (p-1)*(q-1)); m = pow(c, d, n)
```
Serangan umum (coba `RsaCtfTool --publickey key.pub --uncipher c` dulu):
- **n kecil** → faktorkan: factordb.com, `sympy.factorint(n)`.
- **e kecil (e=3)** & m kecil → akar pangkat-e: `gmpy2.iroot(c, 3)`.
- **p, q dekat** → Fermat factorization.
- **Common modulus** (n sama, e beda) → gcd/bezout.
- **Wiener** (d kecil), **Hastad** (e sama, banyak ct), **partial key**.
- **Multi-prime / known phi** → langsung hitung d.

## AES
- **ECB**: blok sama → ciphertext sama. ECB cut-and-paste, byte-at-a-time oracle.
- **CBC**: **padding oracle** (bisa decrypt tanpa key), bit-flipping.
- Mode keliatan dari pola 16-byte block berulang.

## Hash
- Identify: `hashid <hash>` atau dari panjang (MD5=32hex, SHA1=40, SHA256=64).
- Crack: `hashcat -m 0 hash.txt wordlist` / `john`, atau crackstation.net (online).
- **Length extension** (MD5/SHA1 MAC): `hashpump`.

## Checklist stuck
- [ ] CyberChef Magic buat multi-layer?
- [ ] RSA → RsaCtfTool + factordb?
- [ ] XOR single/multi-byte brute?
- [ ] Key ada di deskripsi/hint?
- [ ] Hash → crack online/wordlist.
