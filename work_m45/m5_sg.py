import sys, random, time; sys.path.insert(0, '../tools_m45')
from follow import follow
from wad import read_map
import sim
m = read_map('E1M5')
n, seed = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(seed); t0 = time.time(); best = None
for k in range(n):
    j = (lambda s: rng.uniform(-s, s)) if k else (lambda s: 0)
    W = [dict(x=-148 + j(20), y=-36 + j(20), r=40), dict(x=210 + j(10), y=190 + j(10), r=30), dict(x=204, y=428, r=30), dict(x=320 + j(20), y=445, r=25),
         dict(x=320, y=380, r=20), dict(x=290, y=350, r=14)]
    tics, r = follow(5, W, max_tics=500, K=rng.choice([3, 4, 4, 5]) if k else 4, m=m, uselines={310, 312}, stop_at_end=True)
    ok = getattr(r, 'reached', False) and not r.dead
    print(k, 'ok', ok, 'tics', len(tics), 'pos', [round(v) for v in r.pos[-1][:3]] if r.pos else None, 'dead', r.dead, round(time.time() - t0), flush=True)
    if ok and (best is None or len(tics) < best):
        best = len(tics); sim.write_lmp(f'm5sg_{seed}.lmp', 5, tics)
print('BEST', best)
