from sim import Sim
from lmp import oku
r=Sim(3)
for f,s,a,b in oku('submit/E1M3.lmp')[1]:
 r.step(f,s,a//256,b)
 if r.state['x']>450 and r.state['z']>=143 and r.state['y']>-1630:break
r.report();r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=True;r.combat_lock=True;r.hitscan_priority=True
for p in [(560,-1600),(704,-1600),(704,-1728)]:r.goto(*p,fire=True,rad=16,maxn=250)
r.face(270,n=8);r.step(b=2);r.step(n=10)
r.save('work/trim3.lmp');r.report();r.close()
