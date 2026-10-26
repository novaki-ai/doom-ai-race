from sim import Sim
from lmp import oku
import itertools,contextlib
base=[(f,s,a//256,b) for f,s,a,b in oku('work/saferocket7.lmp')[1]]
best=0
for delay,avoid,lock,pri in itertools.product([0,1,3,7,12],[True,False],[True,False],[True,False]):
 r=Sim(7);r.replay(base);r.step(n=delay);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=avoid;r.combat_lock=lock;r.hitscan_priority=pri;r.combat_range=900
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  for p in [(664,-2480),(640,-2496),(512,-2560),(176,-2560),(104,-2536),(96,-2504),(96,-2440),(280,-2376),(400,-2368),(448,-2256),(448,-2016),(496,-1872),(352,-1760)]:
   if not r.goto(*p,fire=True,rad=14,maxn=250):break
  if r.state['health']>0 and abs(r.state['x']-352)<40 and abs(r.state['y']+1760)<40:
   r.face(90,n=40);r.step(b=2);r.step(n=10)
   if r.state['health']>best:
    best=r.state['health'];r.save('work/rocketswitch7.lmp');print('BEST',delay,avoid,lock,pri,len(r.t),best,flush=True)
 r.close()
 if best>=25:break
