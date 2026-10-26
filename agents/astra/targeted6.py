from sim import Sim
from lmp import oku
r=Sim(6);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/quiet6.lmp')[1]][:5692]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=False
r.goto(-1496,1384,fire=False,shoot_at=(-1488,1376),rad=12,maxn=200)
r.face(0,n=6);r.step(b=2);r.step(n=5)
r.save('work/targeted6.lmp');r.report()
for p in [(-1648,1384),(-1840,1540),(-1984,1520),(-2016,1584),(-2016,1800),(-2016,1880),(-2048,1984),(-1920,2016)]:
 if not r.goto(*p,fire=True,rad=12,maxn=300):break
r.face(0,n=40);r.step(b=2);r.step(n=10)
r.save('work/targetexit6.lmp');r.draw();r.report();r.close()
