import sys, math, json, pickle; sys.path.insert(0, '/race/opus/tools_m67')
from follow import follow, fs_for, wrap
import sim
from wad import read_map
m = read_map('E1M6')
D='/race/opus/work/m67/'
NV = pickle.load(open(D+'nav6ov2.pkl','rb'))
pre = json.load(open(D+'m6_A2.json'))
W = [dict(x=1180, y=-1348, r=40), dict(x=1540, y=-1348, r=30), dict(x=1640, y=-1270, r=20, hard=True), dict(x=1712, y=-1262, r=5, slow=3, hard=True)]
t1, r1 = follow(6, W, prefix=pre, max_tics=len(pre)+300, K=4, m=m, stop_at_end=True)
p = r1.pos[-1]
print('approach end', len(t1), [round(v,1) for v in p[:4]], 'prev', [round(v,1) for v in r1.pos[-2][:2]], flush=True)
def bad(pos):
    for (x, y) in pos:
        if 1640 < x < 1720 and y < -1320: return True
        if -1384 < y < -1304 and x < 1704: return True
    return False
def picked(pos):
    return any(1704 < x < 1716 and -1320 < y < -1308 for (x, y) in pos)
best = None
x0, y0, a0 = p[0], p[1], p[3]
for wait in range(0, 12, 2):
    for n1 in range(1, 10):
        for f in (6, 10, 14, 20, 30, 40, 50):
            for tx in (1709, 1710, 1711):
                t = list(t1) + [(0,0,0,0)]*wait
                d = math.degrees(math.atan2(-1314 - y0, tx - x0))
                ff, ss = fs_for(wrap(d - a0))
                k = f / 50.0
                ff, ss = int(round(ff*k)), int(round(ss*k))
                t += [(ff, ss, 0, 0)]*n1
                # then thrust back north
                dn = 90
                fb, sb = fs_for(wrap(dn - a0))
                t += [(0,0,0,0)]*3 + [(fb, sb, 0, 0)]*10
                r = sim.run(6, t)
                pos = [(q[0], q[1]) for q in r.pos[len(t1):]]
                if picked(pos) and not bad(pos):
                    steps = max(max(abs(pos[i+1][0]-pos[i][0]), abs(pos[i+1][1]-pos[i][1])) for i in range(len(pos)-1))
                    if steps < 15:
                        L = len(t)
                        if best is None or L < best[0]:
                            best = (L, t, (wait, n1, f, tx))
                            print('found', wait, n1, f, tx, L, 'maxstep', round(steps,1), flush=True)
    if best: break
if best:
    json.dump(best[1], open(D+'m6_Bsafe.json','w'))
    print('saved', best[2], best[0])
