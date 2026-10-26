import sys, math; sys.path.insert(0, '../tools_m45')
from m5a import leg, show, m
import sim
P = [(-148,-36), (524,156), (868,204), (888,275), (852,204), (244,172), (204,172), (204,428), (404,508), (876,652), (916,692), (1052,780), (1052,844), (980,884), (764,876)]
W = [dict(x=x, y=y, r=30) for x, y in P] + [dict(x=692, y=804, r=12)]
t, r = leg(W, (), [], mt=900, verbose=True)
print('L12', len(t), [round(v) for v in r.pos[-1][:3]], 'dead', getattr(r, 'dead', None), 'reached', getattr(r, 'reached', None))
show(r, 0, 15)
sim.write_lmp('m5_L12.lmp', 5, t)
