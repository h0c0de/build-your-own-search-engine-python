# Uji irisan 1 — inti VectorCompare: concordance, magnitude,
# relation; jangkar hitung tangan + empat nilai cetak panduan
# pada tujuh dokumen blog penulisnya.
import math

from mesincari import VectorCompare

v = VectorCompare()
lulus = 0


def cek(nama, kondisi):
    global lulus
    assert kondisi, f"GAGAL: {nama}"
    lulus += 1
    print(f"  ok {lulus:2d}. {nama}")


print("== concordance ==")
cek("hitungan kata dasar",
    v.concordance("kucing makan ikan kucing")
    == {'kucing': 2, 'makan': 1, 'ikan': 1})
cek("peka huruf besar (lowercase urusan pemanggil)",
    v.concordance("Kata kata") == {'Kata': 1, 'kata': 1})
cek("keanehan setia panduan: spasi ganda melahirkan kata ''",
    v.concordance("a  b") == {'a': 1, '': 1, 'b': 1})
try:
    v.concordance(123)
    cek("concordance non-string -> ValueError", False)
except ValueError as e:
    cek("concordance non-string -> ValueError",
        str(e) == 'Supplied Argument should be of type string')

print("== magnitude ==")
cek("magnitude {'a':2,'b':1} = akar 5",
    v.magnitude({'a': 2, 'b': 1}) == math.sqrt(5))
cek("magnitude dokumen 3 kata unik = akar 3",
    v.magnitude(v.concordance("satu dua tiga")) == math.sqrt(3))
cek("magnitude concordance kosong = 0", v.magnitude({}) == 0)
try:
    v.magnitude("bukan dict")
    cek("magnitude non-dict -> ValueError", False)
except ValueError:
    cek("magnitude non-dict -> ValueError", True)

print("== relation: kosinus hitung tangan ==")
cek("dokumen identik -> 1.0 (sampai galat apung: 3/(akar3*akar3))",
    abs(v.relation(v.concordance("a b c"), v.concordance("a b c")) - 1.0)
    < 1e-12)
cek("tak berbagi kata -> 0",
    v.relation(v.concordance("a b"), v.concordance("c d")) == 0)
cek("satu kata bersama: 1/akar(6)",
    abs(v.relation(v.concordance("kucing makan ikan"),
                   v.concordance("kucing minum"))
        - 1 / math.sqrt(6)) < 1e-15)
cek("simetris: relation(a,b) = relation(b,a)",
    v.relation(v.concordance("x y y z"), v.concordance("y z w"))
    == v.relation(v.concordance("y z w"), v.concordance("x y y z")))
cek("vektor kosong -> 0 (penjaga bagi-nol)",
    v.relation({}, v.concordance("a")) == 0)
try:
    v.relation([], {})
    cek("relation argumen 1 non-dict -> ValueError", False)
except ValueError as e:
    cek("relation argumen 1 non-dict -> ValueError",
        str(e) == 'Supplied Argument 1 should be of type dict')
try:
    v.relation({}, [])
    cek("relation argumen 2 non-dict -> ValueError", False)
except ValueError as e:
    cek("relation argumen 2 non-dict -> ValueError",
        str(e) == 'Supplied Argument 2 should be of type dict')

print("== jangkar emas: nilai cetak panduan, 7 dokumen penulis ==")
DOKUMEN = {
 0: "At Scale You Will Hit Every Performance Issue I used to think I knew a bit about performance scalability and how to keep things trucking when you hit large amounts of data Truth is I know diddly squat on the subject since the most I have ever done is read about how its done To understand how I came about realising this you need some background",
 1: "Richard Stallman to visit Australia Im not usually one to promote events and the like unless I feel there is a genuine benefit to be had by attending but this is one stands out Richard M Stallman the guru of Free Software is coming Down Under to hold a talk You can read about him here Open Source Celebrity to visit Australia",
 2: "MySQL Backups Done Easily One thing that comes up a lot on sites like Stackoverflow and the like is how to backup MySQL databases The first answer is usually use mysqldump This is all fine and good till you start to want to dump multiple databases You can do this all in one like using the all databases option however this makes restoring a single database an issue since you have to parse out the parts you want which can be a pain",
 3: "Why You Shouldnt roll your own CAPTCHA At a TechEd I attended a few years ago I was watching a presentation about Security presented by Rocky Heckman read his blog its quite good In it he was talking about security algorithms The part that really stuck with me went like this",
 4: "The Great Benefit of Test Driven Development Nobody Talks About The feeling of productivity because you are writing lots of code Think about that for a moment Ask any developer who wants to develop why they became a developer One of the first things that comes up is I enjoy writing code This is one of the things that I personally enjoy doing Writing code any code especially when its solving my current problem makes me feel productive It makes me feel like Im getting somewhere Its empowering",
 5: "Setting up GIT to use a Subversion SVN style workflow Moving from Subversion SVN to GIT can be a little confusing at first I think the biggest thing I noticed was that GIT doesnt have a specific workflow you have to pick your own Personally I wanted to stick to my Subversion like work-flow with a central server which all my machines would pull and push too Since it took a while to set up I thought I would throw up a blog post on how to do it",
 6: "Why CAPTCHA Never Use Numbers 0 1 5 7 Interestingly this sort of question pops up a lot in my referring search term stats Why CAPTCHAs never use the numbers 0 1 5 7 Its a relativity simple question with a reasonably simple answer Its because each of the above numbers are easy to confuse with a letter See the below",
}
indeks = {i: v.concordance(d.lower()) for i, d in DOKUMEN.items()}

JANGKAR = [("captcha", 3, 0.124034734589),
           ("captcha", 6, 0.0957826285221),
           ("mysql stallman", 1, 0.140028008403),
           ("mysql stallman", 2, 0.110096376513)]
for kueri, dok, cetak in JANGKAR:
    nilai = v.relation(v.concordance(kueri.lower()), indeks[dok])
    cek(f"kueri {kueri!r} dok {dok} = cetakan {cetak}",
        abs(nilai - cetak) < 1e-12)

cek("kueri 'captcha' hanya mengenai dok 3 & 6",
    [i for i in range(7)
     if v.relation(v.concordance("captcha"), indeks[i]) != 0] == [3, 6])

print(f"\nIRISAN 1 HIJAU: {lulus} pemeriksaan")
