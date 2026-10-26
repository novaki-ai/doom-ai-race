import sys, math; sys.path.insert(0, '../tools_m45')
from dbg import load
import sim
pre = load(sys.argv[1]); out = sys.argv[2]
r = sim.run(5, pre); x, y, z, a = r.pos[-1][:4]
d = 180 - a
while d > 180: d -= 360
while d < -180: d += 360
t = int(round(d / 1.40625))
tics = list(pre)
while abs(t) > 0:
    s = max(-46, min(46, t)); tics.append((0, 0, s, 0)); t -= s
tics.append((0, 0, 0, 2))
for k in range(80):
    tics.append((50, 0, 0, 0))
    r2 = sim.run(5, tics) if k % 5 == 4 else None
    if r2 and r2.pos[-1][0] < -700: break
r2 = sim.run(5, tics)
print('end', len(tics), [round(v) for v in r2.pos[-1][:4]], r2.pos[-1][4:6])
sim.write_lmp(out, 5, tics)
