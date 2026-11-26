# FORENSIC — Forensics

> Kategori luas: file carving, pcap, stego, memory, disk image. Mulai dari `file` + `binwalk` selalu.

## Triage file misterius
```bash
file mystery            # tipe sebenernya (jangan percaya ekstensi)
xxd mystery | head       # magic bytes (lihat tabel)
binwalk mystery          # file tersembunyi di dalam?
binwalk -e mystery       # extract (atau: foremost mystery)
strings -n 8 mystery | grep -i flag
exiftool mystery         # metadata
```
### Magic bytes
| Hex | Tipe |
|-----|------|
| `FF D8 FF` | JPG |
| `89 50 4E 47` | PNG |
| `50 4B 03 04` | ZIP/APK/docx/jar |
| `25 50 44 46` | PDF |
| `52 61 72 21` | RAR |
| `1F 8B` | gzip |
| `37 7A BC AF` | 7z |
Fix header rusak: edit magic bytes pakai `xxd`/hex editor.

## File carving / embedded
- `binwalk -e` gagal? → `foremost`, `photorec`, atau cari offset `binwalk` lalu `dd if=f of=out bs=1 skip=OFFSET`.
- ZIP nempel di JPG (kasus Cinnamoroll/Pompompurin): `unzip file.jpg`.
- Nested zip + password → cari password di PNG/strings/nama item.

## Stego (gambar/audio)
```bash
steghide extract -sf img.jpg          # JPG (passphrase, kadang kosong)
zsteg img.png                          # PNG/BMP LSB
zsteg -a img.png                       # semua metode
stegsolve                              # GUI: bit plane, channel (jar)
outguess -r img.jpg out.txt            # outguess
exiftool img.jpg                       # comment/metadata
```
- **PNG**: LSB (`zsteg`), chunk aneh (`pngcheck -v`), bit plane (stegsolve).
- **JPG**: `steghide`, `outguess`, `jsteg`.
- **Audio (wav/mp3)**: spectrogram di **Audacity**/Sonic Visualiser; LSB; Morse (dengerin/ukur); DTMF.
- All-in-one online: **aperisolve.com**.

## PDF / Office
```bash
pdfinfo f.pdf; pdftotext f.pdf -; pdfimages -all f.pdf out
exiftool f.pdf; binwalk f.pdf
# office = zip:
unzip -o f.docx -d out && grep -r flag out
```

## PCAP (Wireshark / tshark)
```bash
# follow stream, filter protokol
tshark -r f.pcap -Y "http.request" -T fields -e http.host -e http.request.uri
tshark -r f.pcap -Y "http" --export-objects http,out/   # extract file HTTP
tshark -r f.pcap -z follow,tcp,ascii,0
```
- Wireshark GUI: **Follow TCP/HTTP Stream**, File → Export Objects.
- USB keyboard: HID usage codes → tulisan. Telnet/FTP: kredensial plaintext.
- DNS exfil: data di subdomain. ICMP: data di payload.
- **RTP/VoIP** (kasus Pesan): Telephony → RTP → decode audio; cek `rtp.p_type`; ekstrak payload `tshark -Y rtp -T fields -e rtp.payload`.

## Memory dump (volatility3)
```bash
vol -f mem.raw windows.info
vol -f mem.raw windows.pslist
vol -f mem.raw windows.cmdline
vol -f mem.raw windows.filescan | grep -i flag
vol -f mem.raw windows.dumpfiles --virtaddr 0x...
```

## Disk image (Sleuth Kit)
```bash
mmls disk.img                 # partisi
fls -r disk.img               # list file (termasuk deleted)
icat disk.img <inode> > out   # extract file by inode
# atau mount: sudo mount -o loop,ro disk.img /mnt
```
Kasus Green Tree: `fls -r` → nama folder = potongan flag (urut angka, map karakter).

## Checklist stuck
- [ ] `file` + `binwalk -e` + `strings`?
- [ ] Magic bytes bener? header perlu difix?
- [ ] Gambar → zsteg/steghide/stegsolve/aperisolve?
- [ ] Audio → spectrogram?
- [ ] pcap → follow stream / export objects?
- [ ] Ekstensi bohong? (zip in jpg, dll)
