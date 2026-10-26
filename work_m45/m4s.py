import sys, random, time; sys.path.insert(0, '../tools_m45')
from follow import follow
from wad import read_map
from dbg import load
import sim
m = read_map('E1M4')
pre_file, cut, n, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
prefix = load(pre_file)[:cut]
rng = random.Random(seed)
best = None
t0 = time.time()
for k in range(n):
    EX = rng.uniform(-140, -70); EY = rng.uniform(1870, 1930); NY = rng.uniform(1975, 2015); RY = rng.uniform(1870, 1905)
    W = [dict(x=-535 + rng.uniform(-15, 15), y=1900 + rng.uniform(-30, 30), r=40), dict(x=-500 + rng.uniform(-20, 20), y=NY, r=40),
         dict(x=EX, y=NY, r=40), dict(x=EX, y=EY, r=30),
         dict(x=-560, y=RY, r=30), dict(x=-900, y=1888, r=30), dict(x=-1300, y=1888, r=30), dict(x=-1440, y=1888, r=20),
         dict(x=-1570, y=1888, r=10, face=180, facer=100)]
    tics, res = follow(4, W, prefix=prefix, max_tics=800, K=4, m=m, uselines={648, 649, 468, 469, 547, 548, 554}, repeat_use={554})
    far = min(p[0] for p in res.pos) if res.pos else None
    print(k, 'exit', res.exit_time, 'dead', getattr(res, 'dead', None), 'tics', len(tics), 'minx', round(far) if far else None, 'EX', round(EX), 'EY', round(EY), 'NY', round(NY), 'RY', round(RY), round(time.time() - t0), flush=True)
    if res.exit_time and (best is None or res.exit_time < best):
        best = res.exit_time
        sim.write_lmp(f'm4s_best_{seed}.lmp', 4, tics)
print('BEST', best)
