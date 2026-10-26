from sim import Sim
from lmp import oku
from nav import Nav
r=Sim(3);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/mainexit3.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=True;r.combat_lock=True;r.hitscan_priority=True
n=Nav(r.wad,8,20)
for end in [(-1500,-1930),(-1500,-1870),(-1100,-1470)]:
 sec=[v[:] for v in r.state['sectors']]
 for i,s in enumerate(r.wad.sec):
  if s[0]==s[1] and sec[i][1]>sec[i][0]:sec[i][1]=max(sec[i][1],sec[i][0]+64)
 path=n.path((r.state['x'],r.state['y']),end,sectors=sec);print('PATH',path,flush=True)
 for p in path[1:]:
  if not r.goto(*p,fire=True,rad=14,maxn=350):break
r.face(270,n=20);r.step(b=2);r.step(n=10)
r.save('work/late_secret3.lmp');r.report();r.close()
