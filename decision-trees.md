# Decision Trees — "Kalau X → lakuin Y"

> Otak cadangan offline buat final no-AI. Baca gejala soal → ikutin cabang → tiap buntu ada **🔍 search** (boleh pakai Google AI Overview). Teknik detailnya ada di file kategori.

**Legenda:**
`▶` jalankan/aksi · `├─ └─` cabang keputusan · `🔍` search (Google AI Overview) · `🏁` dapet flag · `↪` pindah ke file lain

---

## FIRST 5 MINUTES (semua soal)
```
START
▶ Baca deskripsi + judul + author + hint + tags (clue sering LITERAL)
▶ Lihat yang dikasih:
   ├─ binary + "nc host port" .......... ↪ PWN
   ├─ binary, cari flag di dalamnya .... ↪ REV
   ├─ URL / web app ................... ↪ WEB
   ├─ n,e,c / ciphertext / teks acak .. ↪ CRYPTO
   ├─ file (img/pcap/zip/dump/pdf) .... ↪ FORENSIC
   ├─ foto/username/nama + "cari" ..... ↪ OSINT
   └─ aneh/jail/game/"sanity" ......... ↪ MISC
▶ Flag udah keliatan? (strings, source, deskripsi, Ctrl-F "flag{") → 🏁
```

---

## PWN
```
▶ file ./chall ; checksec ./chall ; nm ./chall | grep -iE 'win|flag|system'
│
├─ Ada fungsi win()/system() di binary?
│   └─ YA → ret2win: overflow (cari offset: cyclic) → p64(win)
│            segfault di movaps? → sisipin p64(ret) dulu      🔍 "ret2win pwntools movaps"
│
├─ Ada printf(input_user)? (format string)
│   └─ YA → cari offset (AAAA.%N$p) → fmtstr_payload write GOT  🔍 "format string %n arbitrary write"
│
├─ Buffer overflow + NX on + gak ada win?
│   ├─ dikasih libc.so.6 → ret2libc: leak puts(puts@got) → system("/bin/sh")  🔍 "ret2libc leak puts pwntools"
│   └─ gak dikasih libc → leak, cari libc dari offset di libc.rip                🔍 "libc database identify offset"
│
├─ checksec: Canary ON? → leak canary dulu (fmtstr/overread), pasang di payload  🔍 "bypass stack canary ctf"
├─ checksec: PIE ON?    → leak alamat kode dulu, set exe.address                 🔍 "bypass PIE leak ctf"
│
├─ Menu malloc/free/edit/show? → HEAP:
│   ├─ bisa pake setelah free → UAF (leak/tulis)                                 🔍 "use after free tcache ctf"
│   ├─ bisa free 2x → double free / tcache poisoning                             🔍 "tcache poisoning glibc 2.31"
│   └─ (cek versi glibc: nentuin mitigasi)
│
├─ seccomp aktif? (seccomp-tools dump) → execve diblok → ORW (open/read/write)   🔍 "seccomp ORW rop ctf"
├─ gadget minim banget + syscall;ret ada → SROP                                  🔍 "srop sigreturn pwntools"
├─ statis / no leak / no system → ret2dlresolve                                  🔍 "ret2dlresolve pwntools"
│
└─ STUCK → baca disassembly main di Ghidra: ada cek konstanta / integer overflow / signedness?  🔍 "integer overflow exploit ctf"
```

---

## REV
```
▶ file ./x ; strings -n6 ./x | grep -i flag ; ./x (jalanin)
│
├─ flag muncul di strings? → (decode kalau ter-encode) → 🏁
├─ "UPX!" di strings? → upx -d ./x → ulang
│
▶ Tentuin tipe (dari `file`):
│   ├─ .NET (PE, "Mono"/".NET") → dnSpy: decompile, set return true, run      🔍 "dnspy patch method"
│   ├─ Java .jar / Android .apk → jadx-gui                                      🔍 "jadx decompile apk"
│   ├─ Python .pyc → decompyle3 ; PyInstaller .exe → pyinstxtractor dulu       🔍 "pyinstaller extract pyc decompile"
│   └─ ELF/PE native (C/C++/Go/Rust) → Ghidra
│
▶ Di Ghidra: cari main → gimana flag dicek?
│   ├─ strcmp/memcmp vs string tetap → flag ada di situ → 🏁
│   ├─ loop XOR/add/sub/transform → tiru/inverse di Python                       🔍 "reverse engineering xor loop python"
│   ├─ cek tiap karakter independen → brute per posisi, atau angr               🔍 "angr simulation manager find avoid"
│   ├─ hash dibandingin → crack (kalau input pendek: brute)                      🔍 "crack hash hashcat mode"
│   └─ interpreter opcode custom (VM) → disassemble handler dulu                 🔍 "ctf custom vm reversing"
│
├─ anti-debug (ptrace/rdtsc)? → patch NOP / LD_PRELOAD stub                       🔍 "bypass ptrace traceme"
└─ STUCK → dynamic di gdb: patch jne→je ke jalur "Correct", dump memori runtime  🔍 "gdb patch instruction jump"
```

