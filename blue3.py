from sim import Sim
from lmp import oku
r=Sim(3);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/route3b.lmp')[1]][:346]);r.auto_doors=True;r.avoid=True
pts=[(-1870,-1712),(-1840,-1552),(-1808,-1448),(-1730,-1200),(-1700,-820),(-1664,-784),(-1216,-664),(-840,-664),(-800,-704),(-608,-696),(-584,-680),(-496,-664),(-400,-424),(-328,-424),(-176,-456),(-168,-480),(-160,-864)]
for p in pts:
 if not r.goto(*p,fire=True,rad=16):break
r.save('work/blue3.lmp');r.draw();r.report();r.close()
