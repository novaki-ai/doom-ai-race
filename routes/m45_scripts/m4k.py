import sys, math; sys.path.insert(0, '../tools_m45')
from dbg import load
from follow import follow
from wad import read_map
import sim
m = read_map('E1M4')
tB = load(sys.argv[1]); d = int(sys.argv[2]); f0 = int(sys.argv[3]); out = sys.argv[4]
run = [(0, 0, 0, 0)] * d + [(f0, -f0, 0, 0)] + [(50, -50, 0, 0)] * 75
res = sim.run(4, tB + run)
P = res.pos
for i in range(len(tB), len(P)):
    if P[i][0] < -1235 and P[i][2] >= 190:
        cut = i + 1; break
pre = (tB + run)[:cut]
print('landed at tic', cut, P[cut - 1][:3])
W = [dict(x=-1440, y=1888, r=20), dict(x=-1570, y=1888, r=10, face=180, facer=100)]
tics, r2 = follow(4, W, prefix=pre, max_tics=800, K=4, m=m, uselines={547, 548, 554}, repeat_use={554}, verbose=True)
print('exit', r2.exit_time, 'dead', getattr(r2, 'dead', None), 'tics', len(tics))
sim.write_lmp(out, 4, tics)
