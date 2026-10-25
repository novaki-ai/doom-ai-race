from sim import Sim
from lmp import oku
import itertools
base=[(f,s,a//256,b) for f,s,a,b in oku('work/route4b.lmp')[1]][:607]
for xx,yy,aim in itertools.product([-540,-480,-400,-320],[1984,1960,1920],[224,231,225]):
 r=Sim(4);r.replay(base);r.smartturn=True;r.weapon_policy=True
 r.face(180,n=7);r.step(b=2);r.step(n=28)
 r.goto(xx,yy,rad=8,use=False)
 r.face(aim,n=10)
 r.smartturn=False
 r.goto(-1380,1848,fire=False,speed=30,rad=18,maxn=170,use=False)
 if r.state['x']<-1280 and r.state['z']>=190:
  r.smartturn=True;r.goto(-1420,1888,rad=8,use=False);r.face(180,n=8);r.step(b=2);r.step(n=30)
  r.goto(-1560,1888,rad=8,use=False);r.face(180,n=8);r.step(b=2);r.step(n=10)
  if r.state['state']!=0:r.save('work/boost4.lmp');r.report();r.close();break
 r.close()
