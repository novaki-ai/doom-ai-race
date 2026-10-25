from sim import Sim
from lmp import oku
r=Sim(2);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/quickbase2.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=True;r.combat_lock=True;r.hitscan_priority=True
r.face(90,n=40);r.step(b=2);r.step(n=5)
for p in [(-1680,2080),(-1730,2240),(-1680,2270),(-1350,2270),(-1160,2220),(-960,2150),(-820,2240),(-700,2336),(-570,2336),(-460,2400),(-350,2400),(-350,2336),(-280,2336)]:
 if not r.goto(*p,fire=True,rad=18,maxn=350):break
r.face(0,n=40);r.step(b=2);r.step(n=10)
r.save('work/quickfinish2.lmp');r.report();r.close()
