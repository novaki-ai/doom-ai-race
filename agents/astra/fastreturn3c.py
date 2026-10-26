from sim import Sim
from lmp import oku
import itertools,contextlib
base=[(f,s,a//256,b) for f,s,a,b in oku('work/upper3.lmp')[1]]
best=2431
for fire,avoid,brake,delay in itertools.product([True],[True,False],[.5,1,.3],[0,3,7]):
 r=Sim(3);r.replay(base);r.step(n=delay);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=avoid;r.combat_lock=False
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  for p in [(-160,-488),(-168,-456),(-328,-416),(-384,-416),(-416,-432),(-416,-512),(-496,-672),(-576,-672),(-688,-704),(-832,-736),(-860,-704),(-960,-648),(-1080,-620),(-1240,-632),(-1350,-700),(-1450,-768),(-1615,-803),(-1760,-992),(-1824,-1496),(-1856,-1608),(-1880,-1744),(-1864,-2040),(-1864,-2400),(-1896,-2440),(-1896,-2488),(-1900,-2520),(-1824,-3024),(-1792,-3040),(-1400,-3072),(-1200,-3072),(-1192,-3016),(-1192,-2616),(-1304,-2544),(-1344,-2528),(-1280,-2440),(-1256,-2400),(-1256,-2352),(-1280,-2320),(-1312,-2160)]:
   if not r.goto(*p,fire=fire,rad=14,maxn=250,brake=brake):break
 if r.state['health']>0 and abs(r.state['x']+1312)<50 and abs(r.state['y']+2160)<50 and len(r.t)<best:
  best=len(r.t);r.save('work/fastreturn3c.lmp');print('BEST',fire,avoid,brake,delay,best,r.state['health'],flush=True)
 print('TRY',fire,avoid,brake,delay,r.state['health'],round(r.state['x']),round(r.state['y']),len(r.t),flush=True)
 r.close()
