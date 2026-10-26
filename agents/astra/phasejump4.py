from sim import Sim
from lmp import oku
import itertools,contextlib
base=[(f,s,a//256,b) for f,s,a,b in oku('work/bypasslift4.lmp')[1]][:607]
best=681
for x,y in itertools.product([-400,-420,-440,-460,-480,-500,-380,-360,-340,-320,-300],[1888,1864,1912]):
 r=Sim(4);r.replay(base);r.smartturn=True;r.auto_doors=True;r.auto_dist=52
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  r.goto(-570,1888,rad=5,maxn=100)
  r.goto(x,y,fire=False,rad=5,maxn=150)
  r.face(225,n=15)
  for k in range(90):
   r.step(f=50,s=50)
   if r.state['x']<-1280 or r.state['health']<=0:break
 print('TRY',x,y,len(r.t),r.state['x'],r.state['y'],r.state['z'],r.state['health'],flush=True)
 if r.state['x']<-1280 and r.state['z']>=190 and r.state['health']>0:
  r.goto(-1420,1888,rad=8,use=False);r.face(180,n=8);r.step(b=2);r.step(n=30)
  r.goto(-1560,1888,rad=8,use=False);r.face(180,n=8);r.step(b=2);r.step(n=10)
  if r.state['state']!=0 and len(r.t)<best:best=len(r.t);r.save('work/phasejump4.lmp');r.report()
 r.close()
