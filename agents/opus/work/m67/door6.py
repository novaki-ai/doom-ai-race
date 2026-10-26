import sys, json, random, math, time, pickle; sys.path.insert(0, '/race/opus/tools_m67')
import sim
from legs import hits
from follow import follow
from auto import plan
from wad import read_map
m = read_map('E1M6')
D='/race/opus/work/m67/'
NV = pickle.load(open(D+'nav6ov.pkl','rb'))
OV = {151:(48,None)}
# prefix: start -> inside 186 near L206, stopping
try:
    pre = json.load(open(D+'m6_pre186.json'))
except Exception:
    W = plan('E1M6', (32,-1376), [(560,-1060, dict(r=30)), (640,-1170, dict(r=12, slow=4))], overrides=OV)
    pre, r = follow(6, W, prefix=[], max_tics=300, K=4, m=m, stop_at_end=True, nav=NV)
    json.dump(pre, open(D+'m6_pre186.json','w'))
r = sim.run(6, pre)
print('pre', len(pre), [round(v) for v in r.pos[-1][:2]], 'side', r.pos[-1][1]-(r.pos[-1][0]-1984), 'hits', hits(r,0))
def crossed(pos, a):
    for i in range(a, len(pos)):
        if pos[i][1] - (pos[i][0]-1984) < 0: return i
    return None
ws = list(range(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])))
for w in ws:
    t = pre + [(0,0,0,0)]*w
    W1 = [dict(x=780, y=-1300, r=20)]
    t1, r1 = follow(6, W1, prefix=t, max_tics=len(t)+40, K=4, m=m, stop_at_end=True)
    c = crossed(r1.pos, len(pre))
    if getattr(r1,'dead',False) or c is None:
        print(w, 'dead/nocross', getattr(r1,'dead',False), c); continue
    # go back to door after a delay so door would have closed
    t2 = t1 + [(0,0,0,0)]*20
    W2 = [dict(x=560, y=-1060, r=24), dict(x=330, y=-880, r=30)]
    t3, r3 = follow(6, W2, prefix=t2, max_tics=len(t2)+120, K=4, m=m, stop_at_end=True, stuck_tics=40)
    p = r3.pos[-1]
    ok = not getattr(r3,'dead',False) and math.hypot(p[0]-330, p[1]+880) < 80
    print(w, 'cross', c, 'back ok', ok, 'tics', len(t3), 'last', [round(v) for v in p[:2]], 'hits', hits(r3,0), flush=True)
    if ok:
        json.dump(t1, open(D+f'm6_doorok_{w}.json','w'))
