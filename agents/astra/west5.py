from sim import Sim
from lmp import oku
r=Sim(5);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/yellow5.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.avoid=True;r.weapon_policy=True
pts=[(856,880),(1048,832),(1048,776),(704,640),(416,520),(200,420),(120,176),(48,168),(-64,240),(-64,400),(-440,688),(-590,832),(-750,832),(-1000,832)]
for p in pts:
 if not r.goto(*p,fire=True,rad=20):break
r.save('work/west5.lmp');r.draw();r.report();r.close()
