import sys, math, random, time; sys.path.insert(0, '../tools_m45')
from m4e import m, UL
from follow import follow
from dbg import load
import sim
tA = load('m4e_A.lmp')
n, seed = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(seed)
best = None; t0 = time.time()
for k in range(n):
    j = lambda s: rng.uniform(-s, s)
    UX = rng.uniform(-200, -60); NY = 2000 + j(25)
    W = [dict(x=-540 + j(15), y=1930 + j(25), r=40), dict(x=-480 + j(20), y=NY, r=40), dict(x=UX, y=NY + j(15), r=40),
         dict(x=-470 + j(20), y=1945 + j(8), r=30), dict(x=-590, y=1905 + j(10), r=30), dict(x=-800, y=1888, r=30),
         dict(x=-1300, y=1888, r=30), dict(x=-1440, y=1888, r=20), dict(x=-1570, y=1888, r=10, face=180, facer=100)]
    tics, res = follow(4, W, prefix=tA, max_tics=700, K=4, m=m, uselines=UL, repeat_use={554})
    minx = min(p[0] for p in res.pos[350:]) if len(res.pos) > 350 else None
    print(k, 'exit', res.exit_time, 'dead', getattr(res, 'dead', None), 'tics', len(tics), 'minx', round(minx) if minx else None, 'UX', round(UX), round(time.time() - t0), flush=True)
    if res.exit_time and (best is None or res.exit_time < best):
        best = res.exit_time
        sim.write_lmp(f'm4h_best_{seed}.lmp', 4, tics)
print('BEST', best)
