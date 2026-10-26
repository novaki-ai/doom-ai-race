from sim import Sim
r=Sim(5);r.smartturn=True;r.auto_doors=True;r.avoid=True
pts=[(-416,-160),(-64,100),(-64,240),(-64,400),(-440,688),(-552,1184),(-576,1192),(-752,1224),(-760,1300),(-800,1530),(192,1040),(160,1200),(110,1320),(100,1420),(0,1480),(0,1640),(-250,1800),(-300,2100),(-80,2220),(-80,2320),(-150,2336),(-280,2336),(-288,2460)]
for p in pts:
 if not r.goto(*p,fire=True,rad=16):break
r.face(90,n=14);r.step(b=2);r.step(n=2)
r.save('work/fast5.lmp');r.draw();r.report();r.close()
