from sim import Sim
import itertools,contextlib
best=650
for brake,avoid,lock,delay in itertools.product([.5,1,.3],[True,False],[False,True],[0,3,7]):
 r=Sim(3);r.step(n=delay);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=avoid;r.combat_lock=lock;r.hitscan_priority=True
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  for p in [(-1440,-3232),(-1500,-3120),(-1640,-3060),(-1920,-3072),(-1845,-3146),(-1880,-2800),(-1870,-2670),(-1890,-2500),(-1864,-2208),(-1860,-2040),(-2070,-2000),(-2130,-1940),(-2144,-1800),(-2144,-1760)]:
   if not r.goto(*p,fire=True,rad=20,maxn=250,brake=brake,speed=30):break
 if r.state['health']>45 and r.state['armor']>60 and abs(r.state['x']+2144)<35 and abs(r.state['y']+1760)<35 and len(r.t)<best:
  best=len(r.t);r.save('work/fastgear3.lmp');print('BEST',brake,avoid,lock,delay,best,r.state['health'],flush=True)
 r.close()
