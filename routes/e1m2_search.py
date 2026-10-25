import sys, os, math, pickle
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'tools_m23'))
from wad import read_map
from seg import run_segments
import sim
m = read_map('E1M2')
OV = {49: (-232, None), 137: (0, None), 129: (None, 60), 124: (None, 60)}
USE = {325, 291, 326, 527, 777, 854, 873}
segs = [
    dict(goals=[(1440, 352), (1140, 352, dict(must=True, r=20, fixed=True))]),
    dict(goals=[(1350, 352), (-670, 384, dict(jit=6)), (-790, 384, dict(jit=6)), (-1000, 470)], unuse={291}),
    dict(goals=[(-1504, 1440, dict(jit=6)), (-1504, 1530, dict(jit=4, must=True, r=20))], tries=8),
    dict(goals=[(-1490, 2078, dict(face=90, facer=50, jit=5))], ov=OV, tries=8),
    dict(goals=[(-1400, 2080, dict(jit=4)), (-1340, 2270)], ov=OV),
    dict(goals=[(-660, 2336, dict(jit=6)), (-576, 2420, dict(jit=8, must=True, r=24)), (-352, 2400, dict(jit=8)), (-352, 2336, dict(jit=4)), (-290, 2336, dict(face=0, facer=100, r=10, fixed=True))], ov=OV, tries=10, max=900),
]
start_seg = int(sys.argv[1]) if len(sys.argv) > 1 else 0
tries = int(sys.argv[2]) if len(sys.argv) > 2 else 5
prefix, used0, cur = (), (), (-32, -240)
if start_seg > 0:
    prefix, used0, cur, _ = pickle.load(open(os.path.join(HERE, f'e1m2_seg{start_seg - 1}.pkl'), 'rb'))
tics, used, cur, si = run_segments('E1M2', 2, m, segs, USE, {873}, OV, cur, os.path.join(HERE, 'e1m2'), tries=tries,
                                   prefix=prefix, used0=used0, start_seg=start_seg)
res = sim.run(2, tics)
print('FINAL tics', len(tics), 'exit', res.exit_time, 'seg', si)
sim.write_lmp(os.path.join(HERE, 'e1m2_search.lmp'), 2, tics)
