from sim import Sim
from lmp import oku
r=Sim(7);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/blue7.lmp')[1]][:2230]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=False
for p in [(-1450,-64),(-1450,-104),(-1360,-104),(-1200,-160),(-1152,-576),(-960,-224),(-600,-320),(-608,-96)]:
 if not r.goto(*p,fire=True,rad=8,maxn=250):break
r.save('work/edge7.lmp');r.draw();r.report();r.close()
