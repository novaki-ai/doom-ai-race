from sim import Sim
from lmp import oku
import itertools,contextlib
base=[(f,s,a//256,b) for f,s,a,b in oku('work/lastapproach7.lmp')[1]][:4704]
best=5660
for delay,avoid,fire,lock in itertools.product([0,1,3,7],[True,False],[True,False],[True,False]):
 r=Sim(7);r.replay(base);r.step(n=delay);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=avoid;r.combat_lock=lock;r.hitscan_priority=True;r.combat_range=600
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  for p in [(928,-1840),(1104,-1800),(1232,-1744),(1232,-1984),(1232,-2112),(1216,-2200),(1280,-2240),(1408,-2192),(1600,-2240),(1712,-2256),(1712,-2304),(1920,-2304)]:
   if not r.goto(*p,fire=fire,rad=16,maxn=250,speed=30,brake=.5):break
  r.face(0,n=8);r.step(b=2);r.step(n=10)
 print('TRY',delay,avoid,fire,lock,len(r.t),r.state['health'],r.state['state'],flush=True)
 if r.state['state']!=0 and len(r.t)<best:
  best=len(r.t);r.save('work/healfinish7.lmp');print('BEST',best,flush=True)
 r.close()