---

## WEB
```
▶ Buka + Burp ON ; View Source + baca JS ; curl -sI host
▶ Recon: robots.txt, /.git/HEAD, backup (.bak ~ .swp), /admin, ffuf dir
│   └─ .git kebuka? → git-dumper → baca source                                   🔍 "git-dumper exposed .git"
│
├─ Form login / param id numerik? → SQLi:  ' OR '1'='1'-- -  ; UNION SELECT      🔍 "sql injection union based cheatsheet"
├─ Login pakai JSON? → NoSQLi:  {"user":{"$ne":null},"pass":{"$ne":null}}        🔍 "nosql injection mongodb bypass"
├─ Input kepantul ke HTML? → XSS (curi cookie admin bot)                         🔍 "xss cookie stealer payload"
├─ {{7*7}} → 49 ? → SSTI → RCE                                                   🔍 "ssti jinja2 rce payload"
├─ Param file/page/include? → LFI: ../../etc/passwd ; php://filter baca source   🔍 "lfi to rce php wrapper"
├─ Fitur ping/convert/exec? → Command Injection: ; | && $(...)                   🔍 "command injection filter bypass"
├─ Param url=/fetch? → SSRF: localhost, 169.254.169.254                          🔍 "ssrf cloud metadata bypass"
├─ Upload/parse XML? → XXE: SYSTEM "file:///flag"                                🔍 "xxe file read payload"
├─ Ada JWT / cookie signed? → tamper: alg:none, brute HS256, RS256→HS256         🔍 "jwt attack alg none key confusion"
├─ Akses data by id/uuid? → IDOR (ganti punya orang lain)
├─ Logic token/kuota/harga aneh? → bandingin CREATE vs VERIFY ; mass-assign ; race  🔍 "race condition web exploit burp"
│
└─ STUCK → cek Content-Type (json?), method lain (PUT/DELETE), header X-Forwarded-For/X-Original-URL
```

---

## CRYPTO
```
▶ Identifikasi dari ciri:
│
├─ base64/hex/banyak layer → CyberChef "Magic"                                   🔍 "cyberchef magic recipe"
├─ Ada n, e, c → RSA:
│   ├─ coba dulu: RsaCtfTool --publickey/-n -e --uncipher c                      🔍 "rsactftool usage"
│   ├─ n bisa difaktorin? → factordb.com / sympy.factorint
│   ├─ p,q dekat → Fermat factorization                                          🔍 "fermat factorization rsa"
│   ├─ e kecil (=3) & m^e<n → gmpy2.iroot(c,e)                                    🔍 "rsa small e cube root attack"
│   ├─ n sama, e beda, gcd=1 → common modulus                                    🔍 "rsa common modulus attack"
│   ├─ e sama, banyak c, n beda → Håstad broadcast                               🔍 "hastad broadcast attack"
│   └─ d kecil → Wiener                                                          🔍 "wiener attack rsa"
├─ Diketahui sebagian plaintext → XOR known-plaintext (key=xor(ct,pt))
├─ Output beda tiap run + ada seed → PRNG (LCG recover / MT randcrack)           🔍 "predict mersenne twister randcrack"
├─ Huruf acak sepanjang plaintext → substitusi/vigenere → quipqiup / dcode       🔍 "vigenere cipher solver no key"
├─ AES ECB (blok 16 berulang) → byte-at-a-time / cut-and-paste                   🔍 "ecb byte at a time decryption"
├─ AES CBC → padding oracle / bit-flipping                                        🔍 "padding oracle attack python"
└─ STUCK matematika (lattice/partial) → SageMath LLL / Coppersmith               🔍 "coppersmith small_roots sage"
```

---

