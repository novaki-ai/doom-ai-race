import sys; sys.path.insert(0, '../tools')
from follow import follow
from auto import plan
from wad import read_map
import sim
m = read_map('E1M1')
W = plan('E1M1', (1056, -3616), [(2950, -4768, dict(face=180, facer=100, r=10))])
print([(round(w['x']), round(w['y'])) for w in W])
tics, res = follow(1, W, max_tics=1500, K=4, verbose=False, m=m, uselines={151, 152, 340, 341, 324, 325, 330}, repeat_use={330})
print('tics', len(tics), 'exit', res.exit_time, 'last', res.pos[-1] if res.pos else None)
sim.write_lmp('e1m1_try.lmp', 1, tics)
