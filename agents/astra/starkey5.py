from sim import Sim
from lmp import oku
import itertools,contextlib
base=[(f,s,a//256,b) for f,s,a,b in oku('work/starsearch5.lmp')[1]]
best=3789
for brake,rad,lock,avoid in itertools.product([.5,1,.3],[20,26],[False,True],[True,False]):
 r=Sim(5);r.replay(base);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=avoid;r.combat_lock=lock
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  for p in [(120,176),(-24,296),(-8,608),(48,792),(400,856),(696,1048),(880,1112),(1376,1096),(1432,1032),(1456,904),(1536,888),(1560,920),(1560,1352),(1520,1392),(1448,1400),(976,1400),(328,1336),(280,1304),(272,1272),(192,1040)]:
   if not r.goto(*p,fire=True,rad=rad,maxn=250,brake=brake):break
 if r.state['keys'][0] and r.state['health']>20 and len(r.t)<best:
  best=len(r.t);r.save('work/starkey5.lmp');print('BEST',brake,rad,lock,avoid,best,r.state['health'],flush=True)
 r.close()
