# CRYPTO — Cryptography

> Area yang bisa dikuatin (penyisihan cuma dapet multi-en-decode & kuis; miss Lost in FMIPA, dukun-classic, radig). Tool: **CyberChef offline**, Python `pycryptodome`, `RsaCtfTool`, SageMath, dCode.

## Identifikasi cepat
| Ciri | Kemungkinan |
|------|-------------|
| `A-Za-z0-9+/=` | base64 |
| hex only | `bytes.fromhex` |
| `n`, `e`, `c` gede | RSA |
| angka 0-7 only | octal |
| huruf acak sepanjang plaintext | substitusi / vigenere |
| `.-` titik-garis | Morse |
| banyak layer encode | multi-encode (CyberChef **Magic**) |
| kurva / titik (x,y) + `p,a,b` | ECC |
| output tiap run beda, ada seed | PRNG / LCG |

> **CyberChef "Magic"** = auto-detect layer. Coba duluan buat multi-encode (kayak multi-en-decode).

## Encoding (bukan enkripsi — tinggal dibalik)
```python
import base64, codecs, urllib.parse
base64.b64decode(s); base64.b32decode(s); base64.b85decode(s)
bytes.fromhex(s); s.encode().hex()
codecs.encode(s,'rot_13'); urllib.parse.unquote(s)
# base58 (btc): pip install base58 ; base58.b58decode(s)
```
Base lain: base32/58/62/85/91, ascii85, uuencode, quoted-printable — semua ada di CyberChef.

## Classical cipher (dCode / CyberChef)
- **Caesar/ROT-n**: brute 25 shift.
- **Vigenère**: butuh key (sering di deskripsi; kasus kuis: key `padi`, a=0..z=25). Tanpa key: Kasiski/IC → quipqiup.com.
- **Substitution (monoalphabetic)**: frequency analysis → quipqiup.com.
- **Atbash** (`a<->z`), **Affine** (`ax+b`), **Rail fence**, **Columnar transposition**, **Playfair**, **Bacon** (A/B → biner), **Morse**, **Tap code**, **Polybius**, **Nihilist**.
- Clue tema (angka → huruf): A1Z26, phone keypad (T9), ASCII, book cipher.

## XOR
```python
from pwn import xor
xor(ct, key)                      # pwntools, auto-repeat key
# single-byte brute:
for k in range(256):
    out = bytes(c^k for c in ct)
    if b'flag' in out: print(k, out)
# known-plaintext: key = xor(ct[:len(known)], known)   # mis. known = b'flag{'
# repeating-key (vigenere-XOR): tentuin panjang key via Hamming distance, lalu solve per kolom
```

## RSA ⭐ (paling sering muncul)
```python
from Crypto.Util.number import long_to_bytes, inverse, GCD
# dasar:
phi = (p-1)*(q-1); d = inverse(e, phi); m = pow(c, d, n); print(long_to_bytes(m))
```
**Coba dulu otomatis:** `python3 RsaCtfTool.py --publickey key.pem --uncipher c` atau dengan `-n -e`.
Serangan per kondisi:
| Kondisi | Serangan |
|---------|----------|
| n kecil / factorable | factordb.com, `sympy.factorint(n)`, yafu |
| p, q dekat | **Fermat** factorization |
| e kecil (3) & m kecil | akar: `gmpy2.iroot(c, e)` |
| e kecil, banyak ct & n beda | **Håstad broadcast** (CRT + akar) |
| n sama, e beda, gcd(e1,e2)=1 | **Common modulus** (Bézout) |
| d kecil (d < n^0.25) | **Wiener** attack |
| bocor sebagian p/d | **Coppersmith** (SageMath small_roots) |
| diketahui phi / dp,dq | langsung hitung d / CRT |
| e dan phi tidak coprime | akar modular (AMM / tonelli) |
| modulus multi-prime | factorint semua |
```python
# Fermat (p,q dekat):
import gmpy2
a = gmpy2.isqrt(n)+1
while not gmpy2.is_square(a*a-n): a+=1
b = gmpy2.isqrt(a*a-n); p,q = a+b, a-b
```

## AES / block cipher
- **ECB**: blok identik → ciphertext identik. Deteksi: 16-byte block berulang. Serangan: **ECB byte-at-a-time** (oracle append), cut-and-paste.
- **CBC**: **padding oracle** (decrypt tanpa key, byte per byte dari belakang), **bit-flipping** (ubah plaintext blok via ciphertext blok sebelumnya), IV reuse.
- **CTR/OFB/stream**: keystream reuse (nonce sama) → XOR dua ciphertext.
- **GCM**: nonce reuse → forgery.
```python
from Crypto.Cipher import AES
AES.new(key, AES.MODE_ECB).decrypt(ct)
# padding oracle: pakai padding_oracle_attacker / tulis manual
```

## Hash
- Identify: `hashid <hash>` / dari panjang (MD5=32, SHA1=40, SHA256=64 hex).
- Crack: `hashcat -m 0 hash.txt wordlist` / `john --wordlist=rockyou.txt hash.txt` / crackstation.net.
- **Length extension** (MD5/SHA1 `H(secret||msg)` MAC): `hashpump` / hlextend.
- **Collision**: MD5 chosen-prefix (fastcoll), kadang soal minta 2 input beda hash sama.

## PRNG / randomness
- **LCG** (`x = a*x+c mod m`): recover a,c,m dari beberapa output berurutan (selisih + gcd).
- **Mersenne Twister** (Python `random`): kumpulin 624 output 32-bit → recover state (`randcrack`), prediksi berikutnya.
- Seed lemah (time-based) → brute seed sekitar timestamp.

## ECC / lattice (lanjut — pakai SageMath)
- **ECDSA nonce reuse** (k sama 2 signature) → recover private key.
- **Small subgroup / invalid curve**.
- **Lattice (LLL)**: hidden number problem, knapsack, RSA partial — SageMath `matrix(...).LLL()`.

## Checklist stuck
- [ ] CyberChef **Magic** buat multi-layer encode?
- [ ] RSA → RsaCtfTool + factordb dulu, baru serangan spesifik?
- [ ] XOR single/multi-byte brute / known-plaintext?
- [ ] Key/clue ada di deskripsi/judul?
- [ ] Hash → crack online/wordlist / length extension?
- [ ] Output berubah tiap run → PRNG (LCG/MT)?
- [ ] Mentok matematika → SageMath (lattice/Coppersmith).
