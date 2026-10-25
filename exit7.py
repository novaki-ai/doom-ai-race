from sim import Sim
from lmp import oku
from nav import Nav
r=Sim(7);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/clear7.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True;r.combat_lock=True;r.hitscan_priority=True;r.combat_range=900
n=Nav(r.wad,8,20)
for end in [(1712,-2256),(1920,-2304)]:
 sec=[v[:] for v in r.state['sectors']]
 for i,s in enumerate(r.wad.sec):
  if s[0]==s[1] and sec[i][1]>sec[i][0]:sec[i][1]=max(sec[i][1],sec[i][0]+64)
 path=n.path((r.state['x'],r.state['y']),end,sectors=sec);print('PATH',path,flush=True)
 for p in path[1:]:
  if not r.goto(*p,fire=True,rad=14,maxn=450,stucklimit=350):break
 else:continue
 break
r.face(0,n=40);r.step(b=2);r.step(n=10)
r.save('work/exit7.lmp');r.draw();r.report();r.close()
