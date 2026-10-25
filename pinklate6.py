from sim import Sim
from lmp import oku
import math,contextlib
r=Sim(6);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/latesoul6.lmp')[1]][:5013]);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=False
with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
 for k in range(90):
  enemies=[o for o in r.state['monsters'] if o[0]==12 and o[4]>0 and math.hypot(o[1]-r.state['x'],o[2]-r.state['y'])<150]
  if not enemies:break
  o=min(enemies,key=lambda o:math.hypot(o[1]-r.state['x'],o[2]-r.state['y']))
  r.goto(-1664,1424,shoot_at=(o[1],o[2]),rad=8,maxn=1,stucklimit=500)
for p in [(-1664,1400),(-1640,1384)]:r.goto(*p,fire=False,rad=16,maxn=100)
r.goto(-1496,1384,shoot_at=(-1552,1392),rad=14,maxn=180)
r.face(0,n=20);r.step(b=2);r.step(n=10)
r.save('work/pinklate6.lmp');r.report();r.close()
