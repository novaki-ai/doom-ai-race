from sim import Sim
from lmp import oku
import math,itertools,contextlib
base=[(f,s,a//256,b) for f,s,a,b in oku('submit/E1M8.lmp')[1]][:2100]
for loops,avoid,speed in itertools.product([2,4,8],[False,True],[18,24]):
 r=Sim(8);r.replay(base);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.combat_lock=True;r.combat_range=900;r.avoid=avoid
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  for p in [(416,3904),(416,4032),(160,3264),(64,2960),(128,2660),(416,2580)]:r.goto(*p,fire=True,rad=20,maxn=200)
  for k in range(loops*12):
   a=math.pi/2+k*math.tau/12
   r.goto(416+280*math.cos(a),2560+80*math.sin(a),fire=True,rad=20,speed=speed,maxn=70)
   bs=[o for o in r.state['monsters'] if o[0]==15 and o[4]>0]
   if r.state['health']<=0 or not bs:break
  if r.state['health']>0 and bs:
   for p in [(128,2700),(64,2960),(160,3264),(416,3300)]:r.goto(*p,fire=True,rad=20,maxn=150)
   for k in range(160):
    a=math.pi/2+k*math.tau/12
    r.goto(416+230*math.cos(a),3270+220*math.sin(a),fire=True,rad=25,speed=14,maxn=70)
    bs=[o for o in r.state['monsters'] if o[0]==15 and o[4]>0]
    if r.state['health']<=0 or not bs:break
 print('TRY',loops,avoid,speed,'boss',[(o[4],round(o[1]),round(o[2])) for o in bs],'hp',r.state['health'],'ammo',r.state['ammo'],'tic',len(r.t),flush=True)
 if r.state['health']>0 and not bs:r.save('work/fastboss8.lmp');r.report();r.close();break
 r.close()
