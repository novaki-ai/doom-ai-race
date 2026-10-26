from sim import Sim
from lmp import oku
import itertools,contextlib
base=[(f,s,a//256,b) for f,s,a,b in oku('work/fastboss8.lmp')[1]]
for targetx,waitfloor,rad in itertools.product([320,328,336,560],[24,20],[12,20]):
 r=Sim(8);r.replay(base);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=False
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  for p in [(128,3100),(416,3500),(416,4130)]:r.goto(*p,fire=False,rad=16,maxn=250,brake=1,speed=30)
  while r.state['sectors'][30][0]>waitfloor:r.step()
  r.goto(416,4224,fire=False,rad=rad,speed=30,brake=100,maxn=30)
  r.goto(targetx,4460,fire=False,rad=20,speed=30,brake=100,maxn=40)
 print('JUMP',targetx,waitfloor,rad,r.state['x'],r.state['y'],r.state['z'],len(r.t),flush=True)
 if r.state['z']>=-8 and r.state['y']>4416:
  for p in [(targetx,4800),(targetx,4980),(448,5120)]:r.goto(*p,fire=False,rad=20,speed=30,brake=1,maxn=200)
  r.step(n=1500);r.save('work/jumpout8.lmp');r.report();r.close();break
 r.close()
