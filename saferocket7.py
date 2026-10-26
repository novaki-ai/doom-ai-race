from sim import Sim
from lmp import oku
import itertools,contextlib
base=[(f,s,a//256,b) for f,s,a,b in oku('work/shortsouth7.lmp')[1]][:3722]
best=0
for launch,aim,delay,avoid,pri in itertools.product([-256,-208,-176],[(0,-864),(-48,-896)],[0,3],[True,False],[True,False]):
 r=Sim(7);r.replay(base);r.step(n=delay);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=False;r.avoid=avoid;r.combat_lock=True;r.hitscan_priority=pri;r.combat_range=900
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  r.step(b=36,n=1)
  for p in [(-256,-864),(launch,-864)]:r.goto(*p,fire=False,rad=10,maxn=150)
  r.goto(0,-864,speed=0,fire=True,shoot_at=aim,maxn=40,stucklimit=200)
  r.step(b=20,n=1);r.weapon_policy=True
  for p in [(-112,-864),(96,-1184),(96,-1424),(392,-1640),(592,-1640),(648,-1688),(664,-1728)]:
   if not r.goto(*p,fire=True,rad=16,speed=30,brake=.5,maxn=250):break
 if r.state['health']>best and abs(r.state['x']-664)<40 and abs(r.state['y']+1728)<40:
  best=r.state['health'];r.save('work/saferocket7.lmp');print('BEST',launch,aim,delay,avoid,pri,len(r.t),best,flush=True)
 r.close()
 if best>=35:break
