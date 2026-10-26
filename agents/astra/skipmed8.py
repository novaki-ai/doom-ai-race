from sim import Sim
from lmp import oku
import itertools,contextlib
base=[(f,s,a//256,b) for f,s,a,b in oku('work/rectboss8.lmp')[1]]
best=3585
for floor,align in itertools.product([60,64,56,68],[(400,4150),(408,4170),(400,4170)]):
 r=Sim(8);r.replay(base);r.smartturn=True;r.auto_doors=False
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  for p in [(704,3100),(416,3500)]:r.goto(*p,rad=16,maxn=200)
  r.face(90,n=40)
  while r.state['sectors'][30][0]>floor and r.state['health']>0:r.step()
  for p in [(376,4000),(376,4080),align,(320,4420)]:
   if not r.goto(*p,rad=12,maxn=80,speed=30,brake=100):break
  if r.state['y']>4400 and r.state['z']>=-10:
   for p in [(320,4500),(320,4800),(320,4980),(448,5120)]:r.goto(*p,rad=20,speed=30,brake=1,maxn=150)
   r.step(n=1000)
 print('TRY',floor,align,len(r.t),r.state['health'],r.state['state'],round(r.state['x']),round(r.state['y']),r.state['z'],flush=True)
 if r.state['state']!=0 and len(r.t)<best:
  best=len(r.t);r.save('work/skipmed8.lmp');print('BEST',best,flush=True)
 r.close()
