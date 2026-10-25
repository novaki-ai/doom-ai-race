from sim import Sim
from lmp import oku
r=Sim(7);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/west7.lmp')[1]][:1693]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
for p in [(-1152,-576),(-960,-224),(-1192,-144),(-1376,-64),(-1552,160),(-1680,160),(-1696,192),(-1696,328),(-1672,344),(-1424,384),(-1424,336),(-1680,344),(-1696,320),(-1696,176),(-1520,88),(-1464,88),(-1376,-64),(-1200,-160)]:
 if not r.goto(*p,fire=True,rad=12,maxn=500,stucklimit=400):break
r.save('work/armorwest7.lmp');r.draw();r.report();r.close()
