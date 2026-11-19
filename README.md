# Build Your Own Search Engine — Python (Vector Space)

Mesin pencari mungil berbasis **model ruang vektor** yang
ditulis ulang dari nol di Python murni, mengikuti panduan
**Ben Boyter, "Building a Vector Space Indexing Engine in
Python"** (2010) —
https://boyter.org/2010/08/build-vector-space-search-engine-python/
(entri Python kategori Search Engine di build-your-own-x).

Dokumen dan kueri sama-sama diubah menjadi vektor hitungan
kata (*concordance*); relevansi adalah **kemiripan kosinus**
antara kedua vektor itu.

## Contoh

```bash
$ python3 cari.py captcha
0.12403473458921759 Why You Shouldnt roll your own CAPTCHA At a TechEd I attended ...
0.09578262852210709 Why CAPTCHA Never Use Numbers 0 1 5 7 Interestingly this sort ...

$ python3 cari.py            # mode interaktif, seperti demo panduan
Enter Search Term: mysql stallman
0.14002800840280097 Richard Stallman to visit Australia Im not usually one to ...
0.11009637651262618 MySQL Backups Done Easily One thing that comes up a lot on ...
```

Kedua skor itu persis nilai yang dicetak artikel aslinya pada
2010 — port Python 3 di sini (artikelnya Python 2)
bereproduksi sampai di bawah 1e-12.

## API

```python
from mesincari import MesinCari

m = MesinCari()
m.tambah(1, "kucing makan ikan")
m.tambah(2, "anjing tidur seharian")
m.cari("kucing")        # [(skor, id, cuplikan100), ...]
m.cari_cepat("kucing")  # hasil identik, lebih sedikit perbandingan
m.cari_tfidf("kucing")  # peringkat berbobot TF-IDF
m.cari_and("kucing ikan")  # boolean AND: kedua kata wajib ada
```

## Lanjutan di luar panduan (berlabel)

Penulis panduan menutup artikelnya dengan tiga kelemahan
teknik ini. Irisan 3–4 build ini menjawabnya, tanpa mengubah
mode bawaan:

1. **Berat di CPU** → *indeks terbalik*: hanya dokumen yang
   berbagi kata dengan kueri yang dibandingkan. Hasilnya
   dibuktikan identik dengan brute force (korpus panduan +
   40 kueri atas korpus acak 500 dokumen).
2. **Bias peringkat** → *mode TF-IDF*: kata langka menimbang
   lebih berat daripada kata pasaran (`idf = log(N/df)`;
   kata yang ada di semua dokumen berbobot 0).
3. **Tak ada boolean** → *mode AND*: dokumen wajib memuat
   semua kata kueri sebelum diperingkat.

## Uji

```bash
python3 uji_irisan1.py   # inti VectorCompare + jangkar emas panduan
python3 uji_irisan2.py   # MesinCari + CLI end-to-end
python3 uji_irisan3.py   # indeks terbalik: kesetaraan diferensial
python3 uji_irisan4.py   # TF-IDF & boolean + regresi penuh
```

Total 69 pemeriksaan, termasuk keempat nilai cetak panduan
yang bereproduksi persis.

Bagian dari seri **build-your-own-x** (fork
`codecrafters-io/build-your-own-x`): implementasi ulang
Python dari panduan-panduan klasik, dikerjakan irisan demi
irisan dengan uji di setiap langkah. Rencana dan pagar
kelengkapan ada di `RENCANA.md`; konsep per irisan dan temuan
selama pengerjaan ada di `CATATAN.md`.

## Lisensi & atribusi

Kode di repo ini adalah penulisan ulang untuk belajar.
Algoritma dan korpus demonya berasal dari artikel Ben Boyter
di atas; cuplikan 7 pos blog dalam `cari.py` dan berkas uji
adalah data demo artikel tersebut.
