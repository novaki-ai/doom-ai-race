from sim import Sim
from lmp import oku
from nav import Nav
r=Sim(7);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/main7.lmp')[1]][:2890]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
n=Nav(r.wad,8,22)
for end in [(840,-704),(-128,-448),(-992,272)]:
 try:path=n.path((r.state['x'],r.state['y']),end,sectors=r.state['sectors'],forbidden_doors=(72,))
 except Exception as e:print(e);break
 print('PATH',path,flush=True)
 for p in path[1:]:
  if not r.goto(*p,fire=True,rad=12,maxn=180,stucklimit=120) and ((r.state['x']-p[0])**2+(r.state['y']-p[1])**2)>30**2:break
 else:continue
 break
r.goto(-1016,272,fire=True,rad=10,maxn=80)
r.save('work/east7.lmp');r.draw();r.report();r.close()
