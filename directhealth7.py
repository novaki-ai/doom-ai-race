from sim import Sim
from lmp import oku
import itertools,contextlib
base=[(f,s,a//256,b) for f,s,a,b in oku('work/healswitch7.lmp')[1]]
best=5660
for delay,avoid,lock,pri in itertools.product([0,1,3,7,12],[True,False],[True,False],[True,False]):
 r=Sim(7);r.replay(base);r.step(n=delay);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=avoid;r.combat_lock=lock;r.hitscan_priority=pri;r.combat_range=700;r.near=True
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  for p in [(344,-2288),(296,-2320),(216,-2368),(96,-2440),(96,-2528),(128,-2544),(200,-2560),(584,-2560),(672,-2464),(672,-2104),(688,-2064),(736,-2024),(864,-1960),(1000,-1960),(1120,-2024),(1216,-2200),(1280,-2240),(1312,-2272),(1600,-2304),(1712,-2304),(1720,-2272),(1920,-2304)]:
   if not r.goto(*p,fire=True,rad=14,maxn=250):break
  r.face(0,n=8);r.step(b=2);r.step(n=10)
 if r.state['state']!=0 and len(r.t)<best:
  best=len(r.t);r.save('work/directhealth7.lmp');print('BEST',delay,avoid,lock,pri,best,r.state['health'],flush=True)
 r.close()
