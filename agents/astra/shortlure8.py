from sim import Sim
from lmp import oku
import math,itertools,contextlib
base=[(f,s,a//256,b) for f,s,a,b in oku('submit/E1M8.lmp')[1]][:2100]
for delay,y,lock in itertools.product([0,35,70,110],[2640,2660,2700],[True,False]):
 r=Sim(8);r.replay(base);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.combat_lock=lock;r.combat_range=1000;r.avoid=True
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  for p in [(416,3904),(416,4032),(160,3264),(64,2960),(128,y),(416,y)]:r.goto(*p,fire=True,rad=20,maxn=100)
  r.goto(600,y,fire=True,rad=1,maxn=delay,stucklimit=500,speed=0)
  for p in [(128,2700),(64,2960),(160,3264),(416,3300)]:r.goto(*p,fire=True,rad=20,maxn=100)
  r.avoid=False
  for k in range(200):
   a=k*math.tau/12
   r.goto(416+230*math.cos(a),3270+220*math.sin(a),fire=True,rad=25,speed=12,maxn=70)
   bs=[o for o in r.state['monsters'] if o[0]==15 and o[4]>0]
   if r.state['health']<=0 or not bs:break
 print('TRY',delay,y,lock,'boss',[(o[4],round(o[1]),round(o[2])) for o in bs],'hp',r.state['health'],'ammo',r.state['ammo'],'tic',len(r.t),flush=True)
 if r.state['health']>0 and not bs:r.save('work/fastboss8.lmp');r.report();r.close();break
 r.close()
