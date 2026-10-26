from sim import Sim
from lmp import oku
from nav import Nav
r=Sim(6);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/lateback6.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
n=Nav(r.wad,8,20)
for end in [(272,1728),(-1496,1384)]:
 path=n.path((r.state['x'],r.state['y']),end,sectors=r.state['sectors']);print('PATH',path,flush=True)
 for p in path[1:]:
  if not r.goto(*p,fire=True,rad=12,maxn=600,stucklimit=500):break
 else:continue
 break
r.face(0,n=14);r.step(b=2);r.step(n=35)
r.save('work/latesoul6.lmp');r.draw();r.report();r.close()
