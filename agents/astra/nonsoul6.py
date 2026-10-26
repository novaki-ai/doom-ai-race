from sim import Sim
from lmp import oku
from nav import Nav
import itertools,contextlib
base=[(f,s,a//256,b) for f,s,a,b in oku('work/lateback6.lmp')[1]]
for delay,avoid,pri in itertools.product([0,3,7,12],[True,False],[True,False]):
 r=Sim(6);r.replay(base);r.step(n=delay);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=avoid;r.combat_lock=True;r.hitscan_priority=pri;r.combat_range=900
 n=Nav(r.wad,8,20)
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  sec=[v[:] for v in r.state['sectors']]
  for i,s in enumerate(r.wad.sec):
   if s[0]==s[1] and sec[i][1]>sec[i][0]:sec[i][1]=max(sec[i][1],sec[i][0]+64)
  path=n.path((r.state['x'],r.state['y']),(-1640,1496),sectors=sec)
  for p in path[1:]:
   if not r.goto(*p,fire=True,rad=14,maxn=250):break
  for p in [(-1664,1472),(-1664,1400),(-1640,1384),(-1496,1384)]:
   r.goto(*p,fire=True,rad=12,maxn=200,shoot_at=(-1488,1376))
  r.face(0,n=40);r.step(b=2);r.step(n=10)
  for p in [(-1648,1384),(-1840,1540),(-1984,1520),(-2016,1584),(-2016,1800),(-2016,1880),(-2016,1940),(-1944,1952),(-1920,2016)]:
   if not r.goto(*p,fire=True,rad=14,maxn=250):break
  r.face(0,n=40);r.step(b=2);r.step(n=10)
 print('TRY',delay,avoid,pri,r.state['health'],len(r.t),r.state['state'],r.state['x'],r.state['y'],flush=True)
 if r.state['state']!=0:r.save('work/nonsoul6.lmp');r.report();r.close();break
 r.close()
