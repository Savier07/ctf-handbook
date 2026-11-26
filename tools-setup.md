# Tools Setup

Jalanin **sebelum lomba**. Target: Linux (native/VM/WSL). Banyak tool pwn/rev gak jalan mulus di macOS — **siapin VM Linux (Ubuntu/Kali) atau Docker**.

## 0. Base
```bash
sudo apt update && sudo apt install -y build-essential gdb python3 python3-pip python3-venv \
  git netcat-openbsd nmap binutils file xxd curl wget unzip p7zip-full ltrace strace \
  ruby default-jdk tmux vim jq
```

## 1. Python / pwntools (PWN inti)
```bash
python3 -m pip install --upgrade pip
pip install pwntools ropgadget ropper angr pycryptodome gmpy2 sympy requests
```
Cek: `python3 -c "import pwn; print(pwn.__version__)"`
> Tips: pakai virtualenv per event biar gak bentrok: `python3 -m venv .venv && source .venv/bin/activate`.

## 2. gdb + pwndbg (debugger wajib pwn/rev)
```bash
git clone https://github.com/pwndbg/pwndbg && cd pwndbg && ./setup.sh
```
Alternatif: **GEF** (`bash -c "$(curl -fsSL https://gef.blah.cat/sh)"`) atau **pwndbg** keduanya. Plugin berguna: `gdb-pt-dump`, `splitmind`.

## 3. ROP / exploit helpers
```bash
pip install ropgadget ropper
sudo gem install one_gadget        # one-shot execve shell
sudo apt install -y patchelf       # ganti interpreter/libc biner
```
- `ROPgadget --binary ./chall | grep 'pop rdi'`
- `one_gadget ./libc.so.6`
- `patchelf --set-interpreter ./ld-x.xx.so --replace-needed libc.so.6 ./libc.so.6 ./chall` (jalanin biner pakai libc soal)

## 4. libc tools (ret2libc)
```bash
git clone https://github.com/niklasb/libc-database && cd libc-database && ./get
./find printf 760                  # cari libc dari 3 digit terakhir offset
./dump <libc-id>                   # dump offset fungsi
```
Online cadangan: https://libc.rip , https://libc.blukat.me

## 5. Reverse engineering
- **Ghidra** (decompiler gratis terbaik): https://ghidra-sre.org (butuh JDK 17+). Belajar shortcut: `L`=rename, `;`=comment, `Ctrl+Shift+E`=patch.
- **radare2 / rizin**: `sudo apt install radare2` (GUI: **Cutter**).
- **IDA Free** (opsional).
- **.NET**: dnSpy / ILSpy. **Java/APK**: `sudo apt install jadx` (jadx-gui). **Android**: apktool, frida.
- **Python bytecode**: `pip install decompyle3 uncompyle6` ; pycdc (build dari source).
- **upx**: `sudo apt install upx-ucl` (unpack: `upx -d`).

## 6. Web
```bash
sudo apt install -y sqlmap ffuf gobuster wfuzz
pip install requests httpx
git clone https://github.com/ticarpi/jwt_tool
```
- **Burp Suite Community**: https://portswigger.net/burp (proxy, Repeater, Intruder).
- **ffuf**: `ffuf -u http://host/FUZZ -w wordlist.txt -mc 200,301`
- Wordlists: `sudo apt install seclists` → `/usr/share/seclists`.

## 7. Crypto
```bash
pip install pycryptodome gmpy2 sympy
git clone https://github.com/RsaCtfTool/RsaCtfTool && pip install -r RsaCtfTool/requirements.txt
pip install sagemath   # atau pakai SageMathCell online buat lattice/ECC
```
- **CyberChef offline**: download release dari https://github.com/gchq/CyberChef/releases → buka `CyberChef_vX.html` di browser tanpa internet (fitur **Magic** = auto-decode).
- **dCode** (online): https://www.dcode.fr (classical ciphers).
- **SageMath**: buat lattice (LLL), ECC, modular — install atau pakai cocalc/SageCell online.

## 8. Forensics / Stego
```bash
sudo apt install -y binwalk foremost exiftool steghide outguess pngcheck \
  tshark tcpdump sleuthkit testdisk qpdf poppler-utils zbar-tools
pip install volatility3
gem install zsteg
```
- **stegsolve.jar**, **Wireshark** (GUI pcap), **Audacity**/Sonic Visualiser (audio spectrogram).
- **Aperi'Solve** (online all-in-one stego): https://aperisolve.com
- **ImHex / 010 Editor** (hex editor dengan template).

## 9. OSINT
- Google Lens / Yandex Images / TinEye / Bing Visual (reverse image).
- `exiftool <file>` (metadata/GPS).
- `pip install sherlock-project` (username search), `holehe` (email).
- Google Maps + Street View, SunCalc, GeoHints.

## 10. macOS native (kalau gak pakai VM)
- Banyak tool via brew: `brew install binwalk exiftool radare2 nmap ghidra`.
- **PWN gak reliable di macOS** (binary Linux) → tetap pakai VM/Docker Linux buat pwn.
- Docker cepat: `docker run -it --rm -v $PWD:/w -w /w ubuntu:22.04 bash`.

## Troubleshooting
- **`bad CPU type in executable`** (macOS Apple Silicon): binary salah arch (Intel di arm64). Reinstall native: `brew install <tool>`; pastiin `/opt/homebrew/bin` duluan di PATH (`hash -r` abis install). Cek: `file $(which tool)` → harus `arm64`.
- **`Command Line Tools does not support macOS X`**: update CLT — `sudo rm -rf /Library/Developer/CommandLineTools && sudo xcode-select --install`. Gak ganggu tool yang pakai bottle precompiled.
- **pwntools `process` gagal di mac**: pakai VM/Docker Linux.
- **Ghidra gak kebuka**: cek `JAVA_HOME` JDK 17+.

## Checklist pre-lomba
- [ ] VM Linux nyala & snapshot bersih
- [ ] pwntools + pwndbg kejalan (`checksec` works)
- [ ] Ghidra kebuka (JDK ok)
- [ ] CyberChef offline kesimpen
- [ ] Burp proxy keset di browser
- [ ] libc-database ke-download, one_gadget jalan
- [ ] Repo handbook di-clone + templates ke-copy
- [ ] SecLists / wordlists ada
