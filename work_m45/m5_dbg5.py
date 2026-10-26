import sys; sys.path.insert(0, '../tools_m45')
from follow import follow
from dbg import load
from m5beam import STAGES
import sim
pre = load(sys.argv[1]); li = int(sys.argv[2]); st = sys.argv[3] if len(sys.argv) > 3 else 'S2'
wps, kw = STAGES[st][li]
r0 = sim.run(5, pre); print('prefix end', len(pre), [round(v) for v in r0.pos[-1][:3]], r0.pos[-1][4:6])
tics, res = follow(5, wps, prefix=pre, stop_at_end=True, verbose=True, **kw)
print('reached', getattr(res, 'reached', None), 'dead', res.dead, len(tics))
for i in range(len(pre) - 2, len(res.pos), 3): print(i, [round(v) for v in res.pos[i][:3]], res.pos[i][4:6])
