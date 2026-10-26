import sys, random, time; sys.path.insert(0, '../tools_m45')
from follow import follow
from wad import read_map
import sim
m = read_map('E1M5')
n, seed = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(seed); t0 = time.time(); best = None
for k in range(n):
    s1 = rng.choice([150, 200]); s2 = 350 - s1
    xs = rng.uniform(600, 800)
    W = [dict(x=-148 + rng.uniform(-20, 20), y=-36 + rng.uniform(-20, 20), r=40), dict(x=430, y=s1, r=30), dict(x=xs, y=s1, r=30),
         dict(x=xs + 70, y=s2, r=30), dict(x=870 + rng.uniform(-20, 20), y=rng.choice([150, 200]), r=30), dict(x=888, y=262, r=12)]
    tics, r = follow(5, W, max_tics=400, K=rng.choice([3, 4, 4, 5]), m=m, uselines=set(), stop_at_end=True)
    ok = getattr(r, 'reached', False) and not r.dead
    print(k, 'ok', ok, 'tics', len(tics), 'pos', [round(v) for v in r.pos[-1][:2]] if r.pos else None, 'dead', r.dead, 's1', s1, 'xs', round(xs), round(time.time() - t0), flush=True)
    if ok and (best is None or len(tics) < best):
        best = len(tics); sim.write_lmp(f'm5L1_{seed}.lmp', 5, tics)
print('BEST', best)
