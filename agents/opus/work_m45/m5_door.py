import sys, math; sys.path.insert(0, '../tools_m45')
from dbg import load
import sim
pre = load(sys.argv[1])
r = sim.run(5, pre); x, y, z, a = r.pos[-1][:4]
print('end', len(pre), round(x), round(y), round(a))
d = 180 - a
while d > 180: d -= 360
while d < -180: d += 360
t = int(round(d / 1.40625))
tics = list(pre)
while abs(t) > 0:
    s = max(-46, min(46, t)); tics.append((0, 0, s, 0)); t -= s
tics.append((0, 0, 0, 2))
tics += [(25, 0, 0, 0)] * 40
r2 = sim.run(5, tics)
for i in range(len(pre), len(r2.pos), 4): print(i, [round(v) for v in r2.pos[i][:4]])
