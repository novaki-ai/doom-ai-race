from sim import Sim
from lmp import oku
import itertools,contextlib
base=[(f,s,a//256,b) for f,s,a,b in oku('work/rushkey2.lmp')[1]]
best=2041
for brake,avoid,fire in itertools.product([.5,1,.3],[True,False],[True,False]):
 r=Sim(2);r.replay(base);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=avoid;r.combat_lock=True;r.hitscan_priority=True
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  for p in [(0,700),(-500,650),(-500,360),(-680,384),(-752,384),(-830,450),(-1600,470),(-1700,650),(-1710,1000),(-1536,1220),(-1536,1620),(-1536,1980),(-1536,2070)]:
   if not r.goto(*p,fire=fire,rad=20,maxn=250,speed=30,brake=brake):break
  r.face(90,n=15);r.step(b=2);r.step(n=5)
  for p in [(-1680,2080),(-1730,2240),(-1680,2270),(-1350,2270),(-1160,2220),(-960,2150),(-820,2240),(-700,2336),(-570,2336),(-576,2432),(-460,2400),(-350,2400),(-350,2336),(-280,2336)]:
   if not r.goto(*p,fire=fire,rad=20,maxn=250,speed=30,brake=brake):break
  r.face(0,n=15);r.step(b=2);r.step(n=10)
 print('TRY',brake,avoid,fire,r.state['health'],r.state['state'],len(r.t),round(r.state['x']),round(r.state['y']),flush=True)
 if r.state['state']!=0 and len(r.t)<best:best=len(r.t);r.save('work/rushfinish2b.lmp');r.report()
 r.close()
