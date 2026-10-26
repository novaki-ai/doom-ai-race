import sys, random, time; sys.path.insert(0, '../tools_m45')
from follow import follow
from wad import read_map
from dbg import load
import sim
m = read_map('E1M4')
prefix = load('m4c.lmp')[:340]
W = [dict(x=-535, y=1900, r=40), dict(x=-500, y=1995, r=40), dict(x=-100, y=1995, r=40), dict(x=-100, y=1900, r=30),
     dict(x=-560, y=1888, r=30), dict(x=-900, y=1888, r=30), dict(x=-1300, y=1888, r=30), dict(x=-1440, y=1888, r=20),
     dict(x=-1570, y=1888, r=10, face=180, facer=100)]
tics, res = follow(4, W, prefix=prefix, max_tics=800, K=4, m=m, uselines={648, 649, 468, 469, 547, 548, 554}, repeat_use={554}, verbose=True)
print('exit', res.exit_time, getattr(res, 'dead', None), len(tics))
sim.write_lmp('m4one.lmp', 4, tics)
