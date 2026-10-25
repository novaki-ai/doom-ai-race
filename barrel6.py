from sim import Sim
from lmp import oku
import math
r=Sim(6);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/soul6.lmp')[1]][:5604]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
r.face(math.degrees(math.atan2(1344-r.state['y'],-1664-r.state['x'])),n=40);r.face(math.degrees(math.atan2(1344-r.state['y'],-1664-r.state['x'])),fire=True,n=80)
print('barrel',[(o[:5]) for o in r.state['monsters'] if o[0]==30 and abs(o[1]+1664)<10])
for p in [(-1664,1472),(-1664,1400),(-1640,1384),(-1496,1384)]:r.goto(*p,fire=True,rad=12,maxn=300)
r.face(0,n=40);r.step(b=2);r.step(n=5)
r.save('work/barrel6.lmp');r.report();r.close()
