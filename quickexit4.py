from sim import Sim
from lmp import oku
r=Sim(4);r.replay([(f,s,a//256,b) for f,s,a,b in oku('submit/E1M4.lmp')[1]][:840]);r.smartturn=True;r.weapon_policy=True;r.auto_doors=False
r.goto(-1420,1888,fire=False,rad=8,use=False);r.face(180,n=8);r.step(b=2);r.step(n=30)
r.goto(-1560,1888,fire=False,rad=8,use=False);r.face(180,n=8);r.step(b=2);r.step(n=10)
r.save('work/quickexit4.lmp');r.report();r.close()
