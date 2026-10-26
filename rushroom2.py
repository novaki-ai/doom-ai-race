from sim import Sim
from lmp import oku
r=Sim(2);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/rushkey2.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.avoid=True;r.combat_lock=True;r.hitscan_priority=True
for p in [(0,700),(-500,650),(-500,360),(-680,384),(-752,384),(-830,450),(-1600,470),(-1700,650),(-1710,1000),(-1536,1220),(-1536,1620),(-1536,1980),(-1536,2070)]:
 if not r.goto(*p,fire=True,rad=20,maxn=250,speed=30,brake=.5):break
r.face(90,n=15);r.step(b=2);r.step(n=5)
for p in [(-1680,2080),(-1730,2240),(-1680,2270),(-1350,2270),(-1160,2220),(-960,2150),(-820,2240),(-700,2336),(-570,2336),(-576,2432)]:
 if not r.goto(*p,fire=True,rad=20,maxn=250,speed=30,brake=.5):break
r.save('work/rushroom2.lmp');r.report();r.close()
