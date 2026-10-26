from sim import Sim
r=Sim(4);r.near=True
points=[(1900,1150),(1780,1150),(1460,1150),(1240,1350),(1240,1550),(1000,1720),(560,1770),(400,1770),(120,1600),(50,1400),(-250,1360),(-380,1570),(-550,1888),(-700,1888),(-1000,1888),(-1000,2020),(-1380,2020),(-1400,1888),(-1530,1888)]
for p in points:
 if not r.goto(*p,fire=True):break
r.face(180,n=28);r.step(b=2);r.step(n=2)
r.draw();r.save('work/route4.lmp');r.report();r.close()
