from sim import Sim
from lmp import oku
r=Sim(7);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/main7.lmp')[1]][:2974]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
r.goto(-120,-960,fire=True,rad=10,maxn=200)
r.step(b=36);r.face(130,n=40);r.face(130,fire=True,n=20)
for p in [(-120,-800),(-220,-800),(-296,-776),(-224,-504),(-128,-448)]:
 if not r.goto(*p,fire=True,rad=12,maxn=250):break
r.save('work/gate7.lmp');r.draw();r.report();r.close()
