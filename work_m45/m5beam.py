import sys, os; sys.path.insert(0, '../tools_m45')
from optimize import beam_legs2
from wad import read_map
from dbg import load
import sim
m = read_map('E1M5')
def L(pts, ul=(), rep=(), st=70, fa=False, **extra):
    wps = []
    for p in pts:
        d = dict(x=p[0], y=p[1], r=30)
        if len(p) > 2: d.update(p[2])
        if fa: d['fire_ahead'] = 1
        wps.append(d)
    kw = dict(max_tics=4000, m=m, uselines=set(ul), repeat_use=set(rep), stuck_tics=st)
    return (wps, kw)
STAGES = {
 'S2': [L([(870,200), (700,176)]), L([(500,176), (300,176)]), L([(215,185), (204,250), (178,300)]), L([(185,370), (205,431), (241,462)]),
        L([(404,508), (520,545)]), L([(700,600), (880,680)]), L([(1000,740), (1065,770)], st=200), L([(1070,830,{'r':20}), (980,880)], st=200), L([(780,870), (692,804,{'r':14})])],
 'S3': [L([(688,852,{'r':10})]), L([(876,884), (1012,884)]), L([(1052,836), (1052,772)]), L([(800,640), (468,524)]), L([(300,470), (241,462), (205,431)]), L([(185,370), (178,300), (204,250)]),
        L([(150,200), (60,150)]), L([(-64,290,{'r':20})], ul={476,477}), L([(-64,400), (-108,440)], ul={476,477}), L([(-256,800,{'r':12})]), L([(-556,780)]), L([(-612,830,{'r':16})], ul={157,158}), L([(-700,832)], ul={157,158})],
 'S4': [L([(-800,840), (-916,850)], st=150), L([(-1000,900), (-1092,1156)], st=150), L([(-1164,1180), (-1476,1204)]), L([(-1612,1156), (-1620,1100)]), L([(-1452,908), (-1150,832,{'r':10,'face':0,'facer':120})], ul={189}, rep={189})],
 'S5': [L([(-1460,908), (-1620,1092)]), L([(-1620,1148), (-1484,1204)]), L([(-1012,1212), (-996,1250,{'r':14})], st=260), L([(-900,1280,{'r':20})], ul={808,819}, st=260), L([(-836,1276)], ul={811,820}), L([(-748,1228)], ul={776})],
 'S6': [L([(-292,1212), (52,876)], ul={776}), L([(244,860), (492,860)]), L([(700,1060), (876,1116)]), L([(1188,1108), (1252,1052)]), L([(1436,1052), (1452,900)], ul={145,230,432,434}),
        L([(1476,892), (1548,892), (1564,916)], ul={145,230,432,434}), L([(1564,1372), (1532,1396)], ul={145,230}), L([(1460,1404), (972,1404)], ul={145,230}), L([(308,1340), (276,1300)]), L([(196,1044,{'r':14})])],
 'S7': [L([(124,1204), (108,1436)]), L([(12,1540), (12,1676)], ul={322,323}), L([(60,1732), (60,1812), (44,1836)], ul={322,323}), L([(-52,2276), (-140,2332)], ul={739,743,744,400,401}),
        L([(-244,2348), (-288,2460,{'r':10,'face':90,'facer':120})], ul={400,401,409}, rep={409})],
}
if __name__ == '__main__':
    stage, pre_file, n, beam, seed = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    pre = load(pre_file)
    legs = STAGES[stage]
    if stage != 'S7':
        legs = legs + [legs[-1]]  # last leg is re-run as 'final' (must exit) -> avoid: use dummy
    # beam_legs2 treats the last leg as exit leg; for non-final stages we run all legs as non-final by adding a sentinel
    import optimize
    out = f'm5b_{stage}.lmp'
    if stage == 'S7':
        best = beam_legs2(5, legs, n=n, beam=beam, jitter=12, seed=seed, out=out, prefix=pre, safe=True, final_n=n * 2)
    else:
        best = beam_legs2(5, legs[:-1] + [legs[-1]], n=n, beam=beam, jitter=12, seed=seed, out=out, prefix=pre, safe=True)
    print('DONE', stage, best[0] if best else None)
