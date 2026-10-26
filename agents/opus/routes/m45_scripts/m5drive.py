import sys, random, time, os; sys.path.insert(0, '../tools_m45')
from follow import follow
from wad import read_map
from dbg import load
import sim
m = read_map('E1M5')
FA_ALL = bool(int(os.environ.get('FA_ALL', '0')))
def W_(pts, fa=False):
    out = []
    for p in pts:
        d = dict(x=p[0], y=p[1], r=30)
        if len(p) > 2: d.update(p[2])
        if fa and 'face' not in d: d['fire_ahead'] = 1
        out.append(d)
    return out
LEGS = {
 'L0': dict(pts=[(-300,-400,{'r':40}), (-416,-160,{'r':14}), (-148,-36,{'r':40}), (210,190), (204,428), (320,445,{'r':25}), (320,380,{'r':20}), (288,352,{'r':10})], ul={310,312}),
 'L1': dict(pts=[(320,425), (300,462), (241,462), (205,431), (185,370), (178,300), (204,250), (215,180), (430,176), (650,176), (870,190), (888,262,{'r':12})], ul={310,312}),
 'L2': dict(pts=[(870,200), (600,176), (300,176), (210,190), (204,250), (178,300), (185,370), (205,431), (241,462), (404,508), (520,545), (700,600), (880,680), (1000,740), (1065,770), (1070,830,{'r':20}), (980,880), (780,870), (692,804,{'r':14})], ul=set(), st=160),
 'L3': dict(pts=[(876,884), (1012,884), (1052,836), (1052,772), (468,524), (300,470), (241,462), (205,431), (185,370), (178,300), (204,250), (150,200), (60,150), (-64,290,{'r':20}), (-64,400), (-108,420), (-556,780), (-612,830,{'r':16})], ul={476,477,157,158}),
 'L4': dict(pts=[(-700,832), (-916,850), (-1000,900), (-1092,1156), (-1164,1180), (-1476,1204), (-1612,1156), (-1620,1100), (-1452,908), (-1150,832,{'r':10,'face':0,'facer':120})], ul={157,158,189}, rep={189}, st=160),
 'L5': dict(pts=[(-1460,908), (-1620,1092), (-1620,1148), (-1484,1204), (-1012,1212), (-996,1250,{'r':14}), (-900,1280,{'r':20})], ul={808,819}, st=260),
 'L6': dict(pts=[(-836,1276), (-748,1228), (-292,1212), (52,876), (244,860), (492,860), (700,1060), (876,1116), (1188,1108), (1252,1052), (1436,1052), (1452,900), (1476,892), (1548,892), (1564,916), (1564,1372), (1532,1396), (1460,1404), (972,1404), (308,1340), (276,1300), (196,1044,{'r':14})], ul={808,819,811,820,776,145,230,432,434}),
 'L7': dict(pts=[(124,1204), (108,1436), (12,1540), (12,1676), (60,1732), (60,1812), (44,1836), (-52,2276), (-140,2332), (-244,2348), (-288,2460,{'r':10,'face':90,'facer':120})], ul={322,323,400,401,739,743,744,409}, rep={409}, last=True),
}
def do_leg(name, pre, n, seed, jit=15, tlimit=200, fa=False):
    L = LEGS[name]; rng = random.Random(seed); t0 = time.time(); best = None
    for k in range(n):
        if time.time() - t0 > tlimit: break
        pts = []
        for i, p in enumerate(L['pts']):
            p = list(p)
            if k and i < len(L['pts']) - 1:
                p[0] += rng.uniform(-jit, jit); p[1] += rng.uniform(-jit, jit)
            pts.append(tuple(p))
        W = W_(pts, fa=fa and (k % 2 == 1 or FA_ALL))
        last = L.get('last', False)
        tics, r = follow(5, W, prefix=pre, max_tics=len(pre) + 1500, K=rng.choice([3, 4, 4, 5]) if k else 4, m=m, uselines=set(L['ul']), repeat_use=set(L.get('rep', ())), stop_at_end=not last, stuck_tics=L.get('st', 70))
        ok = (r.exit_time is not None) if last else (getattr(r, 'reached', False) and not r.dead)
        key = r.exit_time if last else len(tics)
        print(name, k, 'ok', ok, 'tics', len(tics), 'exit', r.exit_time, 'pos', [round(v) for v in r.pos[-1][:3]] if r.pos else None, 'dead', r.dead, round(time.time() - t0), flush=True)
        if ok:
            sim.write_lmp(f'm5_{name}_ok{k}_s{seed}.lmp', 5, tics)
        if ok and (best is None or key < best[0]):
            best = (key, tics)
            sim.write_lmp(f'm5_{name}_best.lmp', 5, tics)
    return best
if __name__ == '__main__':
    name, pre_file, n, seed = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    fa = len(sys.argv) > 5 and sys.argv[5] == 'fa'
    pre = load(pre_file) if pre_file != '-' else []
    b = do_leg(name, pre, n, seed, fa=fa)
    print('BEST', name, b[0] if b else None)
