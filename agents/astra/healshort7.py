from sim import Sim
from lmp import oku
import itertools,contextlib
base=[(f,s,a//256,b) for f,s,a,b in oku('work/shortsouth7.lmp')[1]][:3722]
best=0
for delay,avoid,lock,pri,brake in itertools.product([0,3,7],[True,False],[True,False],[True,False],[.3,1]):
 r=Sim(7);r.replay(base);r.step(n=delay);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=avoid;r.combat_lock=lock;r.hitscan_priority=pri;r.combat_range=900
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  for p in [(-400,-800),(-120,-800),(-88,-768),(-40,-608),(-48,-592),(-112,-864),(96,-1184),(96,-1424),(392,-1640),(592,-1640),(648,-1688),(664,-1728)]:
   if not r.goto(*p,fire=True,rad=14,speed=30,brake=brake,maxn=250):break
 if r.state['health']>best and abs(r.state['x']-664)<40 and abs(r.state['y']+1728)<40:
  best=r.state['health'];r.save('work/healshort7.lmp');print('BEST',delay,avoid,lock,pri,brake,len(r.t),best,flush=True)
 r.close()
 if best>=45:break
