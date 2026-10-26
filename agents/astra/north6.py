from sim import Sim
from lmp import oku
from nav import Nav
r=Sim(6);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/searchroom6.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
n=Nav(r.wad,8,22)
for end in [(736,-816),(-64,2328)]:
 path=n.path((r.state['x'],r.state['y']),end,sectors=r.state['sectors']);print('PATH',path,flush=True)
 for p in path[1:]:
  if not r.goto(*p,fire=True,rad=12,maxn=650,stucklimit=550):break
 else:continue
 break
r.face(90,n=14);r.step(b=2);r.step(n=10)
r.save('work/north6.lmp');r.draw();r.report();r.close()
