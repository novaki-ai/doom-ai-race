import sys; sys.path.insert(0, '../tools')
from auto import plan
from wad import read_map
from optimize import beam_legs
m = read_map('E1M1')
# legs end well past doors (a new leg forgets which doors were already used)
L1 = plan('E1M1', (1056, -3616), [(1700, -2530)])
L2 = plan('E1M1', (1700, -2530), [(2972, -3600)])
L3 = plan('E1M1', (2972, -3600), [(3004, -4250)])
L4 = plan('E1M1', (3004, -4250), [(2950, -4768, dict(face=180, facer=100, r=10))])
for L in (L1, L2, L3, L4): print([(round(w['x']), round(w['y'])) for w in L])
kw = dict(max_tics=700, m=m, uselines={151, 152, 340, 341, 324, 325, 330}, repeat_use={330})
n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
best = beam_legs(1, [L1, L2, L3, L4], n=n, beam=3, jitter=20, follow_kw=kw, seed=int(sys.argv[2]) if len(sys.argv) > 2 else 3, out='e1m1_beam.lmp', final_n=n * 2)
print('BEST', best[0] if best else None)
