from sim import Sim
from lmp import oku
r=Sim(3);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/route3b.lmp')[1]][:265]);r.auto_doors=True;r.avoid=True
for p in [(-2048,-2368),(-1864,-2208),(-1860,-2040)]:r.goto(*p,fire=True,rad=16)
r.save('work/base3.lmp');r.report();r.smartturn=True;r.combat_lock=True;r.avoid=False
for p in [(-2070,-2000),(-2130,-1940),(-2144,-1800),(-2144,-1760),(-2144,-1600)]:
 if not r.goto(*p,fire=True,rad=16):break
r.save('work/bestgear3.lmp');r.report();r.close()
