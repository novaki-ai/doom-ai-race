from sim import Sim
from lmp import oku
r=Sim(5);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/switch5.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=False;r.combat_lock=True;r.hitscan_priority=True
for p in [(-1440,744),(-1600,600),(-1700,800),(-1776,824),(-1888,824),(-1888,744),(-1888,480),(-1856,448),(-1888,744),(-1888,824),(-1784,832),(-1624,1136),(-1600,1144),(-1328,1208),(-1040,1216),(-992,1240),(-992,1296),(-880,1296),(-800,1400),(-800,1530)]:
 if not r.goto(*p,fire=True,rad=20,maxn=350,stucklimit=300):break
r.save('work/fastsoul5.lmp');r.report();r.close()
