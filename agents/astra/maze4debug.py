from sim import Sim
r=Sim(4);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=True;r.combat_lock=True;r.hitscan_priority=True
for p in [(1900,1150),(1770,1150),(1500,1000),(1400,800),(1312,800),(1100,740),(920,560),(736,392),(736,304),(704,288),(312,296),(-80,384),(-168,440),(-560,696),(-640,904),(-640,1032),(-296,1328),(-296,1416),(-368,1552),(-448,1592),(-480,1640),(-550,1790),(-550,1888)]:
 if not r.goto(*p,fire=True,rad=12 if p in [(736,304),(704,288),(-448,1592)] else 24,maxn=200,speed=30,brake=.5):break
r.report();r.close()
