from sim import Sim
from lmp import oku
r=Sim(7);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/switchend7.lmp')[1]][:4756]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=False
r.goto(400,-2368,shoot_at=(320,-2336),rad=12,maxn=150)
for p in [(448,-2368),(448,-2256),(448,-2016),(496,-1872),(352,-1760)]:
 if not r.goto(*p,fire=True,rad=12,maxn=300):break
r.face(90,n=40);r.step(b=2);r.step(n=10)
r.save('work/zombie7.lmp');r.draw();r.report();r.close()
