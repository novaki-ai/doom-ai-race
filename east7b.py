from sim import Sim
from lmp import oku
from nav import Nav
r=Sim(7);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/main7.lmp')[1]][:2890]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
for p in [(96,-1400),(96,-1272),(264,-1200),(392,-1200),(816,-1120),(816,-832),(600,-832),(600,-704),(840,-704)]:
 if not r.goto(*p,fire=True,rad=12,maxn=350):break
else:
 n=Nav(r.wad,8,22)
 for end in [(-128,-448),(-992,272)]:
  path=n.path((r.state['x'],r.state['y']),end,sectors=r.state['sectors'],forbidden_doors=(72,));print('PATH',path,flush=True)
  for p in path[1:]:
   if not r.goto(*p,fire=True,rad=12,maxn=450):break
  else:continue
  break
 r.goto(-1016,272,fire=True,rad=10,maxn=80)
r.save('work/east7b.lmp');r.draw();r.report();r.close()
