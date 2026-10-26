from sim import Sim
r=Sim(2);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=True;r.combat_lock=True;r.hitscan_priority=True
for p in [(-32,20),(-32,264),(-64,288),(-144,288),(-160,320),(-176,496),(-160,304),(-112,280),(-56,280),(32,192),(48,160),(400,-10),(780,0),(920,0),(1450,0),(1500,350),(1140,352),(1500,350),(1450,0),(900,0),(700,0),(600,600),(0,700),(0,976)]:
 if not r.goto(*p,fire=True,rad=12,maxn=250,speed=30,brake=1):break
r.save('work/shotdebug2.lmp');r.report();r.close()
