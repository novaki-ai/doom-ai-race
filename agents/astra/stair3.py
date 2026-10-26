from sim import Sim
from lmp import oku
r=Sim(3);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/mainexit3.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True;r.combat_lock=True;r.hitscan_priority=True;r.combat_range=1200
for p in [(-1216,-2104),(-992,-1904),(-992,-1880),(-888,-1824),(-800,-1824),(-448,-1600),(-200,-1600),(0,-1600),(480,-1600),(480,-1728),(448,-1792),(560,-1600),(704,-1600),(704,-1728)]:
 if not r.goto(*p,fire=True,rad=14,maxn=650,stucklimit=600):break
r.face(270,n=40);r.step(b=2);r.step(n=10)
r.save('work/stair3.lmp');r.draw();r.report();r.close()
