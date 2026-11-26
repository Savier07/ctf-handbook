# OSINT — Open Source Intelligence

> Cari jejak digital dari petunjuk (gambar, username, metadata). Kekuatan kamu (dorothy, Sojourn, kepo).

## Metadata dulu
```bash
exiftool image.jpg          # GPS, device, timestamp, author, software
```
- **GPS** → langsung masukin koordinat ke Google Maps.
- Comment / XMP / author field sering nyimpen clue.

## Reverse image search
Coba **semua** engine (hasil beda-beda):
- **Google Lens** (paling kuat buat objek/landmark/teks)
- **Yandex Images** (terbaik buat wajah & lokasi)
- **TinEye** (cari sumber asli/duplikat)
- **Bing Visual Search**

## Geolocation (nemu lokasi dari foto)
- Landmark, bahasa plang, plat nomor, arah bayangan.
- **Google Maps + Street View**, GeoHints, Mapillary.
- SunCalc (posisi matahari → waktu/arah). Wikimapia.
- Clue vegetasi/arsitektur → persempit negara dulu (GeoGuessr tips).

## Orang / akun / username
- **Sherlock**: `sherlock <username>` → cek ratusan platform.
- WhatsMyName, namechk.com.
- Instagram/Twitter/LinkedIn/GitHub: bio, postingan, tag lokasi, foto.
- Kasus kepo: format post IG `instagram.com/p/<ID>`; cari via Lens → akun → bio → password.
- Email: hunter.io, haveibeenpwned (breach), Google dork.

## Google dorking
```
site:example.com filetype:pdf
intitle:"index of" "flag"
inurl:admin "keyword"
"exact phrase" -exclude
```

## Domain / IP / web
```bash
whois domain.com; dig domain.com; nslookup domain.com
```
- **crt.sh** (subdomain dari cert), **Wayback Machine** (web.archive.org — versi lama situs), **urlscan.io**, **Shodan**.
- GitHub: cari leaked creds/commit history (`git log -p`).

## Media sosial & orang spesifik
- Timestamp post → timezone. Reflection di kacamata/jendela. Event/cuaca buat verifikasi tanggal.
- Cross-reference beberapa platform buat konfirmasi identitas.

## Checklist stuck
- [ ] exiftool (GPS/metadata)?
- [ ] Reverse image di Lens + Yandex + TinEye?
- [ ] Username → Sherlock + manual cek platform?
- [ ] Clue teks/landmark → Maps/Street View?
- [ ] Wayback/crt.sh buat web lama/subdomain?
- [ ] Baca ulang deskripsi — clue sering literal.
