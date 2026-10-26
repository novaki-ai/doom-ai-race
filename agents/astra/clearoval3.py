from sim import Sim
from lmp import oku
r=Sim(3);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/gearedblue3.lmp')[1]][:947]);r.auto_doors=True;r.smartturn=True;r.weapon_policy=True;r.avoid=False;r.combat_lock=True
r.goto(-1500,-768,fire=True,rad=8)
r.goto(r.state['x']+1,r.state['y']+1,fire=True,rad=0,speed=0,maxn=420,stucklimit=500)
for p in [(-1216,-664),(-1050,-640),(-850,-700),(-800,-704),(-608,-696),(-496,-664),(-400,-424),(-328,-424),(-176,-456),(-168,-480),(-160,-864)]:
 if not r.goto(*p,fire=True,rad=20):break
r.save('work/clearoval3.lmp');r.report();r.close()
