from sim import Sim
from lmp import oku
import itertools,contextlib
base=[(f,s,a//256,b) for f,s,a,b in oku('work/bypasslift4.lmp')[1]]
best=602
for x,y,turnwait in itertools.product(range(-550,-389,10),[1888,1864,1912],[8,15]):
 r=Sim(4);r.replay(base);r.smartturn=True;r.auto_doors=True;r.auto_dist=52
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  r.goto(-570,1888,rad=5,maxn=100)
  r.goto(x,y,fire=False,rad=3,maxn=100)
  r.face(225,n=turnwait)
  for k in range(80):
   r.step(f=50,s=50)
   if r.state['x']<-1280 or r.state['health']<=0:break
  if r.state['x']<-1280 and r.state['z']>=190 and r.state['health']>0:
   r.goto(-1560,1888,face=180,rad=8,speed=30,brake=1,maxn=200,stucklimit=150)
   r.step(b=2);r.step(n=10)
 if r.state['state']!=0 and len(r.t)<best:
  best=len(r.t);r.save('work/closejump4.lmp');print('BEST',x,y,turnwait,best,r.state['health'],flush=True)
 r.close()
