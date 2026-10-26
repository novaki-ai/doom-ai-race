import sys, json, random, math, time; sys.path.insert(0, '/race/opus/tools_m67')
import sim
from legs import hits
D='/race/opus/work/m67/'
pre = json.load(open(D+(sys.argv[4] if len(sys.argv)>4 else 'm6_A.json')))
END = int(sys.argv[1]) if len(sys.argv)>1 else 1100
N = int(sys.argv[2]) if len(sys.argv)>2 else 60
seed = int(sys.argv[3]) if len(sys.argv)>3 else 1
rng = random.Random(seed)
best=None
t0=time.time()
for k in range(N):
    t = list(pre)
    fire = rng.random() < 0.5
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
    if alive and (best is None or h < best[0]):
        best = (h, t, p[:2])
        json.dump(t, open(D+f'm6_wait_{seed}.json','w'))
    print(k, 'alive', alive, 'hits', h, 'end', [round(v) for v in p[:2]], 'fire', fire, f'{time.time()-t0:.0f}s', flush=True)
print('best', best[0] if best else None, best[2] if best else None)
