import sys, math; sys.path.insert(0, '../tools_m45')
from m5a import leg, show, m
import sim
variants = {
 'east': [(-150, -100), (-25, 120), (-30, 290), (-64, 420)],
 'west': [(-150, -100), (-170, 150), (-112, 290), (-64, 420)],
 'mid':  [(-150, -100), (-64, 200), (-64, 290), (-64, 420)],
 'east2': [(-100, -150), (40, 100), (-20, 292), (-64, 420)],
}
for name, pts in variants.items():
    W = [dict(x=x, y=y, r=30) for x, y in pts]
    t, r = leg(W, (), [476, 477], mt=400)
    print(name, len(t), [round(v) for v in r.pos[-1][:3]], 'dead', getattr(r, 'dead', None), 'reached', getattr(r, 'reached', None), flush=True)
    sim.write_lmp(f'm5b_{name}.lmp', 5, t)
