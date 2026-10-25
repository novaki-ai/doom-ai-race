from sim import Sim
from lmp import oku
r=Sim(3);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/searchgear3.lmp')[1]]);r.weapon_policy=True;r.auto_doors=True;r.avoid=True;r.smartturn=True
pts=[(-2144,-1820),(-2120,-1980),(-1860,-2000),(-1870,-1712),(-1840,-1552),(-1808,-1448),(-1740,-1200),(-1760,-992),(-1700,-820),(-1600,-800),(-1216,-664),(-1000,-620),(-840,-664),(-800,-704),(-608,-696),(-496,-664),(-400,-424),(-328,-424),(-272,-528),(-176,-480),(-160,-864)]
for p in pts:
 if not r.goto(*p,fire=True,rad=16):break
r.save('work/gearedblue3.lmp');r.draw();r.report();r.close()
