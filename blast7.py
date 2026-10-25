from sim import Sim
from lmp import oku
import math
r=Sim(7);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/switchend7.lmp')[1]][:4682]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True;r.combat_lock=True
r.step(b=36);r.face(40,n=50);r.report();r.face(40,fire=True,n=45);r.report()
for p in [(96,-2440),(280,-2376),(400,-2368),(448,-2256),(448,-2016),(496,-1872),(352,-1760)]:
 if not r.goto(*p,fire=True,rad=12,maxn=350):break
r.face(90,n=40);r.step(b=2);r.step(n=10)
r.save('work/blast7.lmp');r.draw();r.report();r.close()
