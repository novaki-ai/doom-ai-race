from sim import Sim
from lmp import oku
import itertools,contextlib
base=[(f,s,a//256,b) for f,s,a,b in oku('work/fastboss8.lmp')[1]]
for floor,align,targetx in itertools.product([54,60,48,66],[4150,4170,4130],[336,348,320]):
 r=Sim(8);r.replay(base);r.smartturn=True;r.avoid=False
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  for p in [(128,3100),(416,3500)]:r.goto(*p,rad=16,maxn=150)
  r.face(90,n=40)
  while r.state['sectors'][30][0]>floor:r.step()
  for k in range(80):
   r.goto(416,4500,rad=1,speed=30,brake=100,maxn=1)
   if r.state['y']>=align:break
  r.goto(targetx,4420,rad=12,speed=30,brake=100,maxn=60)
 print('JUMP',floor,align,targetx,len(r.t),r.state['x'],r.state['y'],r.state['z'],flush=True)
 if r.state['z']>=-8 and r.state['y']>4380:
  for p in [(320,4500),(320,4800),(320,4980),(448,5120)]:r.goto(*p,rad=20,speed=30,brake=1,maxn=150)
  r.step(n=1500);r.save('work/runjump8.lmp');r.report();r.close();break
 r.close()
