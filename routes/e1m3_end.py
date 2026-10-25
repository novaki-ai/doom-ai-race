"""Continue E1M3 from a prefix that just crossed the stair trigger: hide, wait, then stairs + exit."""
import sys; sys.path.insert(0, '..')
exec(open('e1m3.py').read().split('if __name__')[0].replace("print(i, len(w)", "pass  # print(i, len(w)"))
from lmp import oku
from optimize import beam_legs2
import sim
h, t, _ = oku(sys.argv[1]); pre = [(f, s, a >> 8, b) for f, s, a, b in t]
r0 = sim.run(3, pre)
cross = None
for i in range(len(r0.pos) - 1, 0, -1):
    if r0.pos[i][0] > -256 and r0.pos[i - 1][0] <= -256: cross = i; break
wait = int(sys.argv[2]) if len(sys.argv) > 2 else 225
hx, hy = (float(sys.argv[3]), float(sys.argv[4])) if len(sys.argv) > 4 else (-704, -1990)
print('cross at', cross, 'prefix', len(pre), 'hide', hx, hy, 'until', cross + wait)
kw0 = dict(legs[26][1]); kw0['stuck_tics'] = 400
hide = [dict(x=-420, y=-1640, r=40), dict(x=-600, y=-1760, r=40), dict(x=hx, y=hy, r=30, hard=1, until=cross + wait)]
sub = [(hide, kw0), legs[26], legs[27]]
best = beam_legs2(3, sub, n=int(sys.argv[5]) if len(sys.argv) > 5 else 6, beam=2, jitter=10, seed=3, out='e1m3_end.lmp', final_n=6, prefix=pre, safe=True)
print('BEST', best[0] if best else None)
