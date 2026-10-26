from sim import Sim
from lmp import oku
r=Sim(8);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/lastboss8.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True
for p in [(416,3904),(416,4032),(416,4300),(320,4384)]:r.goto(*p,fire=True,rad=15,maxn=600,stucklimit=500)
r.face(90,n=14);r.step(b=2);r.step(n=100)
for p in [(320,4480),(380,4550),(416,4800),(416,4980),(448,5120)]:r.goto(*p,fire=False,rad=15,maxn=600,stucklimit=500)
r.step(n=1500)
r.save('work/exit8.lmp');r.draw();r.report();r.close()
