# OSINT — Open Source Intelligence

> Kekuatan kamu (dorothy, Sojourn, kepo, RCT). Prinsip: **clue sering literal** — baca deskripsi baik-baik, kerjain dari petunjuk konkret.

## Langkah 0: metadata dulu
```bash
exiftool image.jpg          # GPS, device, timestamp, author, software, comment
exiftool -a -G1 image.jpg   # semua tag + grup
```
- **GPS** → koordinat langsung ke Google Maps.
- Comment / XMP / Author / Software sering nyimpen clue. Timestamp → timezone/urutan.

## Reverse image search (coba SEMUA, hasil beda)
- **Google Lens** — terbaik buat objek/landmark/teks/produk.
- **Yandex Images** — terbaik buat wajah & lokasi (terutama non-Barat).
- **TinEye** — cari sumber asli & duplikat tertua.
- **Bing Visual Search**, **PimEyes** (wajah, hati-hati).
- Crop/zoom bagian penting dulu (plang, logo, wajah) sebelum search.

## Geolocation (nemu lokasi dari foto)
Petunjuk: landmark, bahasa/tulisan plang, plat nomor, arah & panjang bayangan, vegetasi, arsitektur, tiang listrik, marka jalan, cuaca.
- **Google Maps + Street View**, **Google Earth**, **Mapillary**, **KartaView** (street-level).
- **SunCalc** / suncalc.org — posisi matahari → perkiraan waktu & arah.
- **GeoHints**, **Geoguessr tips**, plonkit.net (ciri per negara).
- Persempit: negara → region → kota → titik. Cocokkan detail unik.

## Orang / akun / username
- **Sherlock**: `sherlock <username>` → cek ratusan platform. **WhatsMyName**, namechk.
- Instagram/X/TikTok/LinkedIn/GitHub/Facebook: bio, postingan, tag lokasi, following, foto profil (reverse search).
- Kasus kepo: format post IG `instagram.com/p/<ID>`; dari gambar → Lens → akun → bio → password di bio postingan lain.
- Email: **holehe** (akun terdaftar), hunter.io, haveibeenpwned (breach), Google dork `"email"`.
- Nomor HP: truecaller, format internasional.

## Google dorking
```
site:example.com filetype:pdf
intitle:"index of" "flag"
inurl:admin "keyword"
"exact phrase" -exclude
cache:url   (versi cache)
```

## Domain / IP / infrastruktur
```bash
whois domain.com ; dig domain.com ANY ; dig +short domain.com
host domain.com ; nslookup domain.com
```
- **crt.sh** (subdomain dari Certificate Transparency), **Shodan** (`org:`, `ssl:`, port), **Censys**.
- **Wayback Machine** (web.archive.org) — versi lama situs (konten dihapus, robots lama). **urlscan.io** — screenshot & request situs.
- **DNS history**: securitytrails, dnsdumpster.
- GitHub: `git log -p` (secret di history), code search leaked creds, commit author email.

## Media sosial & verifikasi waktu
- Timestamp post → timezone. Refleksi di kacamata/jendela/mata. Event/cuaca/liga olahraga buat konfirmasi tanggal.
- Cross-reference beberapa platform buat konfirmasi identitas (foto sama, username mirip, teman sama).
- Wayback + Google cache buat konten yang udah dihapus.

## Dokumen / buku / media (kasus dorothy)
- Clue sastra/film → cari judul (karakter → novel → edisi → halaman). Google Books, archive.org (buku full, cari halaman spesifik).
- Metadata PDF (producer, tanggal) → persempit sumber.

## Checklist stuck
- [ ] `exiftool` (GPS/metadata/comment)?
- [ ] Reverse image di Lens + Yandex + TinEye (crop dulu)?
- [ ] Username → Sherlock + cek manual tiap platform?
- [ ] Clue teks/landmark → Maps/Street View/SunCalc?
- [ ] Wayback / crt.sh / Shodan buat web lama & infra?
- [ ] Baca ulang deskripsi — clue hampir selalu literal & mengarah.
- [ ] Gabungkan beberapa clue (foto + bio + tanggal) buat konfirmasi.
