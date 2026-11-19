# mesincari.py — Mesin pencari ruang vektor mungil.
#
# Ditulis ulang dari nol mengikuti panduan Ben Boyter,
# "Building a Vector Space Indexing Engine in Python" (2010).
# Irisan 1: inti VectorCompare — concordance, magnitude,
# relation (kemiripan kosinus). Port Python 3 yang setia:
# algoritma panduan tidak diubah sama sekali.

import math


class VectorCompare:
    """Membandingkan dokumen sebagai vektor hitungan kata."""

    def magnitude(self, concordance):
        """Panjang vektor: akar dari jumlah kuadrat hitungan."""
        if type(concordance) != dict:
            raise ValueError(
                'Supplied Argument should be of type dict')

        total = 0
        for word, count in concordance.items():
            total += count ** 2
        return math.sqrt(total)

    def relation(self, concordance1, concordance2):
        """Kemiripan kosinus dua concordance: 0..1, makin
        besar makin relevan. Nol bila salah satu vektor
        berpanjang nol (penjaga bagi-nol panduan)."""
        if type(concordance1) != dict:
            raise ValueError(
                'Supplied Argument 1 should be of type dict')
        if type(concordance2) != dict:
            raise ValueError(
                'Supplied Argument 2 should be of type dict')

        topvalue = 0
        for word, count in concordance1.items():
            if word in concordance2:
                topvalue += count * concordance2[word]

        penyebut = self.magnitude(concordance1) * \
            self.magnitude(concordance2)
        if penyebut != 0:
            return topvalue / penyebut
        else:
            return 0

    def concordance(self, document):
        """Hitungan kemunculan tiap kata dalam dokumen
        (dokumen dipecah persis pada spasi tunggal)."""
        if type(document) != str:
            raise ValueError(
                'Supplied Argument should be of type string')

        con = {}
        for word in document.split(' '):
            if word in con:
                con[word] = con[word] + 1
            else:
                con[word] = 1
        return con


class MesinCari:
    """Indeks dokumen + pencarian, mengikuti pemakaian panduan:
    tiap dokumen di-lowercase lalu di-concordance; kueri
    dibandingkan ke semua dokumen; hasil bukan-nol diurutkan
    menurun."""

    def __init__(self):
        self.v = VectorCompare()
        self.dokumen = {}   # id -> teks asli (untuk cuplikan)
        self.indeks = {}    # id -> concordance
        # Indeks terbalik (irisan 3, lanjutan di luar panduan):
        # kata -> himpunan id dokumen yang memuatnya.
        self.terbalik = {}
        # Diagnostik: berapa dokumen dibandingkan pada
        # pencarian terakhir (brute force vs indeks terbalik).
        self.jumlah_dibandingkan = 0

    def tambah(self, doc_id, teks):
        """Indeks (atau indeks ulang) satu dokumen."""
        if doc_id in self.indeks:
            # Indeks ulang: cabut postings versi lama dulu.
            for kata in self.indeks[doc_id]:
                self.terbalik[kata].discard(doc_id)
                if not self.terbalik[kata]:
                    del self.terbalik[kata]
        self.dokumen[doc_id] = teks
        self.indeks[doc_id] = self.v.concordance(teks.lower())
        for kata in self.indeks[doc_id]:
            self.terbalik.setdefault(kata, set()).add(doc_id)

    def cari(self, kueri):
        """Kembalikan [(skor, doc_id, cuplikan)] terurut skor
        menurun; cuplikan = 100 karakter pertama teks asli,
        persis seperti tampilan panduan."""
        q = self.v.concordance(kueri.lower())
        hasil = []
        for doc_id, con in self.indeks.items():
            skor = self.v.relation(q, con)
            if skor != 0:
                hasil.append((skor, doc_id, self.dokumen[doc_id][:100]))
        self.jumlah_dibandingkan = len(self.indeks)
        hasil.sort(key=lambda h: (-h[0], h[1]))
        return hasil

    def cari_cepat(self, kueri):
        """Sama seperti cari(), tetapi hanya dokumen yang
        berbagi minimal satu kata dengan kueri yang
        dibandingkan — sisanya pasti berelasi 0. Hasilnya
        identik dengan cari(); yang berbeda hanya jumlah
        perbandingannya (kelemahan CPU yang dicatat penulis
        panduan)."""
        q = self.v.concordance(kueri.lower())
        kandidat = set()
        for kata in q:
            kandidat |= self.terbalik.get(kata, set())
        hasil = []
        for doc_id in kandidat:
            skor = self.v.relation(q, self.indeks[doc_id])
            if skor != 0:
                hasil.append((skor, doc_id, self.dokumen[doc_id][:100]))
        self.jumlah_dibandingkan = len(kandidat)
        hasil.sort(key=lambda h: (-h[0], h[1]))
        return hasil

    # -- Lanjutan irisan 4 (di luar panduan): TF-IDF & boolean --

    def idf(self, kata):
        """Inverse document frequency: log(N / df). Kata yang
        ada di SEMUA dokumen berbobot 0 — ia tidak membedakan
        apa pun. Kata asing dianggap sejarang mungkin."""
        n = len(self.indeks)
        df = len(self.terbalik.get(kata, ()))
        if df:
            return math.log(n / df)
        return math.log(n) if n else 0.0

    def _bobot(self, concordance):
        """Terapkan bobot TF-IDF ke sebuah concordance."""
        return {kata: hitung * self.idf(kata)
                for kata, hitung in concordance.items()}

    def cari_tfidf(self, kueri):
        """Seperti cari(), tetapi vektor kueri dan dokumen
        dibobot TF-IDF dulu: kata langka menimbang lebih
        berat daripada kata pasaran. Menjawab kelemahan
        kualitas peringkat yang dicatat penulis panduan."""
        q = self._bobot(self.v.concordance(kueri.lower()))
        kandidat = set()
        for kata in self.v.concordance(kueri.lower()):
            kandidat |= self.terbalik.get(kata, set())
        hasil = []
        for doc_id in kandidat:
            skor = self.v.relation(q, self._bobot(self.indeks[doc_id]))
            if skor != 0:
                hasil.append((skor, doc_id, self.dokumen[doc_id][:100]))
        self.jumlah_dibandingkan = len(kandidat)
        hasil.sort(key=lambda h: (-h[0], h[1]))
        return hasil

    def cari_and(self, kueri):
        """Mode boolean AND (kelemahan pertama penulis
        panduan): hanya dokumen yang memuat SEMUA kata kueri
        yang lolos, lalu diperingkat dengan relation mentah."""
        kata = set(self.v.concordance(kueri.lower()))
        if not kata:
            return []
        kandidat = set.intersection(
            *[self.terbalik.get(w, set()) for w in kata])
        q = self.v.concordance(kueri.lower())
        hasil = []
        for doc_id in kandidat:
            skor = self.v.relation(q, self.indeks[doc_id])
            if skor != 0:
                hasil.append((skor, doc_id, self.dokumen[doc_id][:100]))
        self.jumlah_dibandingkan = len(kandidat)
        hasil.sort(key=lambda h: (-h[0], h[1]))
        return hasil
