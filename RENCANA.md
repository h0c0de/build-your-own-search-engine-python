# Rencana — Build Kelima Belas: Vector Space Search Engine

Mengikuti panduan **Ben Boyter**, *"Building a Vector Space
Indexing Engine in Python"* (2010) — entri Python kategori
Search Engine di repo codecrafters-io/build-your-own-x.

Panduan: https://boyter.org/2010/08/build-vector-space-search-engine-python/

## Isi panduan (terverifikasi 20 Nov 2026, dibaca utuh)

Mesin pencari mungil berbasis model ruang vektor:

- `concordance(dokumen)` — hitungan kemunculan tiap kata
  (dokumen dipecah pada spasi).
- `VectorCompare.magnitude(concordance)` — panjang vektor:
  akar jumlah kuadrat hitungan.
- `VectorCompare.relation(c1, c2)` — kemiripan kosinus:
  dot product dibagi perkalian magnitude; 0 bila penyebut 0.
  Hasil 0..1, makin besar makin relevan.
- Pemakaian: indeks = concordance tiap dokumen (di-lowercase);
  kueri dibandingkan ke semua dokumen, yang relasinya bukan 0
  diurutkan menurun, ditampilkan dengan cuplikan 100 karakter.

Jangkar emas (dihitung ulang SEBELUM kode ditulis, cocok
dengan cetakan panduan sampai digit terakhir yang dicetak):
pada 7 dokumen blog penulisnya — kueri "captcha": dok 3 =
0.124034734589, dok 6 = 0.0957826285221; kueri "mysql
stallman": dok 1 = 0.140028008403, dok 2 = 0.110096376513.

Penulis sendiri mencatat tiga kelemahan teknik ini: (1) tidak
ada pencarian boolean, (2) bias ke dokumen kecil, (3) berat di
CPU karena membandingkan ke semua dokumen. Irisan 3–4 adalah
lanjutan berlabel yang menjawab kelemahan (3) dan (1)/(2)
dengan indeks terbalik, bobot TF-IDF, dan mode boolean AND.

## Adaptasi yang dicatat terbuka

- Port Python 2 → Python 3 (panduan 2010): has_key → in,
  iteritems → items, raw_input → input. Algoritma TIDAK
  berubah — dibuktikan oleh jangkar emas di atas yang
  bereproduksi persis.
- Irisan 3–4 (indeks terbalik, TF-IDF, boolean) BUKAN bagian
  panduan; keduanya lanjutan kami yang menjawab daftar
  kelemahan penulisnya sendiri, dan dilabeli sebagai itu.

## Irisan

- [x] Irisan 1 — Inti VectorCompare: concordance, magnitude,
      relation (port setia, termasuk ValueError tipe ala
      panduan). Bukti: kosinus hitung tangan pada dokumen
      mungil + keempat nilai cetak panduan pada 7 dokumennya.
- [x] Irisan 2 — Mesin pencari & CLI: kelas MesinCari
      (tambah dokumen, cari terurut, cuplikan), CLI interaktif
      meniru panduan. Bukti: dua pencarian demo panduan
      end-to-end (urutan + nilai + cuplikan).
- [x] Irisan 3 — Indeks terbalik (lanjutan): hanya dokumen
      yang berbagi kata dengan kueri yang dibandingkan.
      Bukti: hasil IDENTIK dengan brute force pada korpus
      panduan + korpus acak 500 dokumen; jumlah perbandingan
      yang dihemat terhitung.
- [x] Irisan 4 — TF-IDF & boolean + terbit: mode bobot
      TF-IDF (bawaan tetap mode mentah panduan) dan mode
      boolean AND; regresi 1–3; terbit ke
      `build-your-own-search-engine-python`.

## Pagar selesai

- [x] Keempat nilai cetak panduan bereproduksi persis.
- [x] Hasil indeks terbalik identik brute force pada korpus uji.
- [x] Mode mentah (bawaan) tidak berubah oleh lanjutan 3–4.
- [x] `CATATAN.md` satu halaman per irisan: konsep inti + temuan.
- [x] Repo GitHub publik `build-your-own-search-engine-python`
      terbit & terverifikasi.