## FORENSIC
```
▶ file x ; binwalk x ; strings -n8 x | grep -iE 'flag|ctf' ; exiftool x
│
├─ binwalk nunjuk file nempel? → binwalk -e x / foremost x
├─ ZIP? → unzip (butuh password? zip2john x > h ; john h)                        🔍 "zip2john crack password"
├─ magic bytes salah/ketuker? → fix header pakai xxd/hex editor                   🔍 "file signatures list magic bytes"
│
▶ Tipe file:
│   ├─ GAMBAR (png/jpg/bmp) → STEGO:
│   │   ├─ png/bmp → zsteg -a ; stegsolve (bit plane)                            🔍 "zsteg lsb png ctf"
│   │   ├─ jpg → steghide extract (passphrase? stegseek rockyou)                 🔍 "steghide stegseek brute"
│   │   ├─ exiftool comment ; data setelah IEND/EOF ; pngcheck -v
│   │   └─ cepat: upload ke aperisolve.com
│   ├─ AUDIO (wav/mp3) → spectrogram (Audacity/Sonic), Morse, DTMF              🔍 "audio steganography spectrogram ctf"
│   ├─ PCAP → Wireshark: Statistics>Protocol Hierarchy → Follow Stream / Export Objects  🔍 "wireshark export objects http"
│   │   ├─ USB (HID) → decode keystroke dari usage code                          🔍 "usb keyboard hid pcap decoder"
│   │   ├─ RTP/VoIP → Telephony>RTP>decode audio
│   │   └─ DNS/ICMP payload aneh → data exfil
│   ├─ MEMORY dump → volatility3: windows.pslist/cmdline/filescan/hashdump       🔍 "volatility3 plugins cheatsheet"
│   ├─ DISK image → mmls ; fls -r (file deleted) ; icat                          🔍 "sleuthkit fls icat recover"
│   └─ PDF/OFFICE → pdftotext/pdfimages ; unzip docx ; exiftool
└─ STUCK → polyglot? data setelah EOF? ekstensi bohong? (cek `file` lagi)
```

---

## OSINT
```
▶ exiftool file (GPS? author? comment? timestamp?)
│   └─ ada GPS → Google Maps → 🏁
│
├─ FOTO → reverse image: Google Lens + Yandex + TinEye (crop objek penting dulu)  🔍 "yandex reverse image search"
│   ├─ ada landmark/plang/bahasa → geolocation: Street View, SunCalc, plonkit     🔍 "geoguessr identify location tips"
│   └─ ada orang/wajah → lanjut ke "akun/username"
├─ USERNAME → Sherlock + cek manual (IG/X/GitHub/LinkedIn): bio, post, tag        🔍 "sherlock osint username"
├─ EMAIL → holehe (akun terdaftar), haveibeenpwned (breach)                       🔍 "holehe email osint"
├─ DOMAIN/web → crt.sh (subdomain), Wayback Machine (versi lama), Shodan          🔍 "crt.sh subdomain enumeration"
├─ Clue sastra/film/buku/lagu → cari judul → archive.org / Google Books / Google song  🔍 "identify book from quote"
└─ STUCK → baca ulang deskripsi (clue literal), gabungin 2-3 clue buat konfirmasi
```

---

## MISC
```
├─ "Sanity"/deskripsi panjang → flag di deskripsi/Discord/rules/guidebook (Ctrl-F)
├─ nc service, banyak soal cepat, timeout → script pwntools (decode/eval/convert)  🔍 "pwntools automate nc challenge"
├─ Ada Proof-of-Work di awal (cari suffix hash) → script dulu                      🔍 "ctf proof of work solver sha256"
├─ Python sandbox (pyjail) → escape: ().__class__ chain / __builtins__             🔍 "python jail escape payload"
├─ Bash/restricted shell → ${IFS}, {cat,flag}, vi/awk/find -exec escape            🔍 "rbash escape techniques"
├─ Esolang (brainfuck/whitespace/piet) → interpreter online                        🔍 "brainfuck decoder online"
├─ Encoding aneh / zero-width / braille → CyberChef Magic / unicode steg           🔍 "zero width unicode steganography decode"
└─ Game/puzzle/catur → cek SEMUA tombol/endpoint + baca JS (jawaban sering di 'verifikator', bukan logic utama)
```

---

## Prinsip pakai tree ini
1. **Cocokin gejala** soal ke cabang — jangan nebak teknik dari awal.
2. Tiap cabang = **hipotesis**; kalau dicoba gagal, balik ke cabang lain (jangan ngotot).
3. **🔍 search** cuma buat konsep/sintaks umum (Google AI Overview) — BUKAN minta AI nyari bug / analisis source (dilarang di final).
4. Detail teknik + command lengkap ada di file kategori (`pwn.md`, `web.md`, dst).
5. Max ~45 menit/soal tanpa progress → pindah (lihat `methodology.md`).
```
