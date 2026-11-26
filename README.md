# CTF Field Handbook

Cheatsheet pribadi buat dipakai **offline pas lomba** (kompetisi no-AI). Semua ringkas, command-first, gampang di-`Ctrl+F`.

> ⚠️ **Aturan lomba:** handbook ini isinya catatan & referensi teknik buatan sendiri — boleh dipakai. Yang **dilarang**: minta bantuan AI live, kolaborasi, atau solver otomatis pas lomba. Pastiin baca Rules of Engagement tiap kompetisi.

## Daftar isi

| File | Isi |
|------|-----|
| [tools-setup.md](tools-setup.md) | Install & setup semua toolkit (jalanin sebelum lomba) |
| [pwn.md](pwn.md) | Binary exploitation — format string, ROP, ret2libc, GOT, canary/PIE ⭐ |
| [rev.md](rev.md) | Reverse engineering — Ghidra, gdb, deobfuscation, angr |
| [web.md](web.md) | Web exploitation — SQLi, XSS, SSTI, LFI, command injection, JWT |
| [crypto.md](crypto.md) | Cryptography — RSA, XOR, AES, hash, encoding, classical |
| [forensic.md](forensic.md) | Forensics — file carving, pcap, memory, stego, disk image |
| [osint.md](osint.md) | OSINT — reverse image, metadata, geolocation, people search |
| [misc.md](misc.md) | Misc — pyjail, bash, game/logic, scripting cepat |
| [templates/](templates/) | Template exploit siap pakai (pwntools, solve.py, dll) |

## Cara pakai pas lomba

1. **Baca soal → tentuin kategori → buka file kategori itu.**
2. Tiap file disusun: **triage cepat → teknik per jenis bug → command → gotcha.**
3. Kalau mentok, cek bagian **"Checklist kalau stuck"** di tiap file.
4. Prioritas poin: di CTF dynamic-scoring, **soal yang sedikit solve = poin gede.** Kelarin low-hanging fruit dulu biar aman, tapi sisain waktu buat 1-2 soal susah bernilai tinggi.

## Workflow umum tiap soal

```
1. Baca deskripsi + hint + author (kadang bocor teknik)
2. Identifikasi file/service: file <binary> ; checksec ; nmap/nc
3. Tentuin kelas bug dari gejalanya
4. Cari path ke flag (format: biasanya flag{...} / <event>{...})
5. Script kalau repetitif (pwntools / requests / python)
6. Catat flag + simpan solve script
```

## Catatan pribadi (AgriHack 0x0b → persiapan final)
- **Kuat:** REV & WEB. Jaga momentum.
- **Lemah (PRIORITAS DRILL):** PWN lanjut — format string, ROP chain, ret2libc. Lihat [pwn.md](pwn.md).
- Low-solve = high-value: dulu ulaaaaaaar (500), CetGipitiPro (491), HamPORTAL (484) ngangkat skor paling banyak.
