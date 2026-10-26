from sim import Sim
from lmp import oku
from nav import Nav
r=Sim(6);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/searchroom6.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
n=Nav(r.wad,8,22)
for end in [(1616,-608),(1712,-608),(1760,-192),(1160,-224),(-320,128),(-540,128),(-540,480),(-448,992),(-64,2328)]:
 try:path=n.path((r.state['x'],r.state['y']),end,sectors=r.state['sectors'])
 except Exception as e:print(e);break
 print('PATH',path,flush=True)
 for p in path[1:]:
  if not r.goto(*p,fire=True,rad=12,maxn=500,stucklimit=400):break
 else:continue
 break
r.face(90,n=14);r.step(b=2);r.step(n=10)
r.save('work/safe6.lmp');r.draw();r.report();r.close()
