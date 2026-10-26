"""İnsan kuralını rekor demolarından ölçer (referans videodaki "mikrofon tıklaması" yönteminin Doom karşılığı).
Girdi: DSDA arşivinden E1M1–E1M8 UV-Speed rekor demoları + bölüm rekoru (rekor/ham/). Çıktı: olcum.json.
Ölçülen: hareket değerleri, tic başına en büyük dönüş, saniyede ve 10 sn'de yeni ateş/kullan basışı, dönüş yönü değişimi."""
import glob, json, os, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lmp import oku
R = "/race/human-records"
ATES, KULLAN = 1, 2  # BT_ATTACK, BT_USE (bit 2 = BT_CHANGE, 3-5 silah)

def pencere_en(olay, uzunluk):
    en = 0; j = 0
    for i in range(len(olay)):
        while olay[i] - olay[j] >= uzunluk: j += 1
        en = max(en, i - j + 1)
    return en

sonuc = {}
for yol in sorted(glob.glob(os.path.join(R, "**", "*.lmp"), recursive=True)):
    bas, t, dip = oku(yol)
    ad = os.path.basename(yol)
    ileri = Counter(x[0] for x in t); yan = Counter(x[1] for x in t)
    donus = [abs(x[2]) for x in t]
    yeni = {}
    for bit, isim in ((ATES, "ates"), (KULLAN, "kullan")):
        ol = [i for i in range(len(t)) if t[i][3] & bit and not (t[i][3] & 2 << 0 if False else False) and (i == 0 or not t[i - 1][3] & bit)]
        # BT_CHANGE (4) tic'lerinde düğme baytı silah değişimi taşır; ateş/kullan bitleri yine geçerli
        yeni[isim] = dict(toplam=len(ol), en_1sn=pencere_en(ol, 35), en_10sn=pencere_en(ol, 350),
                          en_kisa_aralik=min((b - a for a, b in zip(ol, ol[1:])), default=None))
    yon = [1 if x[2] > 0 else -1 if x[2] < 0 else 0 for x in t]
    degisim = []; son = 0
    for i, y in enumerate(yon):
        if y and son and y != son: degisim.append(i)
        if y: son = y
    sonuc[ad] = dict(surum=bas["surum"], harita=f"E{bas['bolum']}M{bas['harita']}", tic=len(t), ileri=dict(sorted(ileri.items())),
                     yan=dict(sorted(yan.items())), donus_en=max(donus), donus_99=sorted(donus)[int(len(donus) * .99)],
                     donus_yon_degisimi_en_1sn=pencere_en(degisim, 35), **yeni, dipnot=dip[:160])
json.dump(sonuc, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "olcum.json"), "w"), ensure_ascii=False, indent=1)
for k, v in sonuc.items():
    print(f"{k:16} {v['harita']} v{v['surum']} {v['tic']:>5} tic · ileri {list(v['ileri'])} · yan {list(v['yan'])} · dönüş en {v['donus_en']} (%99 {v['donus_99']}) · "
          f"yön değ/sn {v['donus_yon_degisimi_en_1sn']} · ateş {v['ates']} · kullan {v['kullan']}")
