# CTF Field Handbook

Cheatsheet pribadi buat dipakai **offline pas lomba** (kompetisi no-AI). Semua ringkas, command-first, gampang di-`Ctrl+F`. Disusun dari pengalaman AgriHack 0x0b + referensi umum.

> ⚠️ **Aturan lomba:** handbook ini isinya catatan & referensi teknik buatan sendiri — boleh dipakai. Yang **dilarang**: minta bantuan AI live, kolaborasi, atau solver otomatis pas lomba. Selalu baca Rules of Engagement tiap kompetisi.

## Daftar isi

| File | Isi |
|------|-----|
| [methodology.md](methodology.md) | Strategi lomba, manajemen waktu, cara baca soal, scoring ⭐ |
| [tools-setup.md](tools-setup.md) | Install & setup semua toolkit + troubleshooting |
| [pwn.md](pwn.md) | Binary exploitation — fmtstr, ROP, ret2libc, heap, shellcode, seccomp ⭐ |
| [rev.md](rev.md) | Reverse engineering — Ghidra, gdb, angr, deobf, patching, anti-debug |
| [web.md](web.md) | Web — SQLi, XSS, SSTI, LFI, RCE, SSRF, XXE, deserialize, JWT, race |
| [crypto.md](crypto.md) | Crypto — RSA, AES, XOR, hash, PRNG, ECC, lattice, encoding |
| [forensic.md](forensic.md) | Forensics — carving, pcap, memory, stego, disk, git |
| [osint.md](osint.md) | OSINT — reverse image, metadata, geolocation, people/username |
| [misc.md](misc.md) | Misc — pyjail, bash jail, esolang, scripting, logic |
| [templates/](templates/) | Exploit siap pakai (pwntools, fmtstr, ret2libc, shellcode, canary, web, crypto) |

## Cara pakai pas lomba
1. **Baca soal → tentuin kategori → buka file kategori.**
2. Tiap file disusun: **triage cepat → teknik per jenis bug → command → gotcha → "checklist kalau stuck".**
3. Mentok? Baca [methodology.md](methodology.md) bagian *"Kalau stuck 20 menit"*.

## Kenali kategori dari gejala
| Gejala soal | Kemungkinan kategori |
|-------------|----------------------|
| Dikasih binary ELF + alamat `nc host port` | **PWN** |
| Dikasih binary tapi disuruh cari flag di dalamnya | **REV** |
| Dikasih URL / web app | **WEB** |
| Dikasih `n,e,c` / ciphertext / teks acak | **CRYPTO** |
| Dikasih file (img/pcap/zip/dump) | **FORENSIC** |
| Dikasih foto/username/nama, "cari di internet" | **OSINT** |
| Aneh / jail / game / "sanity" | **MISC** |

## Flag format
- Biasanya `flag{...}`, atau `<event>{...}` (AgriHack: `agrihack{...}`).
- Submit persis, case-sensitive. Hati-hati trailing space / newline.
- `grep -aoE 'agrihack\{[^}]*\}'` buat nyari di output/file.

## Catatan dari AgriHack 0x0b (penyisihan → final)
- **Kuat:** REV & WEB. Jaga momentum, ini sumber poin stabil.
- **PRIORITAS DRILL:** PWN lanjut. Penyisihan cuma dapet int/baby-bof/toddler-bof; **miss ctrl-hijack-0/1/2 & fmtstr** (total ~1800+ poin). Lihat [pwn.md](pwn.md).
- Mid-tier yang kelewat & gettable: Way Back Then (OSINT 211), Lost in FMIPA (CRYPTO 419), minefields (MISC 419), Kamu Siapa?? (REV 475), dukun-classic/radig (CRYPTO 491).
- **Low-solve = high-value** (dynamic scoring): dulu ulaaaaaaar (500, 1 solve!), CetGipitiPro (491), HamPORTAL (484) ngangkat skor paling banyak. Sisain waktu buat 1-2 soal susah.
