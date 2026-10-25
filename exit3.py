from sim import Sim
from lmp import oku
from nav import Nav
r=Sim(3);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/mainexit3.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
r.goto(-704,-2144,fire=True,rad=10,maxn=500);r.face(0,n=40);r.step(b=2);r.step(n=15)
n=Nav(r.wad,8,20)
for end in [(-448,-1600),(-200,-1600),(576,-1600),(704,-1680)]:
 sec=[v[:] for v in r.state['sectors']]
 for i,s in enumerate(r.wad.sec):
  if s[0]==s[1] and sec[i][1]>sec[i][0]:sec[i][1]=max(sec[i][1],sec[i][0]+64)
 try:path=n.path((r.state['x'],r.state['y']),end,sectors=sec)
 except Exception as e:print(e);break
 print('PATH',path,flush=True)
 for p in path[1:]:
  if not r.goto(*p,fire=True,rad=12,maxn=500,stucklimit=400):break
 else:continue
 break
r.goto(704,-1728,fire=True,rad=10,maxn=200);r.face(270,n=40);r.step(b=2);r.step(n=10)
r.save('work/exit3.lmp');r.draw();r.report();r.close()
