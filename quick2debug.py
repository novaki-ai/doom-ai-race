from sim import Sim
from lmp import oku
r=Sim(2);r.replay([(f,s,a//256,b) for f,s,a,b in oku('submit/E1M2.lmp')[1]][:600]);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=True;r.combat_lock=False;r.hitscan_priority=True;r.step(n=3)
for p in [(780,0),(920,0),(1450,0),(1500,350),(1140,352),(1500,350),(1450,0),(900,0),(700,0),(600,600),(-500,650),(-500,360),(-680,384),(-830,450),(-1600,470),(-1700,650),(-1710,1000),(-1536,1220),(-1536,1620),(-1536,1980),(-1536,2070)]:
 if not r.goto(*p,fire=True,rad=18,maxn=350):break
r.save('work/quickbase2.lmp');r.report();r.close()
