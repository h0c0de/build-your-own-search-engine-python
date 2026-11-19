# Uji irisan 2 — MesinCari + CLI: dua pencarian demo panduan
# end-to-end (urutan, nilai, cuplikan), perilaku tepi, dan CLI
# sebagai subproses.
import subprocess
import sys

from cari import DOKUMEN, buat_mesin
from mesincari import MesinCari

lulus = 0


def cek(nama, kondisi):
    global lulus
    assert kondisi, f"GAGAL: {nama}"
    lulus += 1
    print(f"  ok {lulus:2d}. {nama}")


print("== pencarian demo panduan, end-to-end ==")
mesin = buat_mesin()
hasil = mesin.cari("captcha")
cek("captcha: tepat dua hasil", len(hasil) == 2)
cek("captcha: urutan dok 3 lalu 6",
    [h[1] for h in hasil] == [3, 6])
cek("captcha: skor dok 3 = cetakan panduan",
    abs(hasil[0][0] - 0.124034734589) < 1e-12)
cek("captcha: skor dok 6 = cetakan panduan",
    abs(hasil[1][0] - 0.0957826285221) < 1e-12)
cek("cuplikan = 100 karakter pertama teks ASLI (bukan lowercase)",
    hasil[0][2] == DOKUMEN[3][:100] and hasil[0][2].startswith("Why You"))

hasil = mesin.cari("mysql stallman")
cek("mysql stallman: urutan dok 1 lalu 2",
    [h[1] for h in hasil] == [1, 2])
cek("mysql stallman: skor-skornya = cetakan panduan",
    abs(hasil[0][0] - 0.140028008403) < 1e-12
    and abs(hasil[1][0] - 0.110096376513) < 1e-12)

print("== perilaku mesin ==")
cek("kueri huruf besar sama hasilnya (lowercase di dalam)",
    [h[1] for h in mesin.cari("CAPTCHA")] == [3, 6])
cek("kueri tanpa padanan -> daftar kosong",
    mesin.cari("xyzqwerty") == [])
cek("mesin kosong -> daftar kosong", MesinCari().cari("a") == [])

m = MesinCari()
m.tambah("x", "satu dua")
m.tambah("x", "tiga empat")
cek("tambah id yang sama menimpa indeks lama",
    m.cari("satu") == [] and len(m.cari("tiga")) == 1)

print("== CLI sebagai subproses ==")
r = subprocess.run([sys.executable, "cari.py", "captcha"],
                   capture_output=True, text=True)
cek("CLI satu-tembak captcha: dua baris keluar",
    r.returncode == 0 and r.stdout.count("\n") == 2)
cek("CLI mencetak skor & cuplikan ala panduan",
    r.stdout.startswith("0.124034734589")
    and "Why You Shouldnt roll your own CAPTCHA" in r.stdout)
r = subprocess.run([sys.executable, "cari.py"],
                   input="mysql stallman\n\n",
                   capture_output=True, text=True)
cek("CLI interaktif via pipa stdin bekerja",
    r.returncode == 0 and "Richard Stallman to visit Australia" in r.stdout
    and r.stdout.index("Richard Stallman") < r.stdout.index("MySQL Backups"))

print("== regresi irisan 1 ==")
r = subprocess.run([sys.executable, "uji_irisan1.py"],
                   capture_output=True, text=True)
cek("uji_irisan1 hijau penuh", r.returncode == 0 and "HIJAU" in r.stdout)

print(f"\nIRISAN 2 HIJAU: {lulus} pemeriksaan")
