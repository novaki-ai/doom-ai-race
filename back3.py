from sim import Sim
from lmp import oku
from nav import Nav
r=Sim(3);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/searchblue3.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=False
n=Nav(r.wad,8,24)
for end in [(-832,-736),(-1760,-992),(-1280,-2400)]:
 try:path=n.path((r.state['x'],r.state['y']),end,sectors=r.state['sectors'])
 except Exception as e:print(e);break
 print('PATH',path,flush=True)
 for p in path[1:]:
  if not r.goto(*p,fire=True,rad=12,maxn=300):break
 else:continue
 break
r.save('work/back3.lmp');r.draw();r.report();r.close()
