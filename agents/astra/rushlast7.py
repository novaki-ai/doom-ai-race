from sim import Sim
from lmp import oku
import itertools,contextlib
base=[(f,s,a//256,b) for f,s,a,b in oku('work/lastapproach7.lmp')[1]]
best=5660
for delay,avoid,fire,route in itertools.product([0,1,3,7],[True,False],[False,True],[0,1]):
 r=Sim(7);r.replay(base);r.step(n=delay);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=avoid;r.combat_lock=True;r.hitscan_priority=True;r.combat_range=500
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  pts=[(1240,-2080),(1240,-2160),(1280,-2240),(1440,-2240),(1712,-2256),(1712,-2304),(1920,-2304)] if route==0 else [(1200,-2128),(1216,-2200),(1280,-2240),(1312,-2272),(1600,-2304),(1712,-2256),(1712,-2304),(1920,-2304)]
  for p in pts:
   if not r.goto(*p,fire=fire,rad=20,maxn=150,speed=30,brake=1):break
  r.face(0,n=8);r.step(b=2);r.step(n=10)
 print('TRY',delay,avoid,fire,route,len(r.t),r.state['health'],r.state['state'],flush=True)
 if r.state['state']!=0 and len(r.t)<best:
  best=len(r.t);r.save('work/rushlast7.lmp');print('BEST',best,flush=True)
 r.close()
