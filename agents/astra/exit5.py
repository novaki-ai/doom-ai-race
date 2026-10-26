from sim import Sim
from lmp import oku
r=Sim(5);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/searchkey5.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
for p in [(256,928),(128,1232),(104,1416),(-32,1472),(32,1472),(-240,1472),(0,1544),(0,1640),(-250,1800),(-512,1984),(-300,2100),(-80,2220),(-80,2320),(-150,2336),(-280,2336),(-288,2460)]:
 if not r.goto(*p,fire=True,rad=20,maxn=500,stucklimit=400):break
r.face(90,n=14);r.step(b=2);r.step(n=10)
r.save('work/exit5.lmp');r.draw();r.report();r.close()
