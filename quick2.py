from sim import Sim
from lmp import oku
import itertools,contextlib
base=[(f,s,a//256,b) for f,s,a,b in oku('submit/E1M2.lmp')[1]][:600]
best=2371
for delay,avoid,lock in itertools.product([0,3,7],[False,True],[True,False]):
 r=Sim(2);r.replay(base);r.step(n=delay);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=avoid;r.combat_lock=lock;r.hitscan_priority=True
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  for p in [(780,0),(920,0),(1450,0),(1500,350),(1140,352),(1500,350),(1450,0),(900,0),(700,0),(600,600),(-500,650),(-500,360),(-680,384),(-830,450),(-1600,470),(-1700,650),(-1710,1000),(-1536,1220),(-1536,1620),(-1536,1980),(-1536,2070)]:
   if not r.goto(*p,fire=True,rad=18,maxn=350):break
  r.face(90,n=25);r.step(b=2);r.step(n=5)
  for p in [(-1680,2080),(-1730,2240),(-1680,2270),(-1350,2270),(-1160,2220),(-960,2150),(-820,2240),(-700,2336),(-570,2336),(-460,2400),(-350,2400),(-350,2336),(-280,2336)]:
   if not r.goto(*p,fire=True,rad=18,maxn=350):break
  r.face(0,n=25);r.step(b=2);r.step(n=10)
 print('TRY',delay,avoid,lock,r.state['health'],len(r.t),r.state['state'],r.state['x'],r.state['y'],flush=True)
 if r.state['state']!=0 and len(r.t)<best:best=len(r.t);r.save('work/quick2.lmp');r.report()
 r.close()
