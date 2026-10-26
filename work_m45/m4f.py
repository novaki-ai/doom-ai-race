import sys, math; sys.path.insert(0, '../tools_m45')
from m4e import run_stage, m
from dbg import load
import sim
tA = load('m4e_A.lmp')
a = [float(v) for v in sys.argv[1:]]
SX = a[0] if a else -190
SY = a[1] if len(a) > 1 else 1888
WB = [dict(x=-505, y=1650, r=30), dict(x=-215, y=1592, r=30), dict(x=SX, y=1760, r=30), dict(x=SX, y=SY, r=8, face=135, facer=60)]
tB, rB = run_stage(WB, tA)
print('B', len(tB), [round(v, 1) for v in rB.pos[-1][:4]], getattr(rB, 'dead', None))
for i in range(350, len(rB.pos), 4): print(i, [round(v) for v in rB.pos[i][:4]])
sim.write_lmp('m4f_B.lmp', 4, tB)
