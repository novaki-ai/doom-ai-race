from sim import Sim
from lmp import oku
from nav import Nav
r=Sim(6);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/recover6.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
n=Nav(r.wad,8,22)
for end in [(-1496,1384),(-2016,1800),(-2016,1984),(-1920,2016)]:
 sec=[v[:] for v in r.state['sectors']]
 for i,s in enumerate(r.wad.sec):
  if s[0]==s[1] and sec[i][1]>sec[i][0]:sec[i][1]=max(sec[i][1],sec[i][0]+64)
 try:path=n.path((r.state['x'],r.state['y']),end,sectors=sec)
 except Exception as e:print(e);break
 print('PATH',path,flush=True)
 for p in path[1:]:
  if not r.goto(*p,fire=True,rad=12,maxn=600,stucklimit=500):break
 else:
  if end==(-1496,1384):r.face(0,n=14);r.step(b=2);r.step(n=35)
  continue
 break
r.face(0,n=14);r.step(b=2);r.step(n=10)
r.save('work/exit6.lmp');r.draw();r.report();r.close()
