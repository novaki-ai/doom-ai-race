from sim import Sim
from lmp import oku
r=Sim(6);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/yellow6b.lmp')[1]][:1866]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
from nav import Nav
n=Nav(r.wad,8,22)
for end in [(-672,-320),(-704,-256),(-736,-256),(1760,-192)]:
 try:path=n.path((r.state['x'],r.state['y']),end,sectors=r.state['sectors'])
 except Exception as e:print(e);break
 print('PATH',path,flush=True)
 for p in path[1:]:
  if not r.goto(*p,fire=True,rad=22,maxn=500,stucklimit=400):break
 else:continue
 break
r.save('work/main6.lmp');r.draw();r.report();r.close()
