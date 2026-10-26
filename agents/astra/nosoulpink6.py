from sim import Sim
from lmp import oku
from nav import Nav
import itertools,contextlib,math
base=[(f,s,a//256,b) for f,s,a,b in oku('work/lateback6.lmp')[1]]
best=5482
for delay,avoid,pri in itertools.product([0,1,3,7,12],[True,False],[True,False]):
 r=Sim(6);r.replay(base);r.step(n=delay);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=avoid;r.combat_lock=True;r.hitscan_priority=pri;r.combat_range=900
 n=Nav(r.wad,8,20)
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  sec=[v[:] for v in r.state['sectors']]
  for i,s in enumerate(r.wad.sec):
   if s[0]==s[1] and sec[i][1]>sec[i][0]:sec[i][1]=max(sec[i][1],sec[i][0]+64)
  path=n.path((r.state['x'],r.state['y']),(-1648,1584),sectors=sec)
  for p in path[1:]:
   if not r.goto(*p,fire=True,rad=14,maxn=250):break
  r.goto(-1640,1496,fire=True,rad=14,maxn=200)
  r.avoid=False
  for k in range(120):
   enemies=[o for o in r.state['monsters'] if o[0]==12 and o[4]>0 and math.hypot(o[1]-r.state['x'],o[2]-r.state['y'])<150]
   if not enemies or r.state['health']<=0:break
   o=min(enemies,key=lambda o:math.hypot(o[1]-r.state['x'],o[2]-r.state['y']))
   r.goto(-1664,1424,shoot_at=(o[1],o[2]),rad=8,maxn=1,stucklimit=500)
  for p in [(-1664,1400),(-1640,1384)]:r.goto(*p,fire=True,rad=16,maxn=100)
  r.goto(-1496,1384,shoot_at=(-1552,1392),rad=14,maxn=180)
  r.face(0,n=20);r.step(b=2);r.step(n=10)
  for p in [(-1648,1384),(-1792,1344),(-1840,1540),(-1984,1520),(-2016,1584),(-2016,1800),(-2016,1880),(-2016,1940),(-2048,1984),(-1944,1952),(-1920,2016)]:
   if not r.goto(*p,fire=True,rad=14,maxn=250):break
  r.face(0,n=20);r.step(b=2);r.step(n=10)
 print('TRY',delay,avoid,pri,len(r.t),r.state['health'],r.state['state'],r.state['x'],r.state['y'],flush=True)
 if r.state['state']!=0 and len(r.t)<best:
  best=len(r.t);r.save('work/nosoulpink6.lmp');print('BEST',best,flush=True)
 r.close()
