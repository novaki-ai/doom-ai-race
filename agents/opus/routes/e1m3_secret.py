import sys, os, math, pickle
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'tools_m23'))
from wad import read_map
from seg import run_segments
from openall import open_all
import sim
m = read_map('E1M3')
OV = open_all('E1M3')
OV[165] = (128, None)
OV2 = dict(OV); OV2[66] = (64, None)
USE = {995, 329, 332, 535, 360, 87, 785}
D = dict(direct=True, r=16)
def d(**k):
    x = dict(D); x.update(k); return x
segs = [
    dict(goals=[(-1504, -3235, dict(must=True, r=16, jit=3)), (-1504, -3140, dict(jit=3)), (-1867, -2557, dict(must=True, r=16, jit=3)), (-1922, -2502, dict(jit=3, r=20)),
                (-1936, -2104, dict(face=90, facer=60, r=14, jit=3))], ov=OV, need={535}, tries=int(os.environ.get('T0', 4)), max=900),
    dict(goals=[(-2248, -2168, dict(jit=4)), (-2560, -1420, dict(jit=6))], ov=OV, tries=int(os.environ.get('T0', 4)), max=900),
    dict(goals=[(-2690, -1335, dict(jit=3, r=20)), (-2860, -1150, dict(jit=4)), (-2770, -960, dict(jit=3, r=20)),
                (-2705, -968, d()), (-2698, -1010, d()), (-2690, -1062, d()), (-2640, -1064, d()), (-2575, -1064, d()),
                (-2500, -1062, d()), (-2450, -1000, d()), (-2405, -935, d(face=45, facer=60, r=12))], ov=OV, need={360}, tries=int(os.environ.get('T1', 4)), max=600),
    dict(goals=[(-2450, -1000, d()), (-2500, -1062, d()), (-2575, -1064, d()), (-2640, -1064, d()), (-2690, -1062, d()),
                (-2698, -1010, d()), (-2705, -968, d()), (-2770, -960, d(r=20)), (-2860, -1150, dict(jit=4)), (-2690, -1335, dict(jit=3, r=20)),
                (-2560, -1420, dict(jit=6)), (-1900, -2540, dict(jit=6)), (-1500, -3000, dict(jit=6)), (-1480, -2700, dict(jit=4)), (-1504, -2560, dict(jit=3, r=20))],
         ov=OV2, unuse={329, 332}, tries=int(os.environ.get('T2', 4)), max=900),
    dict(goals=[(-1504, -2140, dict(jit=4)), (-1504, -1980, dict(jit=4, r=20)), (-1504, -1880, dict(jit=6)), (-1300, -1668, dict(jit=4)), (-1492, -1492, dict(jit=4)),
                (-1492, -1420, dict(jit=4)), (-1260, -1428, dict(jit=4)), (-1116, -1444, dict(jit=4)), (-1088, -1500, dict(face=270, facer=60, r=10, fixed=True))],
         ov=OV2, tries=int(os.environ.get('T3', 6)), max=900),
]
start_seg = int(sys.argv[1]) if len(sys.argv) > 1 else 0
PFX = os.environ.get('PFX', 'e1m3s')
prefix, used0, cur = (), (), (-1472, -3344)
if start_seg > 0:
    prefix, used0, cur, _ = pickle.load(open(os.path.join(HERE, os.environ.get('LOADPFX', PFX) + f'_seg{start_seg - 1}.pkl'), 'rb'))
tics, used, cur, si = run_segments('E1M3', 3, m, segs, USE, {785}, OV, cur, os.path.join(HERE, PFX), tries=4,
                                   prefix=prefix, used0=used0, start_seg=start_seg, seed=int(os.environ.get('SEED', 0)))
res = sim.run(3, tics)
print('FINAL tics', len(tics), 'exit', res.exit_time, 'seg', si)
sim.write_lmp(os.path.join(HERE, PFX + '_search.lmp'), 3, tics)
