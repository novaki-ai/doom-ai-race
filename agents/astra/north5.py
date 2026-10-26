from sim import Sim
from lmp import oku
r=Sim(5);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/exit5.lmp')[1]][:3864]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
for p in [(0,1544),(0,1640),(250,1740),(320,1728),(450,1860),(500,2040),(320,2130),(80,2130),(-80,2220),(-80,2320),(-150,2336),(-280,2336),(-288,2460)]:
 if not r.goto(*p,fire=True,rad=20,maxn=500,stucklimit=400):break
r.face(90,n=14);r.step(b=2);r.step(n=10)
r.save('work/north5.lmp');r.draw();r.report();r.close()
