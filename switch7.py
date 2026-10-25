from sim import Sim
from lmp import oku
r=Sim(7);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/platform7.lmp')[1]][:1303]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
for p in [(96,-1088),(96,-1544),(32,-1568)]:
 if not r.goto(*p,fire=True,rad=12,maxn=500,stucklimit=400):break
r.face(270,n=40);r.step(b=2);r.step(n=20)
r.save('work/switch7.lmp');r.draw();r.report();r.close()
