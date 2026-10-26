import sys, json, random, math, time; sys.path.insert(0, '/race/opus/tools_m67')
import sim
from legs import hits
from follow import follow
from auto import plan
from wad import read_map
m = read_map('E1M6')
D='/race/opus/work/m67/'
pre = json.load(open(D+'m6_A.json'))
END = int(sys.argv[1]); N = int(sys.argv[2]); seed = int(sys.argv[3])
rng = random.Random(seed)
best=None
t0=time.time()
RK=(1680,-1344)
for k in range(N):
    t = list(pre)
    fire = rng.random() < 0.6
    while len(t) < END:
        d = rng.randint(15, 60)
        f = rng.choice([50, 50, 30, 0, -30, -50]); s = rng.choice([50, 40, 0, -40, -50])
        tu = rng.randint(-8, 8)
        for j in range(d):
            if len(t) >= END: break
            t.append((f, s, tu, 1 if fire else 0))
    r = sim.run(6, t)
    alive = all((p[5] & 0x7fff) < 7 for p in r.pos[len(pre):])
    h = hits(r, len(pre))
    p = r.pos[-1]
    # did we touch the key already?
    touched = any(abs(q[0]-RK[0])<36 and abs(q[1]-RK[1])<36 for q in r.pos[len(pre):])
    msg = f'{k} alive {alive} hits {h} end {[round(v) for v in p[:2]]} key {touched}'
    if alive:
        try:
            W = plan('E1M6', p[:2], [(RK[0], RK[1], dict(r=16)), (560,-1060, dict(r=24)), (330,-880, dict(r=30))])
        except Exception as e:
            print(msg, 'noplan', e); continue
        tt, rr = follow(6, W, prefix=t, max_tics=len(t)+400, K=4, m=m, uselines=set(), stop_at_end=True, stuck_tics=200)
        ok = not getattr(rr,'dead',False) and math.hypot(rr.pos[-1][0]-330, rr.pos[-1][1]+880) < 80
        h2 = hits(rr, len(pre))
        msg += f' -> follow tics {len(tt)} ok {ok} hits {h2} last {[round(v) for v in rr.pos[-1][:2]]}'
        if ok and (best is None or (len(tt) + 10*h2) < best[0]):
            best = (len(tt) + 10*h2, tt)
            json.dump(tt, open(D+f'm6_W_{seed}.json','w'))
            msg += ' BEST'
    print(msg, f'{time.time()-t0:.0f}s', flush=True)
print('best', best[0] if best else None)
