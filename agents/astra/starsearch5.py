from sim import Sim
from lmp import oku
import itertools,contextlib
base=[(f,s,a//256,b) for f,s,a,b in oku('work/westdone5.lmp')[1]][:2076]
best=2763
for delay,avoid,lock,brake in itertools.product([0,3],[True,False],[True,False],[.3,1]):
 r=Sim(5);r.replay(base);r.step(n=delay);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=avoid;r.combat_lock=lock;r.hitscan_priority=True
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  for p in [(-1888,744),(-1888,808),(-1848,832),(-1784,832),(-1624,1136),(-1600,1144),(-1328,1208),(-1040,1216),(-984,1224),(-984,1296),(-880,1296),(-800,1400),(-800,1530)]:
   if not r.goto(*p,fire=True,rad=16,maxn=300,speed=30,brake=brake):break
 if r.state['health']>=70 and r.state['x']>0 and r.state['y']<300 and len(r.t)<best:
  best=len(r.t);r.save('work/starsearch5.lmp');print('BEST',delay,avoid,lock,brake,best,r.state['health'],flush=True)
 r.close()
