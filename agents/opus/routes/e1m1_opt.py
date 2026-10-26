import sys; sys.path.insert(0, '../tools')
from auto import plan
from wad import read_map
from optimize import search
m = read_map('E1M1')
W = plan('E1M1', (1056, -3616), [(2950, -4768, dict(face=180, facer=100, r=10))])
kw = dict(max_tics=700, K=4, m=m, uselines={151, 152, 340, 341, 324, 325, 330}, repeat_use={330})
best = search(1, W, n=int(sys.argv[1]) if len(sys.argv) > 1 else 60, jitter=28, follow_kw=kw, out='e1m1_best.lmp', seed=int(sys.argv[2]) if len(sys.argv) > 2 else 1, best_time=14.37)
print('BEST', best[0] if best else None)
