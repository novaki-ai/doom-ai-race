from sim import Sim
from lmp import oku
r=Sim(6);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/latesoul6.lmp')[1]][:5013]);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=True
for p in [(-1664,1472),(-1664,1400),(-1640,1384)]:r.goto(*p,fire=False,rad=12,maxn=150)
r.goto(-1496,1384,shoot_at=(-1488,1376),rad=12,maxn=200)
r.face(0,n=40);r.step(b=2);r.step(n=10)
r.save('work/targetlate6.lmp');r.report();r.close()
