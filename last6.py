from sim import Sim
from lmp import oku
r=Sim(6);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/targetexit6.lmp')[1]][:6134]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
for p in [(-1976,1952),(-1920,1970),(-1920,2016)]:r.goto(*p,fire=False,face=0,rad=10,maxn=100)
r.step(b=2);r.step(n=10);r.save('work/last6.lmp');r.report();r.close()
