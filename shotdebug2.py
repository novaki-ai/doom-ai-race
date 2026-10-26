from sim import Sim
r=Sim(2);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=True;r.combat_lock=True;r.hitscan_priority=True
for p in [(-32,20),(-64,288),(-192,288),(-192,416),(-176,496),(-192,288),(-64,288),(400,180),(400,-10),(780,0),(920,0),(1450,0),(1500,350),(1140,352),(1500,350),(1450,0),(900,0),(700,0),(600,600),(0,700),(0,976)]:
 if not r.goto(*p,fire=True,rad=22,maxn=250,speed=30,brake=1):break
r.save('work/shotdebug2.lmp');r.report();r.close()
