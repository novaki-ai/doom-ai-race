from sim import Sim
from lmp import oku
prefix=[(f,s,a//256,b) for f,s,a,b in oku('work/jump4.lmp')[1]][:736]
for y in range(1828,1901,2):
 r=Sim(4);r.replay(prefix);r.auto_doors=True
 ok=r.goto(-1380,y,speed=30,fire=False,maxn=150)
 if ok:
  r.goto(-1400,1888,fire=True);r.goto(-1530,1888,fire=True);r.face(180,n=28);r.step(b=2);r.step(n=2);r.save('work/win4.lmp');r.report();r.close();print('SUCCESS Y',y);break
 r.close()
