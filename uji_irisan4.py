# Uji irisan 4 — TF-IDF & boolean AND: jangkar idf hitung
# tangan, pertukaran urutan mentah vs TF-IDF, kata di semua
# dokumen berbobot nol, dan penyaringan AND; plus regresi.
import math
import subprocess
import sys

from cari import buat_mesin
from mesincari import MesinCari

lulus = 0


def cek(nama, kondisi):
    global lulus
    assert kondisi, f"GAGAL: {nama}"
    lulus += 1
    print(f"  ok {lulus:2d}. {nama}")


def korpus_uji():
    m = MesinCari()
    m.tambah("d1", "kucing umum umum umum")
    m.tambah("d2", "kucing langka")
    m.tambah("d3", "umum biasa saja")
    m.tambah("d4", "umum umum biasa")
    return m


print("== idf: jangkar hitung tangan (N=4) ==")
m = korpus_uji()
cek("idf kata di 3 dari 4 dokumen = log(4/3)",
    abs(m.idf("umum") - math.log(4 / 3)) < 1e-15)
cek("idf kata di 2 dari 4 dokumen = log(2)",
    abs(m.idf("kucing") - math.log(2)) < 1e-15)
cek("idf kata di 1 dari 4 dokumen = log(4)",
    abs(m.idf("langka") - math.log(4)) < 1e-15)
m2 = MesinCari()
m2.tambah("a", "sama beda")
m2.tambah("b", "sama lain")
cek("kata di SEMUA dokumen: idf = log(1) = 0", m2.idf("sama") == 0.0)
cek("akibatnya kueri kata itu saja kosong di mode TF-IDF",
    m2.cari_tfidf("sama") == [] and len(m2.cari("sama")) == 2)

print("== TF-IDF menukar urutan yang mentah salah ==")
mentah = [h[1] for h in m.cari("kucing umum")]
tfidf = [h[1] for h in m.cari_tfidf("kucing umum")]
cek("mentah: d4 (cuma kata pasaran 'umum') di atas d2",
    mentah == ["d1", "d4", "d2", "d3"])
cek("tfidf: d2 (kata langka 'kucing') naik di atas d4",
    tfidf == ["d1", "d2", "d4", "d3"])
cek("kedua mode tetap menaruh d1 pertama & d3 terakhir",
    mentah[0] == tfidf[0] == "d1" and mentah[-1] == tfidf[-1] == "d3")

print("== boolean AND ==")
g = buat_mesin()
cek("AND 'captcha numbers': hanya dok 6 (dok 3 tak punya 'numbers')",
    [h[1] for h in g.cari_and("captcha numbers")] == [6])
cek("mode mentah kueri yang sama memberi dok 6 & 3 "
    "(6 menang: memuat kedua kata)",
    [h[1] for h in g.cari("captcha numbers")] == [6, 3])
cek("AND dengan kata asing -> kosong",
    g.cari_and("captcha zzztidakada") == [])
cek("AND satu kata == cari satu kata",
    g.cari_and("captcha") == g.cari("captcha"))
cek("AND peringkat di dalam lolos tetap skor mentah",
    g.cari_and("mysql backups")[0][1] == 2)

print("== mode bawaan tidak berubah oleh lanjutan ==")
cek("cari('captcha') di korpus panduan tetap nilai panduan",
    abs(g.cari("captcha")[0][0] - 0.124034734589) < 1e-12)

print("== regresi irisan 1-3 (subproses) ==")
for n in (1, 2, 3):
    r = subprocess.run([sys.executable, f"uji_irisan{n}.py"],
                       capture_output=True, text=True)
    cek(f"uji_irisan{n} hijau penuh", r.returncode == 0
        and "HIJAU" in r.stdout)

print(f"\nIRISAN 4 HIJAU: {lulus} pemeriksaan")
