from sim import Sim
from lmp import oku
import itertools,contextlib
base=[(f,s,a//256,b) for f,s,a,b in oku('work/quickfinish2.lmp')[1]][:1797]
for delay,avoid,lock in itertools.product([140,210,280],[False,True],[True,False]):
 r=Sim(2);r.replay(base);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=avoid;r.combat_lock=lock;r.hitscan_priority=True
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  r.goto(-480,2336,speed=0,maxn=delay,stucklimit=500,fire=True)
  for p in [(-460,2400),(-350,2400),(-350,2336),(-280,2336)]:r.goto(*p,fire=True,rad=16,maxn=250)
  r.face(0,n=20);r.step(b=2);r.step(n=10)
 print('TRY',delay,avoid,lock,r.state['health'],len(r.t),r.state['state'],flush=True)
 if r.state['state']!=0:r.save('work/room2.lmp');r.report();r.close();break
 r.close()
