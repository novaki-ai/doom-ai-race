from sim import Sim
from lmp import oku
import itertools,contextlib,math
base=[(f,s,a//256,b) for f,s,a,b in oku('work/lastapproach7.lmp')[1]]
best=5660
for launch,aim,wait,avoid in itertools.product([(1056,-1984),(1110,-2018)],[(1248,-2208),(1216,-2176)],[35,50],[True,False]):
 r=Sim(7);r.replay(base);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.avoid=avoid;r.combat_lock=True;r.hitscan_priority=True;r.combat_range=900;r.weapon_policy=False
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  r.step(b=36)
  r.goto(*launch,fire=False,rad=8,maxn=150)
  r.face(math.degrees(math.atan2(aim[1]-r.state['y'],aim[0]-r.state['x'])),n=wait)
  r.goto(r.state['x']+100,r.state['y'],speed=0,shoot_at=aim,fire=True,maxn=40,stucklimit=100)
  r.step(b=20);r.weapon_policy=True
  for p in [(1120,-2024),(1216,-2200),(1280,-2240),(1312,-2272),(1600,-2304),(1712,-2256),(1712,-2304),(1920,-2304)]:
   if not r.goto(*p,fire=True,rad=14,maxn=250):break
  r.face(0,n=8);r.step(b=2);r.step(n=10)
 print('TRY',launch,aim,wait,avoid,len(r.t),r.state['health'],r.state['state'],flush=True)
 if r.state['state']!=0 and len(r.t)<best:
  best=len(r.t);r.save('work/lastrocket7.lmp');print('BEST',best,flush=True)
 r.close()
