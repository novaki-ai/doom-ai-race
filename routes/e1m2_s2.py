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
    dict(goals=[[(1440, 352), (1140, 352, dict(must=True, r=20, fixed=True))],
                [(1470, 280, dict(r=24)), (1405, 352, dict(must=True, r=18, face=205, facer=80, hold=30, firehold=True, jit=3)), (1140, 352, dict(must=True, r=20, fixed=True))],
                [(1470, 280, dict(r=24)), (1405, 352, dict(must=True, r=18, face=205, facer=80, hold=28, firehold=True, jit=3)), (1395, 352, dict(must=True, r=18, face=152, facer=80, hold=28, firehold=True, jit=3)), (1140, 352, dict(must=True, r=20, fixed=True))]], tries=int(os.environ.get('T0', 6))),
    dict(goals=[[(1350, 352), (1492, 330, dict(jit=4, r=24)), (1492, 200, dict(jit=4, r=24)), (-670, 384, dict(jit=4, must=True, r=14)), (-790, 384, dict(jit=4)), (-1000, 470)],
                [(1205, 352, dict(must=True, r=16, face=0, facer=60, hold=28, firehold=True, jit=4)), (1350, 352), (1492, 330, dict(jit=4, r=24)), (1492, 200, dict(jit=4, r=24)), (-670, 384, dict(jit=4, must=True, r=14)), (-790, 384, dict(jit=4)), (-1000, 470)],
                [(1205, 352, dict(must=True, r=16, face=0, facer=60, hold=42, firehold=True, jit=4)), (1350, 352), (1492, 330, dict(jit=4, r=24)), (1492, 200, dict(jit=4, r=24)), (-670, 384, dict(jit=4, must=True, r=14)), (-790, 384, dict(jit=4)), (-1000, 470)]], tries=int(os.environ.get('T1', 6))),
    dict(goals=[[(-1504, 1440, dict(jit=6)), (-1504, 1530, dict(jit=4, must=True, r=20))],
                [(-1830, 600, dict(jit=6)), (-1830, 900, dict(jit=8)), (-1504, 1440, dict(jit=6)), (-1504, 1530, dict(jit=4, must=True, r=20))],
                [(-1716, 560, dict(must=True, r=16, face=95, facer=60, hold=28, firehold=True, jit=4)), (-1504, 1440, dict(jit=6)), (-1504, 1530, dict(jit=4, must=True, r=20))]], tries=int(os.environ.get('T2', 6))),
    dict(goals=[(-1536, 1690, dict(jit=6)), (-1472, 1850, dict(jit=8)), (-1472, 1905, dict(jit=5)), (-1428, 1985, dict(jit=5)), (-1458, 2078, dict(face=122, facer=40, jit=4))], ov=OV, tries=8, need={777}),
    dict(goals=[(-1400, 2080, dict(jit=4)), (-1340, 2200, dict(jit=6)), (-1536, 2272, dict(must=True, r=24, jit=4)), (-1300, 2270, dict(jit=6))], ov=OV, tries=6),
    dict(goals=[(-690, 2336, dict(jit=4, must=True, r=16)), (-722, 2312, dict(must=True, r=12, face=4, facer=80, hold=int(os.environ.get('CAMP', 150)), firehold=True, jit=6)), (-560, 2290, dict(jit=10)), (-430, 2285, dict(jit=6)), (-352, 2282, dict(jit=4)), (-352, 2336, dict(r=10, must=True, face=0, facer=60, hold=90, firehold=True)), (-290, 2336, dict(face=0, facer=100, r=10, fixed=True, firehold=True))], ov=OV, tries=int(os.environ.get('T5', 10)), max=1200),
]
start_seg = int(sys.argv[1]) if len(sys.argv) > 1 else 0
tries = int(sys.argv[2]) if len(sys.argv) > 2 else 5
prefix, used0, cur = (), (), (-32, -240)
if start_seg > 0:
    prefix, used0, cur, _ = pickle.load(open(os.path.join(HERE, os.environ.get('LOADPFX', 'e1m2') + f'_seg{start_seg - 1}.pkl'), 'rb'))
tics, used, cur, si = run_segments('E1M2', 2, m, segs, USE, {873}, OV, cur, os.path.join(HERE, os.environ.get('PFX', 'e1m2')), tries=tries,
                                   prefix=prefix, used0=used0, start_seg=start_seg)
res = sim.run(2, tics)
print('FINAL tics', len(tics), 'exit', res.exit_time, 'seg', si)
sim.write_lmp(os.path.join(HERE, os.environ.get('PFX', 'e1m2') + '_search.lmp'), 2, tics)
