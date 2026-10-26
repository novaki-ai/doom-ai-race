from sim import Sim
from lmp import oku
import itertools,contextlib
base=[(f,s,a//256,b) for f,s,a,b in oku('work/rushroom2.lmp')[1]]
best=2041
for delay,route,avoid,lock in itertools.product([70,140,210,280],[0,1],[False,True],[True,False]):
 r=Sim(2);r.replay(base);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.avoid=avoid;r.combat_lock=lock;r.hitscan_priority=True
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  r.goto(-465,2422,speed=0,maxn=delay,stucklimit=500,fire=True)
  pts=[(-460,2400),(-350,2400),(-350,2336),(-280,2336)] if route==0 else [(-560,2240),(-400,2240),(-350,2280),(-350,2336),(-280,2336)]
  for p in pts:
   if not r.goto(*p,fire=True,rad=16,maxn=250):break
  r.face(0,n=15);r.step(b=2);r.step(n=10)
 print('TRY',delay,route,avoid,lock,r.state['health'],len(r.t),r.state['state'],flush=True)
 if r.state['state']!=0 and len(r.t)<best:best=len(r.t);r.save('work/pistolend2.lmp');r.report()
 r.close()
