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
    RY = rng.choice([1848, 1856, 1888, 1920, 1928]) + rng.uniform(-4, 4)
    j = lambda s: rng.uniform(-s, s)
    W = [dict(x=-505 + j(15), y=1630 + j(20), r=30), dict(x=-330 + j(30), y=1475 + j(20), r=40), dict(x=-90 + j(10), y=1520 + j(20), r=40),
         dict(x=-85 + j(8), y=RY - 40 + j(10), r=30), dict(x=-300, y=RY, r=30), dict(x=-700, y=RY, r=30), dict(x=-1100, y=RY + (1888 - RY) * 0.5, r=30),
         dict(x=-1300, y=1888, r=30), dict(x=-1440, y=1888, r=20), dict(x=-1570, y=1888, r=10, face=180, facer=100)]
    tics, res = follow(4, W, prefix=tA, max_tics=750, K=4, m=m, uselines=UL, repeat_use={554})
    minx = min(p[0] for p in res.pos[350:]) if len(res.pos) > 350 else None
    print(k, 'exit', res.exit_time, 'dead', getattr(res, 'dead', None), 'tics', len(tics), 'minx', round(minx) if minx else None, 'RY', round(RY), round(time.time() - t0), flush=True)
    if res.exit_time and (best is None or res.exit_time < best):
        best = res.exit_time
        sim.write_lmp(f'm4g_best_{seed}.lmp', 4, tics)
print('BEST', best)
