from sim import Sim
import math
r=Sim(8);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True
r.goto(-84,-224,rad=3,use=False);r.face(0,n=10);r.step(b=2);r.step(n=40)
r.goto(-32,-224,fire=False,rad=8)
r.face(math.degrees(math.atan2(-192-r.state['y'],176-r.state['x'])),fire=True,n=90)
for p in [(120,-224),(400,-100),(416,100),(416,380),(528,384),(416,500),(416,700),(416,928),(-32,864),(-160,864),(-96,928),(-96,800),(416,864),(416,1400),(416,2380),(416,2600),(416,3100)]:
 if not r.goto(*p,fire=True,rad=20,maxn=500):break
r.save('work/route8.lmp');r.draw();r.report();r.close()
