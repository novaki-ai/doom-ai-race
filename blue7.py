from sim import Sim
from lmp import oku
from nav import Nav
r=Sim(7);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/west7.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
n=Nav(r.wad,8,20)
for end in [(-1152,-576),(-608,-96),(-1024,272)]:
 sec=[v[:] for v in r.state['sectors']]
 for i,s in enumerate(r.wad.sec):
  if s[0]==s[1] and sec[i][1]>sec[i][0]:sec[i][1]=max(sec[i][1],sec[i][0]+64)
 try:path=n.path((r.state['x'],r.state['y']),end,sectors=sec)
 except Exception as e:print(e);break
 print('PATH',path,flush=True)
 for p in path[1:]:
  if not r.goto(*p,fire=True,rad=12,maxn=600,stucklimit=500):break
 else:continue
 break
r.save('work/blue7.lmp');r.draw();r.report();r.close()
