from sim import Sim
from lmp import oku
r=Sim(6);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/barrel6.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True;r.combat_lock=True;r.combat_range=800
r.goto(r.state['x']+100,r.state['y'],speed=0,rad=5,fire=True,maxn=400,stucklimit=500)
for p in [(-1648,1384),(-1840,1540),(-1984,1520),(-2016,1584),(-2016,1800),(-2016,1880),(-2048,1984),(-1920,2016)]:
 if not r.goto(*p,fire=True,rad=12,maxn=300):break
r.face(0,n=40);r.step(b=2);r.step(n=10)
r.save('work/clearwest6.lmp');r.draw();r.report();r.close()
