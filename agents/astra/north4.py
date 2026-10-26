from sim import Sim
from nav import Nav
r=Sim(4);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
for p in [(1900,1150),(1780,1150),(1460,1150),(1240,1350),(1240,1550),(1000,1720),(560,1770),(400,1770),(200,1770),(64,1740),(-80,1760),(-80,1680)]:
 if not r.goto(*p,fire=False,rad=15,maxn=200):break
r.report();r.save('work/north4.lmp');r.draw();r.close()
