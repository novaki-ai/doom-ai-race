from sim import Sim
from lmp import oku
r=Sim(6);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/soul6.lmp')[1]][:5604]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
for p in [(-1664,1472),(-1664,1400),(-1640,1384),(-1496,1384)]:r.goto(*p,fire=False,rad=12,maxn=200)
r.face(0,n=40);r.step(b=2);r.step(n=5)
r.save('work/quiet6.lmp');r.report();r.close()
