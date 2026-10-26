from sim import Sim
r=Sim(3);r.auto_doors=True
points=[(-1500,-3120),(-1480,-2840),(-1480,-2500),(-1480,-2112),(-1416,-1608),(-1416,-1568),(-1496,-1480),(-1496,-1440),(-1240,-1432),(-1136,-1448),(-1088,-1504)]
for p in points:
 if not r.goto(*p,fire=True):break
r.face(-90,n=28);r.step(b=2);r.step(n=2)
r.draw();r.save('work/route3.lmp');r.report();r.close()
