from sim import Sim
from lmp import oku
r=Sim(7);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/platform7.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
for p in [(-512,-104),(-544,-104),(-608,-96),(-560,-128),(-576,-856),(-552,-936),(-432,-1208),(-432,-1376),(-392,-1408),(-360,-1408),(-336,-1376),(-336,-1344)]:
 if not r.goto(*p,fire=True,rad=12,maxn=500,stucklimit=400):break
r.save('work/soul7.lmp');r.draw();r.report();r.close()
