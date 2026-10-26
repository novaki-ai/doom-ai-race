from sim import Sim
from lmp import oku
r=Sim(7);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/blue7.lmp')[1]][:2223]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=False
r.goto(-1400,128,rad=8,fire=False,face=270,maxn=100);r.step(b=36);r.face(270,n=40);r.face(270,fire=True,n=60)
for p in [(-1452,32),(-1452,-64),(-1376,-64),(-1376,-104),(-1200,-160),(-960,-224),(-1152,-576),(-896,-760),(-896,-1288),(-800,-1450),(-640,-1504)]:
 if not r.goto(*p,fire=True,rad=10,maxn=350):break
r.face(0,n=40);r.step(b=2);r.step(n=30)
r.save('work/rocket7.lmp');r.draw();r.report();r.close()
