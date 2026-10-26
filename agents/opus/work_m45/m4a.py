import sys; sys.path.insert(0, '../tools_m45')
from follow import follow
from auto import plan
from wad import read_map
import sim
m = read_map('E1M4')
W = plan('E1M4', (2032, 1120), [(-1570, 1888, dict(face=180, facer=100, r=10))], overrides={52:(184,None)})
print([(round(w['x']), round(w['y'])) for w in W])
tics, res = follow(4, W, max_tics=1500, K=4, m=m, uselines={648, 649, 468, 469, 547, 548, 554}, repeat_use={554}, verbose=True)
print(len(tics), res.exit_time, getattr(res, 'dead', None))
for i in range(0, len(res.pos), 10): print(i, [round(v) for v in res.pos[i][:4]])
sim.write_lmp('m4a.lmp', 4, tics)
