from sim import Sim
from lmp import oku
r=Sim(5);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/searchgate5.lmp')[1]])
r.smartturn=True;r.auto_doors=True;r.weapon_policy=True
for p in [(-1064,552),(-1112,512),(-1170,448),(-1320,448),(-1488,448),(-1624,540),(-1624,576),(-1440,744),(-1120,832)]:
 if not r.goto(*p,fire=True,rad=20):break
r.face(0,n=14);r.step(b=2);r.step(n=3)
r.save('work/switch5.lmp');r.draw();r.report();r.close()
