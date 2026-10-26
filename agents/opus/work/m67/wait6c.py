import sys, json, random, math, time, pickle; sys.path.insert(0, '/race/opus/tools_m67')
import sim
from legs import hits
from follow import follow
from auto import plan
from wad import read_map
m = read_map('E1M6')
D='/race/opus/work/m67/'
NV = pickle.load(open(D+'nav6ov.pkl','rb'))
pre = json.load(open(D+'m6_A.json'))
END = int(sys.argv[1]); N = int(sys.argv[2]); seed = int(sys.argv[3]); HMAX = int(sys.argv[4])
rng = random.Random(seed)
t0=time.time()
RK=(1680,-1344); BK=(-1536,-1728)
good=[]
for k in range(N):
    t = list(pre)
    fire = rng.random() < 0.5
    while len(t) < END:
        d = rng.randint(10, 70)
        if rng.random() < 0.25: f, s, tu = 0, 0, 0
        else:
            f = rng.choice([50, 50, 30, 0, -30, -50]); s = rng.choice([50, 40, 0, -40, -50]); tu = rng.randint(-8, 8)
        for j in range(d):
            if len(t) >= END: break
            t.append((f, s, tu, 1 if fire else 0))
    r = sim.run(6, t)
    alive = all((p[5] & 0x7fff) < 7 for p in r.pos[len(pre):])
    if not alive: continue
    h = hits(r, 0)
    touched = any(abs(q[0]-RK[0])<40 and abs(q[1]-RK[1])<40 for q in r.pos[len(pre):])
    if h <= HMAX and not touched: good.append((h, t))
print('patterns', N, 'good', len(good), f'{time.time()-t0:.0f}s', flush=True)
good.sort(key=lambda g: g[0])
best=None
for h, t in good[:int(sys.argv[5])]:
    p = sim.run(6, t).pos[-1]
    try:
        W = plan('E1M6', p[:2], [(RK[0], RK[1], dict(r=16)), (560,-1060, dict(r=24)), (330,-880, dict(r=30))])
    except Exception as e:
        continue
    tt, rr = follow(6, W, prefix=t, max_tics=len(t)+400, K=4, m=m, uselines=set(), stop_at_end=True, stuck_tics=200, nav=NV)
    ok = not getattr(rr,'dead',False) and math.hypot(rr.pos[-1][0]-330, rr.pos[-1][1]+880) < 80
    msg = f'h {h} -> door tics {len(tt)} ok {ok} hits {hits(rr,0)}'
    if ok:
        W2 = plan('E1M6', (330,-880), [(BK[0], BK[1], dict(r=16))], overrides={151:(48,None)})
        t3, r3 = follow(6, W2, prefix=tt, max_tics=len(tt)+500, K=4, m=m, uselines={951}, stop_at_end=True, nav=NV)
        ok3 = not getattr(r3,'dead',False) and math.hypot(r3.pos[-1][0]-BK[0], r3.pos[-1][1]-BK[1]) < 60
        msg += f' -> blue tics {len(t3)} ok {ok3} hits {hits(r3,0)} last {[round(v) for v in r3.pos[-1][:2]]}'
        if ok3 and (best is None or len(t3) + 10*hits(r3,0) < best[0]):
            best = (len(t3) + 10*hits(r3,0), t3)
            json.dump(t3, open(D+f'm6_D_{seed}.json','w')); msg += ' BEST'
    print(msg, f'{time.time()-t0:.0f}s', flush=True)
