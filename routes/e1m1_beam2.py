import sys; sys.path.insert(0, '../tools')
from auto import plan
from wad import read_map
from optimize import beam_legs
m = read_map('E1M1')
pts = [(1056, -3616), (1290, -2760), (1700, -2530), (2560, -2660), (2960, -3100), (2975, -3700), (3004, -4250)]
legs = [plan('E1M1', a, [b]) for a, b in zip(pts, pts[1:])]
legs.append(plan('E1M1', pts[-1], [(2950, -4768, dict(face=180, facer=100, r=10))]))
for L in legs: print([(round(w['x']), round(w['y'])) for w in L])
from nav import Nav
kw = dict(max_tics=700, nav=Nav('E1M1'), m=m, uselines={151, 152, 340, 341, 324, 325, 330}, repeat_use={330})
n = int(sys.argv[1]) if len(sys.argv) > 1 else 12
best = beam_legs(1, legs, n=n, beam=4, jitter=16, follow_kw=kw, seed=int(sys.argv[2]) if len(sys.argv) > 2 else 5, out='e1m1_beam2.lmp', final_n=n * 2)
print('BEST', best[0] if best else None)
