from sim import Sim
from lmp import oku
r=Sim(3);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/route3b.lmp')[1]][:124]);r.auto_doors=True;r.avoid=True
r.goto(-1880,-2850,fire=True)
r.avoid=False
for p in [(-1250,-2850),(-1170,-2740),(-1170,-2500),(-1344,-2528),(-1504,-2500),(-1504,-2160),(-1504,-2040),(-1504,-1870),(-1700,-1670),(-1700,-1480),(-1500,-1440),(-1230,-1440),(-1100,-1470)]:
 if not r.goto(*p,fire=False,speed=30):break
r.face(-90,n=28);r.step(b=2);r.step(n=2)
r.save('work/jump3.lmp');r.draw();r.report();r.close()
