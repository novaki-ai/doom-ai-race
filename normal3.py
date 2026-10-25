from sim import Sim
from lmp import oku
r=Sim(3);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/route3b.lmp')[1]][:265]);r.smartturn=True;r.auto_doors=True;r.avoid=True
pts=[(-2048,-2368),(-1864,-2208),(-1860,-2040),(-1870,-1712),(-1840,-1552),(-1808,-1448),(-1740,-1200),(-1760,-992),(-1700,-820),(-1600,-800),(-1600,-736),(-1216,-664),(-1104,-768),(-840,-664),(-800,-704),(-608,-696),(-584,-680),(-496,-664),(-400,-424),(-328,-424),(-272,-528),(-160,-864)]
for p in pts:
 if not r.goto(*p,fire=True,rad=16):break
r.save('work/normal3.lmp');r.draw();r.report();r.close()
