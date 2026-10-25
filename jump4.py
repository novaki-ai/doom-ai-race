from sim import Sim
from lmp import oku
r=Sim(4);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/route4b.lmp')[1]][:607]);r.auto_doors=True
r.face(180,n=28);r.step(b=2);r.step(n=28)
r.goto(-540,1984,fire=True)
r.goto(-80,1976,fire=True,rad=3)
r.face(231,n=28)
r.goto(-1380,1840,speed=30,fire=False)
r.goto(-1400,1888,fire=True)
r.goto(-1530,1888,fire=True)
r.face(180,n=28);r.step(b=2);r.step(n=2)
r.draw();r.save('work/jump4.lmp');r.report();r.close()
