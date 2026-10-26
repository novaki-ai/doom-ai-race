from sim import Sim
from lmp import oku
import itertools,contextlib,math
base=[(f,s,a//256,b) for f,s,a,b in oku('submit/E1M8.lmp')[1]][:2100]
for speed,avoid,lock in itertools.product([12,18,24],[False,True],[True,False]):
 r=Sim(8);r.replay(base);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.combat_lock=lock;r.combat_range=900;r.avoid=avoid
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  for p in [(416,3904),(416,4032),(416,3300)]:r.goto(*p,fire=True,rad=20,maxn=150)
  for k in range(12):
   for p in [(128,3100),(128,2600),(416,2600),(704,2600),(704,3100),(640,3300),(192,3300)]:
    r.goto(*p,fire=True,rad=20,speed=speed,maxn=100)
    bs=[o for o in r.state['monsters'] if o[0]==15 and o[4]>0]
    if r.state['health']<=0 or not bs:break
   if r.state['health']<=0 or not bs:break
 print('TRY',speed,avoid,lock,'boss',[(o[4],round(o[1]),round(o[2])) for o in bs],'hp',r.state['health'],'ammo',r.state['ammo'],'tic',len(r.t),flush=True)
 if r.state['health']>0 and not bs:r.save('work/fastboss8.lmp');r.report();r.close();break
 r.close()
