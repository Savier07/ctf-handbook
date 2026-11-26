# FORENSIC — Forensics

> Kategori luas. Penyisihan banyak high-value kelewat (warm, descuidado, traffis, King Stegano? semua 499-500). Mulai `file` + `binwalk` + `strings` selalu.

## Triage file misterius
```bash
file mystery            # tipe sebenernya (jangan percaya ekstensi)
xxd mystery | head       # magic bytes (tabel bawah)
binwalk mystery          # file tersembunyi di dalam?
binwalk -e mystery       # extract (atau: foremost / 7z x)
strings -n 8 mystery | grep -iE 'flag|ctf|pass|key'
strings -el mystery      # UTF-16
exiftool mystery         # metadata
```
### Magic bytes
| Hex | Tipe |
|-----|------|
| `FF D8 FF` | JPG |
| `89 50 4E 47 0D 0A 1A 0A` | PNG |
| `47 49 46 38` | GIF |
| `50 4B 03 04` | ZIP/APK/docx/jar/xlsx |
| `25 50 44 46` | PDF |
| `52 61 72 21` | RAR |
| `1F 8B` | gzip |
| `37 7A BC AF 27 1C` | 7z |
| `42 4D` | BMP |
| `49 49 2A 00` / `4D 4D 00 2A` | TIFF |
| `66 74 79 70` (offset 4) | MP4/MOV |
Header rusak? edit magic bytes pakai hex editor (`xxd`, ImHex, 010). Dimensi PNG salah (crop) → fix IHDR width/height.

## File carving / embedded
- `binwalk -e` gagal? → `foremost mystery`, `photorec`, atau manual: cari offset dari `binwalk`, lalu `dd if=f of=out bs=1 skip=OFFSET`.
- ZIP nempel di JPG (Cinnamoroll/Pompompurin): `unzip file.jpg` / `binwalk -e`.
- Nested zip + password: cari password di PNG/strings/nama item/deskripsi. ZIP crack: `fcrackzip -u -D -p rockyou.txt f.zip` / `zip2john f.zip > h; john h`.
- Polyglot file (valid 2 format sekaligus).

## Stego — gambar
```bash
exiftool img.jpg            # comment/metadata/GPS
steghide extract -sf img.jpg   # JPG/BMP/WAV (passphrase, kadang kosong)
steghide info img.jpg
zsteg img.png               # PNG/BMP LSB
zsteg -a img.png            # semua metode
stegsolve                   # GUI: bit plane, channel, XOR dua gambar
outguess -r img.jpg out.txt
pngcheck -v img.png         # chunk aneh / data setelah IEND
```
- **PNG/BMP**: LSB (`zsteg`), bit plane (stegsolve), chunk tambahan, data setelah IEND.
- **JPG**: `steghide`, `outguess`, `jsteg`, DCT.
- Dua gambar mirip → XOR / diff (stegsolve).
- All-in-one online: **aperisolve.com**. Steghide passphrase brute: `stegseek img.jpg rockyou.txt`.

## Stego — audio
- **Spectrogram**: Audacity / Sonic Visualiser (teks/QR muncul di spektrum).
- **LSB audio**, **Morse** (dengerin/ukur durasi), **DTMF** (tone telepon → dtmf decoder).
- Reverse / speed change / channel kiri-kanan beda.
- SSTV (gambar via radio) → QSSTV.

## PDF / Office
```bash
pdfinfo f.pdf; pdftotext f.pdf -; pdfimages -all f.pdf out; pdfdetach -list f.pdf
exiftool f.pdf; binwalk f.pdf; qpdf --qdf --object-streams=disable f.pdf out.pdf  # un-compress streams
# office = zip:
unzip -o f.docx -d out && grep -riE 'flag|http' out
```
- Teks disembunyiin (warna putih, di belakang gambar, metadata), object stream, JS embed.

## PCAP (Wireshark / tshark)
```bash
tshark -r f.pcap -q -z io,phs                       # protokol hierarchy (overview)
tshark -r f.pcap -Y "http.request" -T fields -e http.host -e http.request.uri
tshark -r f.pcap --export-objects http,out/          # extract file HTTP
tshark -r f.pcap -Y "ftp || telnet" -T fields -e text  # kredensial plaintext
tshark -r f.pcap -z follow,tcp,ascii,0               # follow stream index 0
```
- Wireshark GUI: **Follow TCP/HTTP/TLS Stream**, File → **Export Objects**, Statistics → Conversations/Protocol Hierarchy.
- **USB keyboard** (HID): usage codes → tulisan (script `usbkeyboard`). **USB mouse**: rekonstruksi gerakan.
- **DNS exfil**: data di subdomain. **ICMP**: data di payload. **TLS**: butuh key (SSLKEYLOGFILE) buat decrypt.
- **RTP/VoIP** (kasus Pesan): Telephony → RTP → Stream Analysis → decode audio; `tshark -Y rtp -T fields -e rtp.payload`; cek `rtp.p_type` (0=PCMU/G.711).
- WiFi (WPA): `aircrack-ng -w rockyou.txt f.pcap` (butuh handshake).

## Memory dump (volatility3)
```bash
vol -f mem.raw windows.info          # profil
vol -f mem.raw windows.pslist        # proses
vol -f mem.raw windows.cmdline       # command line
vol -f mem.raw windows.filescan | grep -i flag
vol -f mem.raw windows.dumpfiles --virtaddr 0x...
vol -f mem.raw windows.hashdump      # hash NTLM
vol -f mem.raw windows.netscan ; windows.registry.printkey
# linux: linux.bash (history), linux.pslist
```

## Disk image (Sleuth Kit)
```bash
mmls disk.img                        # partisi
fls -r -o <offset> disk.img          # list file (termasuk deleted, recursive)
icat -o <offset> disk.img <inode> > out
# atau mount:
sudo mount -o loop,ro,offset=$((512*OFFSET)) disk.img /mnt
```
Kasus Green Tree: `fls -r` → nama folder = potongan flag (urut angka → map karakter dari README).

## Git / version forensics
```bash
git log --all --oneline ; git log -p             # cari di history
git stash list ; git reflog                       # commit/stash tersembunyi
git show <hash>:path/to/file                       # file di commit tertentu
# .git bocor di web: git-dumper http://host/.git out/
```

## QR / barcode
```bash
zbarimg code.png        # decode QR/barcode
```
QR rusak → rekonstruksi finder pattern / error correction (QRazyBox online).

## Checklist stuck
- [ ] `file` + `binwalk -e` + `strings` + `exiftool`?
- [ ] Magic bytes bener? header/dimensi perlu difix?
- [ ] Gambar → zsteg/steghide/stegseek/stegsolve/aperisolve?
- [ ] Audio → spectrogram / Morse / DTMF?
- [ ] pcap → protocol hierarchy → follow stream / export objects?
- [ ] USB HID / DNS / ICMP exfil?
- [ ] Memory → volatility3 (pslist/cmdline/filescan)?
- [ ] Disk → fls/icat (file deleted)?
- [ ] Ekstensi bohong? polyglot? data setelah EOF?
