from sim import Sim
from lmp import oku
r=Sim(7);r.replay([(f,s,a//256,b) for f,s,a,b in oku('submit/E1M7.lmp')[1]][:5470]);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=True;r.combat_lock=True;r.hitscan_priority=True;r.combat_range=900
for p in [(864,-1960),(1000,-1960),(1120,-2024),(1216,-2200),(1312,-2272),(1600,-2304),(1712,-2304),(1920,-2304)]:
 if not r.goto(*p,fire=True,rad=14,maxn=300):break
r.face(0,n=8);r.step(b=2);r.step(n=10)
r.save('work/quick7.lmp');r.report();r.close()
