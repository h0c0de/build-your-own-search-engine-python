# Catatan — Vector Space Search Engine (Boyter)

Satu halaman per irisan: konsep inti + temuan selama
pengerjaan. Panduan: Ben Boyter, "Building a Vector Space
Indexing Engine in Python" (2010) —
https://boyter.org/2010/08/build-vector-space-search-engine-python/

## Irisan 1 — Inti VectorCompare

Konsep inti: **dokumen adalah vektor, relevansi adalah
sudut.** Concordance mengubah teks menjadi vektor hitungan
kata; magnitude adalah panjang vektor itu; relation adalah
kosinus sudut antara vektor kueri dan vektor dokumen — dot
product dibagi perkalian panjang. Dokumen yang arahnya paling
sejajar dengan kueri menang, berapa pun panjangnya.

Temuan:
- Keempat nilai cetak panduan (2010, Python 2) bereproduksi
  pada port Python 3 ini sampai di bawah 1e-12 — port-nya
  terbukti setia, bukan kira-kira.
- Kosinus dokumen identik TIDAK persis 1.0 dalam aritmetika
  apung (3/(√3·√3) = 1.0000000000000002) — uji pertama yang
  menuntut == 1.0 gagal dengan benar; toleransi adalah
  jawaban jujurnya.
- Keanehan yang dipertahankan apa adanya: pecah pada spasi
  tunggal berarti spasi ganda melahirkan "kata" string
  kosong, dan concordance peka huruf besar (lowercase adalah
  urusan pemanggil, persis seperti pemakaian di panduan).

## Irisan 2 — Mesin pencari & CLI

Konsep inti: **pembungkusan yang setia.** MesinCari tidak
menambah matematika apa pun — ia hanya mengotomatiskan
persis apa yang skrip panduan lakukan dengan tangan:
lowercase, concordance per dokumen, bandingkan kueri ke
semua, buang nol, urutkan menurun, tampilkan cuplikan 100
karakter dari teks ASLI (bukan yang sudah di-lowercase).

Temuan:
- Demo panduan berjalan end-to-end lewat dua pintu (kelas
  langsung dan CLI subproses, interaktif maupun satu-tembak)
  dengan urutan, skor, dan cuplikan yang cocok.
- Satu penyimpangan kecil yang disengaja: panduan mengurutkan
  tuple (skor, cuplikan) sehingga seri dipecahkan oleh teks
  cuplikan; kami mengurutkan (skor menurun, id menaik) agar
  hasil deterministik dan bisa diuji — urutan demo panduan
  tidak terpengaruh karena skornya tidak seri.

## Irisan 3 — Indeks terbalik

Konsep inti: **jangan bandingkan yang pasti nol.** Relasi
kosinus dokumen yang tidak berbagi satu kata pun dengan
kueri selalu 0, jadi indeks terbalik (kata → himpunan dokumen
yang memuatnya) membatasi perbandingan hanya ke gabungan
postings kata-kata kueri. Ini menjawab kelemahan ketiga yang
dicatat penulis panduan (berat di CPU) tanpa mengubah satu
pun hasil.

Temuan:
- Kesetaraan dibuktikan, bukan diklaim: hasil cari_cepat
  identik byte-per-byte (termasuk skor float-nya) dengan
  brute force pada korpus panduan dan 40 kueri atas korpus
  acak 500 dokumen.
- Pada korpus acak itu, kueri satu kata langka turun dari 500
  perbandingan ke hanya dokumen berkandidat; kata di luar
  kosakata berharga 0 perbandingan.
- Harga strukturnya ada di tambah(): indeks ulang sebuah
  dokumen kini wajib mencabut postings versi lamanya —
  diuji eksplisit karena di situlah indeks terbalik biasanya
  diam-diam membusuk.

## Irisan 4 — TF-IDF & boolean + terbit

Konsep inti: **kata pasaran tidak membedakan apa pun.**
TF-IDF menimbang tiap kata dengan log(N/df): kata yang ada
di semua dokumen berbobot tepat 0, kata langka menimbang
paling berat — dan kosinus yang sama persis dari irisan 1
berjalan di atas vektor berbobot itu tanpa diubah. Mode AND
adalah irisan himpunan postings sebelum peringkat.

Temuan:
- Efek TF-IDF dibuktikan sebagai pertukaran urutan yang
  konkret pada korpus rancangan: mode mentah menaruh dokumen
  yang hanya cocok di kata pasaran "umum" di atas dokumen
  yang cocok di kata langka "kucing"; TF-IDF membaliknya,
  ujung-ujung urutan tidak berubah.
- Satu ekspektasi uji sempat salah dari sisi penulis uji
  (urutan mentah "captcha numbers" adalah 6 lalu 3, bukan
  3 lalu 6 — dok 6 memuat kedua kata sehingga dot-nya tiga
  kali) — mesinnya benar sejak awal; yang diperbaiki ujinya.
- Mode bawaan panduan tidak bergeser sedikit pun oleh kedua
  lanjutan: nilai "captcha" tetap nilai cetak 2010.
- Total seri uji build ini: 69 pemeriksaan (20 + 15 + 17 + 17).
