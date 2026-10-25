from sim import Sim
import itertools
best=631
for fire,speed,rad in itertools.product([False,True],[30,22],[20,30]):
 r=Sim(1);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True
 for p in [(1250,-3000),(1290,-2530),(1480,-2490),(1660,-2490),(2240,-2660),(2400,-2650),(2800,-2800),(2930,-2940),(2930,-3550),(3000,-3800),(3044,-4110),(3050,-4240),(3090,-4420),(3010,-4580),(3008,-4700),(2970,-4768)]:
  if not r.goto(*p,fire=fire,rad=rad,speed=speed):break
 r.goto(2940,-4768,rad=6,fire=fire,face=180);r.face(180,n=7);r.step(b=2);r.step(n=10)
 r.report()
 if r.state['state']!=0 and len(r.t)<best:best=len(r.t);r.save('work/fast1.lmp')
 r.close()
