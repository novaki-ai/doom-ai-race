from sim import Sim
from lmp import oku
import itertools,contextlib
base=[(f,s,a//256,b) for f,s,a,b in oku('submit/E1M8.lmp')[1]][:2100]
best=4016
for speed,avoid,brake in itertools.product([24,30,18],[True,False],[1,.5]):
 r=Sim(8);r.replay(base);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.combat_lock=True;r.combat_range=1000;r.avoid=avoid
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  for p in [(416,3904),(416,4032),(160,3264),(64,2960),(128,2600),(128,2544)]:r.goto(*p,fire=True,rad=20,maxn=150)
  for k in range(30):
   for p in [(704,2544),(704,2640),(128,2640),(128,2544)]:
    r.goto(*p,fire=True,rad=24,speed=speed,brake=brake,maxn=100)
    bs=[o for o in r.state['monsters'] if o[0]==15 and o[4]>0]
    if r.state['health']<=0 or not bs:break
   if r.state['health']<=0 or not bs:break
 print('TRY',speed,avoid,brake,'boss',[(o[4],round(o[1]),round(o[2])) for o in bs],'hp',r.state['health'],'ammo',r.state['ammo'],'tic',len(r.t),flush=True)
 if r.state['health']>0 and not bs and len(r.t)<best:
  best=len(r.t);r.save('work/rectboss8.lmp');r.report()
 r.close()
