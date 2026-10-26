from sim import Sim
from lmp import oku
r=Sim(4);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/phasejump4.lmp')[1]][:579]);r.smartturn=True;r.auto_doors=True;r.auto_dist=60
r.goto(-1560,1888,face=180,rad=8,speed=30,brake=1,maxn=200)
r.step(b=2);r.step(n=10);r.save('work/finaltrim4.lmp');r.report();r.close()
