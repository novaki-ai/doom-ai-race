import sys; sys.path.insert(0, '../tools_m45')
from follow import follow
from auto import plan
from wad import read_map
import sim
m = read_map('E1M4')
args = [float(a) for a in sys.argv[1:]]
EX = args[0] if len(args) > 0 else -90
EY = args[1] if len(args) > 1 else 1900
NY = args[2] if len(args) > 2 else 1995
W = plan('E1M4', (2032, 1120), [(-468, 1580)])
W += [dict(x=-530, y=1790, r=40), dict(x=-535, y=1900, r=40), dict(x=-500, y=NY, r=40), dict(x=EX, y=NY, r=40), dict(x=EX, y=EY, r=30),
      dict(x=-560, y=1888, r=30), dict(x=-900, y=1888, r=30), dict(x=-1300, y=1888, r=30), dict(x=-1440, y=1888, r=20),
      dict(x=-1570, y=1888, r=10, face=180, facer=100)]
tics, res = follow(4, W, max_tics=900, K=4, m=m, uselines={648, 649, 468, 469, 547, 548, 554}, repeat_use={554}, verbose=False)
print('RESULT', args, len(tics), res.exit_time, getattr(res, 'dead', None))
xs = [(i, round(p[0]), round(p[1]), round(p[2])) for i, p in enumerate(res.pos) if i > 340 and i % 5 == 0]
print(xs[:45])
sim.write_lmp('m4d.lmp', 4, tics)
