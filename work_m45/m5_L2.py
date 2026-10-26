import sys, random, time; sys.path.insert(0, '../tools_m45')
from follow import follow
from wad import read_map
from dbg import load
import sim
m = read_map('E1M5')
pre = load(sys.argv[1]); n, seed = int(sys.argv[2]), int(sys.argv[3]); out = sys.argv[4]
rng = random.Random(seed); t0 = time.time(); best = None
P = [(860, 200), (600, 176), (300, 176), (210, 190), (204, 428), (404, 508), (520, 545), (700, 600), (880, 680), (1000, 740), (1065, 770)]
for k in range(n):
    W = [dict(x=x + (rng.uniform(-15, 15) if k else 0), y=y + (rng.uniform(-15, 15) if k else 0), r=30) for x, y in P]
    W += [dict(x=1070, y=830, r=20), dict(x=980, y=880, r=30), dict(x=780, y=870, r=30), dict(x=692, y=804, r=14)]
    tics, r = follow(5, W, prefix=pre, max_tics=700, K=rng.choice([3, 4, 4, 5]) if k else 4, m=m, uselines=set(), stop_at_end=True, stuck_tics=150)
    ok = getattr(r, 'reached', False) and not r.dead
    print(k, 'ok', ok, 'tics', len(tics), 'pos', [round(v) for v in r.pos[-1][:3]] if r.pos else None, 'dead', r.dead, round(time.time() - t0), flush=True)
    if ok and (best is None or len(tics) < best):
        best = len(tics); sim.write_lmp(out, 5, tics)
print('BEST', best)
