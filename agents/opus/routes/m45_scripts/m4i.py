import sys, math, random, time; sys.path.insert(0, '../tools_m45')
from m4e import m, UL
from follow import follow
from dbg import load
import sim
tA = load('m4e_A.lmp')
a = [float(v) for v in sys.argv[1:]]
TX = a[0] if a else -220
WB = [dict(x=-470, y=1888, r=12), dict(x=TX, y=1888, r=25, face=135, facer=400)]
tB, rB = follow(4, WB, prefix=tA, max_tics=700, K=4, m=m, uselines={547, 548, 554}, repeat_use={554}, stop_at_end=True)
print('B', len(tB), [round(v, 1) for v in rB.pos[-1][:4]], getattr(rB, 'dead', None))
for i in range(350, len(rB.pos), 4): print(i, [round(v) for v in rB.pos[i][:4]])
sim.write_lmp('m4i_B.lmp', 4, tB)
