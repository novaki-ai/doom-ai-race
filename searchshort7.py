from sim import Sim
from lmp import oku
import itertools,contextlib
base=[(f,s,a//256,b) for f,s,a,b in oku('work/east7b.lmp')[1]]
best=0
for delay,avoid,lock,pri,fire in itertools.product([0,3,7,12],[True,False],[False,True],[False,True],[True,False]):
 r=Sim(7);r.replay(base);r.step(n=delay);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=avoid;r.combat_lock=lock;r.hitscan_priority=pri;r.combat_range=700
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  for p in [(-520,312),(-496,312),(-400,304),(-352,232),(-392,-48),(-416,-224),(-416,-784),(-256,-864),(-112,-864),(96,-1184),(96,-1424),(392,-1640),(592,-1640),(648,-1688),(664,-1728)]:
   if not r.goto(*p,fire=fire,rad=16,maxn=200):break
 if r.state['health']>best and abs(r.state['x']-664)<40 and abs(r.state['y']+1728)<40:
  best=r.state['health'];r.save('work/searchshort7.lmp');print('BEST',delay,avoid,lock,pri,fire,len(r.t),best,flush=True)
 r.close()
 if best>=40:break
