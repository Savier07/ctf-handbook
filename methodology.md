# Methodology — Strategi & Mindset Lomba

> Teknik doang gak cukup; manajemen waktu & urutan ngerjain sering nentuin ranking.

## Sebelum lomba (H-1)
- [ ] VM Linux siap + snapshot bersih (lihat [tools-setup.md](tools-setup.md)).
- [ ] Semua tool ke-test jalan (pwntools, Ghidra, Burp, CyberChef offline).
- [ ] Clone repo handbook ini ke mesin lomba: `git clone https://github.com/Savier07/ctf-handbook`.
- [ ] Template exploit ke-copy ke folder kerja.
- [ ] Tidur cukup. Otak segar > 2 jam begadang.

## Jam pertama (scan seluruh board)
1. **Baca SEMUA soal dulu** sebelum ngerjain. Catat tebakan kategori + estimasi susah.
2. Mulai dari **yang paling gampang / paling banyak solve** → kumpulin poin cepat, bangun momentum & percaya diri.
3. Tandai 2-3 soal high-value yang masih keliatan masuk akal buat lu → jadwalin di tengah lomba pas fokus penuh.

## Urutan prioritas (dynamic scoring)
- Poin turun makin banyak yang solve → **soal low-solve = mahal**. Tapi jangan langsung ke yang 0 solve (sering rabbit hole).
- Pola optimal: **gampang dulu (amanin) → medium (bulk poin) → 1-2 hard (pembeda ranking)**.
- ROI: soal 450-500 poin yang lu bisa > tiga soal 100 poin yang makan waktu sama.

## Baca soal (clue sering literal)
- **Judul & deskripsi**: sering bocorin teknik (nama tool, istilah, meme).
- **Author**: kadang pola (author sama = gaya mirip).
- **Hint**: biasanya ngurangin poin kalau dibuka — buka cuma kalau mentok & poinnya masih worth.
- **File yang dikasih**: ekstensi bisa bohong (`file` dulu).
- **Tags/kategori**: arahin teknik.

## Kalau stuck 20 menit
1. **Baca ulang deskripsi** — ada clue yang kelewat?
2. Cek **asumsi**: udah bener kategori/teknik?
3. Lihat **"checklist kalau stuck"** di file kategori.
4. Coba **teknik lain** buat kelas bug yang sama.
5. **Pindah soal lain**, balik lagi nanti (otak bawah sadar jalan).
6. Catat progress biar pas balik gak mulai dari nol.
> Aturan: jangan ngabisin >45 menit di satu soal tanpa progress keliatan. Pindah.

## Kebiasaan bagus
- **Simpan tiap solve script** (`solve_<chall>.py`) — kepake buat WU + referensi.
- **Screenshot** step penting pas ngerjain (buat write-up & bukti).
- **Catat flag** langsung ke file (`flags.txt`) biar gak ketuker.
- Automasi yang repetitif (pwntools / requests) — jangan manual.
- Kerja di **folder per soal** biar rapi.

## Write-up (kalau wajib, kayak AgriHack)
- **Tulis sendiri, bahasa sendiri** — AI gak boleh nulis WU utuh.
- Kalau pakai AI buat mentoring: sertakan **link share publik** (`claude.ai/share/...`, bukan `/chat/`), isinya sama antara WU & platform.
- **Jangan upload file soal ke AI**, jangan one-shot solve, jangan AI agent. (Di penyisihan ada yang kena revoke gara-gara "upload attachment ke AI" & "no wu".)
- Struktur WU: Deskripsi → Analisis → Temuan kunci → Langkah eksploit (bernomor, + yang sempat gagal) → Flag → AI Source.

## Setup folder lomba (saran)
```
ctf-<event>/
  handbook/        # clone repo ini
  <chall-name>/
    chall          # file soal
    solve.py       # dari templates/
    notes.md       # catatan + flag
  flags.txt
```

## Checklist mental
- Flag udah di depan mata? (strings, source, deskripsi)
- Ekstensi/kategori udah bener?
- Udah coba teknik paling umum buat kategori ini?
- Ada yang repetitif yang harusnya di-script?
- Udah kelamaan? Pindah dulu.
