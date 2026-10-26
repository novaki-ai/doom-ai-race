from sim import Sim
from lmp import oku
r=Sim(8);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/route8.lmp')[1]][:448]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True
r.goto(416,872,fire=False,rad=6);r.face(180,n=12);r.face(180,fire=True,n=240)
for p in [(168,896),(-160,864),(-96,928),(-96,800),(-32,864),(416,864),(416,1400),(416,2380),(416,2600),(416,3100)]:
 if not r.goto(*p,fire=True,rad=20,maxn=500):break
r.save('work/armory8.lmp');r.draw();r.report();r.close()
