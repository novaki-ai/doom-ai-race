import sys; sys.path.insert(0, '../tools_m45')
from follow import follow
from auto import plan
from wad import read_map
import sim
m = read_map('E1M4')
UX = float(sys.argv[1]) if len(sys.argv) > 1 else -150
W = plan('E1M4', (2032, 1120), [(-468, 1580)])
W += [dict(x=-530, y=1790, r=40), dict(x=-535, y=1900, r=40), dict(x=-480, y=1985, r=40), dict(x=UX, y=1985, r=40),
      dict(x=-560, y=1888, r=30), dict(x=-900, y=1888, r=30), dict(x=-1300, y=1888, r=30), dict(x=-1440, y=1888, r=20),
      dict(x=-1570, y=1888, r=10, face=180, facer=100)]
tics, res = follow(4, W, max_tics=900, K=4, m=m, uselines={648, 649, 468, 469, 547, 548, 554}, repeat_use={554}, verbose=True)
print(len(tics), res.exit_time, getattr(res, 'dead', None))
for i in range(0, len(res.pos), 5):
    if i > 300: print(i, [round(v) for v in res.pos[i][:4]])
sim.write_lmp('m4b.lmp', 4, tics)
