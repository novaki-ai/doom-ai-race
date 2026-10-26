from sim import Sim
from lmp import oku
r=Sim(7);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/saferocket7.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True;r.auto_dist=52;r.combat_lock=True;r.hitscan_priority=True;r.combat_range=900
for p in [(664,-2480),(640,-2496),(512,-2560),(176,-2560),(104,-2536),(96,-2504),(96,-2440),(280,-2328),(344,-2288),(336,-2112),(496,-1872),(352,-1760)]:
 if not r.goto(*p,fire=True,rad=12,maxn=500,stucklimit=400):break
r.face(90,n=40);r.step(b=2);r.step(n=10)
r.save('work/debugswitch7.lmp');r.draw();r.report();r.close()
