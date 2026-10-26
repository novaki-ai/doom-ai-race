from sim import Sim
from lmp import oku
r=Sim(7);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/switchend7.lmp')[1]][:4712]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True;r.combat_lock=True;r.hitscan_priority=True;r.combat_range=900
for p in [(280,-2376),(400,-2368),(448,-2256),(448,-2016),(496,-1872),(352,-1760)]:
 if not r.goto(*p,fire=True,rad=12,maxn=350):break
r.face(90,n=40);r.step(b=2);r.step(n=10)
r.save('work/clear7.lmp');r.draw();r.report();r.close()
