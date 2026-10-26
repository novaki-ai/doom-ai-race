import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools_m23'))
from follow import follow
from auto import plan
from wad import read_map
import sim
m = read_map('E1M2')
OV = {49: (-232, None), 137: (0, None), 129: (None, 60), 124: (None, 60)}
goals = [(1440, 352), (1140, 352, dict(must=True, r=20)), (1350, 352), (1490, 430), (-700, 384), (-1536, 1540), (-1536, 2070, dict(face=90, facer=60)), (-1400, 2080), (-1340, 2270), (-660, 2336), (-290, 2336, dict(face=0, facer=100, r=10))]
W = plan('E1M2', (-32, -240), goals, overrides=OV)
print([(round(w['x']), round(w['y'])) for w in W])
USE = {325, 326, 527, 777, 854, 873}
tics, res = follow(2, W, max_tics=2000, K=4, verbose=True, m=m, uselines=USE, repeat_use={873})
print('tics', len(tics), 'exit', res.exit_time, 'dead', getattr(res, 'dead', None), 'last', res.pos[-1] if res.pos else None)
sim.write_lmp(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'e1m2_try.lmp'), 2, tics)
