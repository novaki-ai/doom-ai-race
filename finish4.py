from sim import Sim
from lmp import oku
r=Sim(4);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/route4b.lmp')[1]][:607]);r.auto_doors=True
r.goto(-1380,1888,speed=30,fire=False)
r.goto(-1530,1888,fire=True)
r.face(180,n=28);r.step(b=2);r.step(n=2)
r.draw();r.save('work/finish4.lmp');r.report();r.close()
