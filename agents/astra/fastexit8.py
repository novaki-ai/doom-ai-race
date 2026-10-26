from sim import Sim
from lmp import oku
r=Sim(8);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/fastboss8.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
for p in [(128,3100),(416,3500),(416,4300),(320,4384)]:r.goto(*p,fire=False,rad=16,maxn=250)
r.face(90,n=10);r.step(b=2);r.step(n=100)
for p in [(380,4550),(416,4800),(416,4980),(448,5120)]:r.goto(*p,fire=False,rad=15,maxn=300,stucklimit=250)
r.step(n=1500)
r.save('work/fastexit8.lmp');r.report();r.close()
