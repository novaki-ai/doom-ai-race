from sim import Sim
r=Sim(2);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.avoid=True
for p in [(0,0),(400,-10),(780,0),(920,0),(1450,0),(1500,350),(1140,352),(1500,350),(1450,0),(900,0),(700,0),(600,600),(0,700),(0,976)]:
 if not r.goto(*p,fire=False,rad=22,maxn=250,speed=30,brake=1):break
r.report();r.save('work/rushdebug2.lmp');r.close()
