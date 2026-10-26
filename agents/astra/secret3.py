from sim import Sim
from lmp import oku
from nav import Nav
r=Sim(3);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/gearedblue3.lmp')[1]][:947]);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=True;r.combat_lock=True;r.hitscan_priority=True
r.goto(-1380,-784,fire=True,rad=14,maxn=300)
r.face(0,n=40);r.step(b=2);r.step(n=100)
n=Nav(r.wad,8,20)
for end in [(-1100,-1160),(-1100,-1470)]:
 path=n.path((r.state['x'],r.state['y']),end,sectors=r.state['sectors']);print('PATH',path,flush=True)
 for p in path[1:]:
  if not r.goto(*p,fire=True,rad=14,maxn=350,stucklimit=300):break
r.face(270,n=40);r.step(b=2);r.step(n=10)
r.save('work/secret3.lmp');r.report();r.close()
