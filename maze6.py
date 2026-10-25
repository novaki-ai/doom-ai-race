from sim import Sim
from lmp import oku
r=Sim(6);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/main6.lmp')[1]][:2140]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
for p in [(296,-160),(608,-168),(1160,-184),(1208,-224),(1760,-192),(1944,-416),(1960,-512),(2136,-696),(2152,-760),(2368,-968),(2440,-968),(2456,-992),(2456,-1416),(2400,-1504),(2400,-2096),(2624,-2240)]:
 if not r.goto(*p,fire=True,rad=12,maxn=500,stucklimit=400):break
r.face(270,n=14);r.step(b=2);r.step(n=5)
r.save('work/maze6.lmp');r.draw();r.report();r.close()
