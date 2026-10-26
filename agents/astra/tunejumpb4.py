from sim import Sim
from lmp import oku
import contextlib
base=[(f,s,a//256,b) for f,s,a,b in oku('work/bypasslift4.lmp')[1]]
best=602
for value in range(50,-1,-1):
 r=Sim(4);r.replay(base);r.smartturn=True;r.auto_doors=True;r.auto_dist=52
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  r.goto(-570,1888,rad=5,maxn=100)
  r.goto(-450,1864,rad=3,maxn=100)
  r.face(225,n=10)
  for k in range(35):
   r.step(f=50,s=50)
   if r.state['x']<-720 or r.state['health']<=0:break
  r.step(f=value,s=value)
  for k in range(50):
   r.step(f=50,s=50)
   if r.state['x']<-1280 or r.state['health']<=0:break
  if r.state['x']<-1280 and r.state['z']>=190 and r.state['health']>0:
   r.goto(-1560,1888,face=180,rad=8,speed=30,brake=1,maxn=200,stucklimit=150)
   r.step(b=2);r.step(n=10)
 if r.state['state']!=0 and len(r.t)<best:
  best=len(r.t);r.save('work/tunejumpb4.lmp');print('BEST',value,best,r.state['health'],flush=True)
 r.close()
