import sys, math, time, json, os; sys.path.insert(0, '/race/opus/tools_m67')
from legs import run_leg
from auto import plan
from wad import read_map
import sim
D='/race/opus/work/m67/'
m = read_map('E1M6')
nbr = {i:set() for i in range(len(m.sectors))}
for fs,bs in m.lsec:
    if fs>=0 and bs>=0: nbr[fs].add(bs); nbr[bs].add(fs)
def opened(sec):
    c = min(m.sectors[n][1] for n in nbr[sec] if n!=sec)
    return (None, c-4)
OV = {151:(48,None), 37:opened(37), 28:opened(28), 242:opened(242)}
BK=(-1536,-1728); YK=(1088,-608); RK=(1680,-1344)
LEGS = {
 'A': ((32,-1376), [(760,-1290, dict(r=20))], set()),
 'B': ((760,-1290), [(RK[0], RK[1], dict(r=16))], set()),
 'C': (RK, [(560,-1080, dict(r=20))], set()),
 'C2': ((1710,-1280), [(560,-1060, dict(r=24)), (330,-880, dict(r=30))], set()),
 'D': ((376,-902), [(BK[0], BK[1], dict(r=16))], {951}),
 'E': (BK, [(-1176,-1736, dict(r=6, hard=True)), (-352,-1480, dict(r=10)), (-352,-1385, dict(r=16)), (1250,-256, dict(r=20))], {935, 121}),
 'F': ((1250,-256), [(YK[0], YK[1], dict(r=16))], {1119, 1139}),
 'Fb': ((1274,-254), [(1640,-192, dict(r=12, hard=True)), (1830,-192, dict(r=30, hard=True)), (2605,-2180, dict(r=14, hard=True)), (2624, -2250, dict(r=12, face=270, facer=80))], {975, 438}),
 'Gb': ((2624,-2250), [(2400,-1660, dict(r=14)), (2400,-1470, dict(r=16)), (YK[0], YK[1], dict(r=16))], set()),
 'Hb': (YK, [(-64, 2330, dict(r=12, face=90, facer=80))], {976, 890, 822}),
 'Hs': (YK, [(992,-740, dict(r=12, hard=True)), (992,-830, dict(r=14, hard=True)), (870,-885, dict(r=14, hard=True)), (800,-820, dict(r=14, hard=True)), (800,-600, dict(r=20)), (-64, 2330, dict(r=12, face=90, facer=80))], {1122, 1138, 890}),
 'Hb1': (YK, [(1960,-960, dict(r=14, hard=True)), (1790,-192, dict(r=12, hard=True)), (1560,-192, dict(r=30, hard=True))], {976}),
 'Hb2': ((1560,-192), [(-64, 2330, dict(r=12, face=90, facer=80))], {890, 822}),
 'G': (YK, [(-64, 2330, dict(r=12, face=90, facer=80))], {890, 822}),
 'Z2': ((-64,2280), [(-64, 2346, dict(r=8, face=90, facer=90, hard=True, use=True, user=70)), (100, 2330, dict(r=14, hard=True)), (-30, 1790, dict(r=20, hard=True)), (-50, 1560, dict(r=24, hard=True)), (-500, 1440, dict(r=12, hard=True)), (-450, 1010, dict(r=14, hard=True)), (-950, 1295, dict(r=12, hard=True)), (-1530, 1300, dict(r=12, hard=True)), (-1500, 1384, dict(r=24, face=0, facer=90)), (-1780, 1350, dict(r=14, hard=True)), (-1930, 2016, dict(r=10, face=0, facer=100))], {822, 599, 614, 627}),
 'Z': ((-64,2280), [(-64, 2346, dict(r=8, face=90, facer=90, hard=True, use=True, user=70)), (-30, 1790, dict(r=20, hard=True)), (-50, 1560, dict(r=24, hard=True)), (-950, 1295, dict(r=12, hard=True)), (-1530, 1300, dict(r=12, hard=True)), (-1500, 1384, dict(r=24, face=0, facer=90)), (-1780, 1350, dict(r=14, hard=True)), (-1930, 2016, dict(r=10, face=0, facer=100))], {822, 599, 614, 627}),
}
def load(name):
    return json.load(open(D+'m6_'+name+'.json'))
def main():
    leg = sys.argv[1]; prev = sys.argv[2] if len(sys.argv) > 2 else None
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    prefix = load(prev) if prev else []
    st, goals, ul = LEGS[leg]
    ov = dict(OV)
    if leg.startswith('Hb'):
        ov[191] = (None, m.sectors[191][0]); ov[214] = (None, m.sectors[214][0])
    W = plan('E1M6', st, goals, overrides=ov)
    print('W', [(round(w['x']), round(w['y'])) for w in W])
    import pickle
    from nav import Nav
    try: NV = pickle.load(open(D+'nav6ov2.pkl','rb'))
    except Exception:
        NV = Nav('E1M6', OV); pickle.dump(NV, open(D+'nav6ov2.pkl','wb'))
    best = run_leg(6, m, prefix, W, ul, n=n, final=(leg=='Z'), nav=NV, seed=int(sys.argv[4]) if len(sys.argv)>4 else 1, hit_w=40)
    if best:
        json.dump(best[1], open(D+'m6_'+leg+'.json','w'))
        print('saved', leg, len(best[1]))
if __name__ == "__main__": main()
