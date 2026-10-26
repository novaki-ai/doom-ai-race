from sim import Sim
from lmp import oku
r=Sim(3);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/gearedblue3.lmp')[1]][:947]);r.auto_doors=True;r.smartturn=True;r.weapon_policy=True;r.avoid=False
pts=[(-1400,-800),(-1380,-840),(-1216,-920),(-992,-900),(-792,-832),(-680,-768),(-584,-680),(-496,-664),(-400,-424),(-328,-424),(-176,-456),(-168,-480),(-160,-864)]
for p in pts:
 if not r.goto(*p,fire=True,rad=16):break
r.save('work/lowerblue3.lmp');r.draw();r.report();r.close()
