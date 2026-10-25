from sim import Sim
from lmp import oku
import math,itertools,contextlib
base=[(f,s,a//256,b) for f,s,a,b in oku('work/gun8.lmp')[1]]
best=2000
for y,loops,sg in itertools.product([2600,2640,2560],[12,20,6,30],[False,True]):
 r=Sim(8);r.replay(base);r.smartturn=True;r.auto_doors=True;r.weapon_policy=sg;r.combat_lock=True;r.combat_range=900;r.avoid=False
 if not sg:r.step(b=28)
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  for k in range(loops):
   r.goto(192 if k%2==0 else 640,y,fire=True,rad=20,speed=20,maxn=100)
   if r.state['health']<=0:break
  if r.state['health']>0:
   for p in [(160,2660),(64,2960),(160,3264),(416,3300)]:r.goto(*p,fire=True,rad=20,maxn=100)
  for k in range(200):
   if r.state['ammo'][0]<5:r.weapon_policy=True
   a=math.pi/2+k*math.tau/16
   r.goto(416+300*math.cos(a),3000+300*math.sin(a),fire=True,rad=20,speed=16,maxn=70)
   bs=[o for o in r.state['monsters'] if o[0]==15 and o[4]>0]
   if r.state['health']<=0 or not bs:break
  if r.state['health']>0 and not bs:
   r.save('work/fastboss8.lmp')
  score=sum(o[4] for o in bs)
  if score<best:
   best=score;r.save('work/bestboss8.lmp')
 print('TRY',y,loops,sg,'boss',score,'hp',r.state['health'],'tics',len(r.t),flush=True)
 if r.state['health']>0 and not bs:r.report();r.close();break
 r.close()
