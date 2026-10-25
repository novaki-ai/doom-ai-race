from sim import Sim
from lmp import oku
from nav import Nav
r=Sim(6);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/late6.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=True;r.combat_lock=True;r.hitscan_priority=True;r.combat_range=700
for p in [(1152,-700),(1220,-760)]:r.goto(*p,fire=True,rad=14,maxn=250)
n=Nav(r.wad,8,22)
for end in [(1128,144),(400,1728),(272,1728)]:
 sec=[v[:] for v in r.state['sectors']]
 for i,s in enumerate(r.wad.sec):
  if s[0]==s[1] and sec[i][1]>sec[i][0]:sec[i][1]=max(sec[i][1],sec[i][0]+64)
 path=n.path((r.state['x'],r.state['y']),end,sectors=sec,forbidden_doors=[62]);print('PATH',path,flush=True)
 for p in path[1:]:
  if not r.goto(*p,fire=True,rad=14,maxn=350,stucklimit=300):break
r.save('work/eastsoul6.lmp');r.report();r.close()
