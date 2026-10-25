from sim import Sim
from lmp import oku
r=Sim(5);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/westdone5.lmp')[1]][:2076]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True
for p in [(-1888,744),(-1888,808),(-1848,832),(-1784,832),(-1624,1136),(-1600,1144),(-1328,1208),(-1040,1216),(-992,1240),(-992,1296),(-880,1296),(-800,1400),(-800,1530)]:
 if p==(-1784,832):r.face(0,n=10);r.step(b=2);r.step(n=50)
 if not r.goto(*p,fire=True,rad=22,maxn=500,stucklimit=400):break
r.save('work/star5.lmp');r.draw();r.report();r.close()
