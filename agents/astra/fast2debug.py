from sim import Sim
r=Sim(2);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True;r.combat_lock=False
for p in [(-32,20),(-64,288),(-192,288),(-192,350)]:r.goto(*p,fire=True,rad=14)
r.face(90,n=40);r.step(b=2);r.step(n=25)
for p in [(-192,416),(-176,496),(-192,288),(-64,288),(400,180),(370,288),(240,288),(240,432)]:
 if not r.goto(*p,fire=True,rad=16,maxn=300):break
r.save('work/fastgear2.lmp');r.report();r.close()
