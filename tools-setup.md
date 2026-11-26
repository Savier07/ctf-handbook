# Tools Setup

Jalanin **sebelum lomba** biar pas hari-H gak buang waktu install. Target: Linux (native/VM/WSL). Banyak tool pwn/rev gak jalan mulus di macOS — **siapin VM Linux (Ubuntu/Kali) atau Docker**.

## 0. Base
```bash
sudo apt update && sudo apt install -y build-essential gdb python3 python3-pip git \
  netcat-openbsd nmap binutils file xxd curl wget unzip p7zip-full ltrace strace
```

## 1. Python / pwntools (PWN inti)
```bash
python3 -m pip install --upgrade pip
pip install pwntools ropgadget angr pycryptodome requests
```
Cek: `python3 -c "import pwn; print(pwn.__version__)"`

## 2. gdb + pwndbg (debugger wajib buat pwn/rev)
```bash
git clone https://github.com/pwndbg/pwndbg && cd pwndbg && ./setup.sh
```
Alternatif: **GEF** (`bash -c "$(curl -fsSL https://gef.blah.cat/sh)"`). Pilih salah satu.

## 3. ROP / exploit helpers
```bash
pip install ropgadget                 # cari gadget
# one_gadget (butuh ruby):
sudo apt install -y ruby && sudo gem install one_gadget
# ropper (alternatif ROPgadget):
pip install ropper
```

## 4. libc tools (ret2libc)
```bash
git clone https://github.com/niklasb/libc-database && cd libc-database && ./get
# cari libc dari offset: ./find printf 760  (contoh)
```
Online cadangan (kalau lomba izinin internet): https://libc.rip , https://libc.blukat.me

## 5. Reverse engineering
- **Ghidra** — decompiler gratis terbaik: https://ghidra-sre.org (butuh JDK 17+)
- **radare2 / rizin**: `sudo apt install radare2`  (atau cutter buat GUI)
- **IDA Free** (opsional, Windows/Linux)
- **dnSpy** (.NET), **jadx** (Android/Java): `sudo apt install jadx`
- **upx** (unpack): `sudo apt install upx-ucl`

## 6. Web
```bash
sudo apt install -y sqlmap
pip install requests httpx
```
- **Burp Suite Community** — proxy/intercept: https://portswigger.net/burp
- **ffuf** (fuzzing dir/param): `go install github.com/ffuf/ffuf/v2@latest` atau `sudo apt install ffuf`
- **jwt_tool**: `git clone https://github.com/ticarpi/jwt_tool`

## 7. Crypto
```bash
pip install pycryptodome gmpy2 sympy
git clone https://github.com/RsaCtfTool/RsaCtfTool && pip install -r RsaCtfTool/requirements.txt
```
- **CyberChef** (offline!): download dari https://github.com/gchq/CyberChef/releases → buka `CyberChef_vX.html` di browser tanpa internet
- **dCode** (online): https://www.dcode.fr (classical ciphers)

## 8. Forensics / Stego
```bash
sudo apt install -y binwalk foremost exiftool steghide zsteg outguess \
  tshark tcpdump sleuthkit testdisk
pip install volatility3
```
- **stegsolve** (jar), **wireshark** (GUI pcap), **Audacity** (audio/spectrogram)
- **Aperi'Solve** (online all-in-one stego): https://aperisolve.com

## 9. OSINT
- Google Lens / Yandex Images / TinEye (reverse image)
- `exiftool <img>` (metadata/GPS)
- Google Maps + Street View, GeoHints, SunCalc (geolocation)
- Sherlock (`pip install sherlock-project`) — username search

## Checklist pre-lomba
- [ ] VM Linux nyala & snapshot bersih dibikin
- [ ] pwntools + pwndbg kejalan (`checksec` works)
- [ ] Ghidra kebuka, JDK ok
- [ ] CyberChef offline kesimpen
- [ ] Burp proxy keset di browser
- [ ] libc-database ke-download
- [ ] Template exploit (templates/) ke-copy ke working dir
