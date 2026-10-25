from sim import Sim
from lmp import oku
from nav import Nav
r=Sim(6);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/recover6.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=True;r.combat_lock=True;r.hitscan_priority=True;r.combat_range=800
n=Nav(r.wad,8,24)
for end in [(400,1728),(272,1728)]:
 path=n.path((r.state['x'],r.state['y']),end,sectors=r.state['sectors'],forbidden_doors=[62]);print('PATH',path,flush=True)
 for p in path[1:]:
  if not r.goto(*p,fire=True,rad=14,maxn=300,stucklimit=200):break
r.save('work/rightsoul6.lmp');r.report();r.draw();r.close()
