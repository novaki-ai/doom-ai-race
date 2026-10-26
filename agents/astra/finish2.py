from sim import Sim
from lmp import oku
r=Sim(2);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/route2.lmp')[1]][:1999]);r.near=False
r.goto(-587,2342,rad=0,maxn=260,fire=True,speed=0,stucklimit=300)
for p in [(-460,2400),(-350,2400),(-350,2336),(-280,2336)]:
 if not r.goto(*p,fire=True):break
r.face(0,n=28);r.step(b=2);r.step(n=2)
r.save('work/finish2.lmp');r.report();r.draw();r.close()
