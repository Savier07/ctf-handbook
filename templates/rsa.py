#!/usr/bin/env python3
# RSA toolkit ringkas. Isi n,e,c (dan p/q kalau ada). Coba fungsi sesuai kondisi.
from Crypto.Util.number import long_to_bytes, inverse, GCD
import gmpy2

n = 0
e = 65537
c = 0

def decrypt(p, q):
    d = inverse(e, (p-1)*(q-1))
    return long_to_bytes(pow(c, d, n))

def fermat(n):                      # p, q dekat
    a = gmpy2.isqrt(n) + 1
    while not gmpy2.is_square(a*a - n):
        a += 1
    b = gmpy2.isqrt(a*a - n)
    return int(a+b), int(a-b)

def small_e_root():                 # e kecil & m^e < n (tanpa mod wrap)
    m, exact = gmpy2.iroot(c, e)
    return long_to_bytes(int(m)) if exact else None

def common_modulus(c1, c2, e1, e2): # n sama, e beda, gcd(e1,e2)=1
    g, a, b = gmpy2.gcdext(e1, e2)
    if a < 0: c1 = inverse(c1, n); a = -a
    if b < 0: c2 = inverse(c2, n); b = -b
    return long_to_bytes(int((pow(c1, a, n) * pow(c2, b, n)) % n))

if __name__ == '__main__':
    # contoh alur:
    # 1) cek factordb.com / sympy.factorint(n)
    # 2) p,q dekat -> p,q = fermat(n); print(decrypt(p,q))
    # 3) e kecil    -> print(small_e_root())
    # 4) kalau mentok: python3 RsaCtfTool.py -n <n> -e <e> --uncipher <c>
    pass
