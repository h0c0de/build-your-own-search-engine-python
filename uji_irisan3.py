# Uji irisan 3 — indeks terbalik: hasil cari_cepat IDENTIK
# dengan brute force cari() pada korpus panduan dan korpus
# acak 500 dokumen; penghematan perbandingan terhitung.
import random
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


print("== postings pada korpus panduan ==")
mesin = buat_mesin()
cek("postings 'captcha' = {3, 6}", mesin.terbalik['captcha'] == {3, 6})
cek("postings 'the' memuat banyak dokumen",
    len(mesin.terbalik['the']) >= 5)

print("== identik di korpus panduan ==")
for kueri in ["captcha", "mysql stallman", "git workflow",
              "the", "zzztidakada", "code code code"]:
    cek(f"cari_cepat == cari untuk {kueri!r}",
        mesin.cari_cepat(kueri) == mesin.cari(kueri))

print("== identik di korpus acak 500 dokumen ==")
rng = random.Random(20261120)
kosakata = [f"kata{i}" for i in range(60)] + \
    ["kucing", "anjing", "makan", "tidur", "lari"]
m = MesinCari()
for i in range(500):
    n = rng.randint(5, 60)
    m.tambah(i, ' '.join(rng.choice(kosakata) for _ in range(n)))
semua_sama = True
for _ in range(40):
    kueri = ' '.join(rng.choice(kosakata + ["luar", "kosakata"])
                     for _ in range(rng.randint(1, 3)))
    if m.cari_cepat(kueri) != m.cari(kueri):
        semua_sama = False
        print("    BEDA pada kueri:", kueri)
cek("40 kueri acak: hasil cepat identik brute force", semua_sama)

print("== penghematan perbandingan ==")
m.cari("kucing")
cek("brute force membandingkan semua 500", m.jumlah_dibandingkan == 500)
hasil = m.cari_cepat("kucing")
cek("indeks terbalik membandingkan jauh lebih sedikit",
    0 < m.jumlah_dibandingkan < 250)
cek("jumlah dibandingkan = jumlah dokumen berkandidat",
    m.jumlah_dibandingkan == len(m.terbalik['kucing']))
m.cari_cepat("luar kosakata")
cek("kata di luar kosakata: 0 perbandingan",
    m.jumlah_dibandingkan == 0)

print("== indeks ulang menjaga postings ==")
m2 = MesinCari()
m2.tambah("d", "apel jeruk")
m2.tambah("d", "mangga")
cek("postings kata lama tercabut",
    'apel' not in m2.terbalik and m2.terbalik['mangga'] == {'d'})
cek("hasil pencarian mengikuti versi terbaru",
    m2.cari_cepat("apel") == [] and len(m2.cari_cepat("mangga")) == 1)

print("== regresi irisan 1-2 ==")
for n in (1, 2):
    r = subprocess.run([sys.executable, f"uji_irisan{n}.py"],
                       capture_output=True, text=True)
    cek(f"uji_irisan{n} hijau penuh", r.returncode == 0
        and "HIJAU" in r.stdout)

print(f"\nIRISAN 3 HIJAU: {lulus} pemeriksaan")
