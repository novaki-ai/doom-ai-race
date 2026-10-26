from sim import Sim
from lmp import oku
from nav import Nav
r=Sim(7);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/rocket7.lmp')[1]][:2742]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
for p in [(-800,-1520),(-624,-1880),(-560,-1952),(-256,-1984),(-160,-2020),(-72,-1960),(0,-1952),(48,-1936),(128,-1880),(160,-1856),(160,-1680),(96,-1544),(96,-1088),(-120,-800),(-400,-800),(-416,-768),(-416,-448)]:
 if not r.goto(*p,fire=True,rad=12,maxn=350):break
n=Nav(r.wad,8,20)
for end in [(-128,-448),(-992,272)]:
 try:path=n.path((r.state['x'],r.state['y']),end,sectors=r.state['sectors'],forbidden_doors=(72,))
 except Exception as e:print(e);break
 print('PATH',path,flush=True)
 for p in path[1:]:
  if not r.goto(*p,fire=True,rad=12,maxn=450):break
 else:continue
 break
r.goto(-1016,272,fire=True,rad=10,maxn=60)
r.save('work/main7.lmp');r.draw();r.report();r.close()
