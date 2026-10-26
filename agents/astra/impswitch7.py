from sim import Sim
from lmp import oku
import itertools,contextlib,math
base=[(f,s,a//256,b) for f,s,a,b in oku('work/debugswitch7.lmp')[1]][:4252]
best=0
for delay,avoid,pri in itertools.product([0,1,3,7],[True,False],[True,False]):
 r=Sim(7);r.replay(base);r.step(n=delay);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=avoid;r.combat_lock=True;r.hitscan_priority=pri;r.combat_range=700
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  imp=min([o for o in r.state['monsters'] if o[0]==11 and o[4]>0],key=lambda o:math.hypot(o[1]-r.state['x'],o[2]-r.state['y']))
  uid=imp[9]
  for k in range(100):
   imp=next((o for o in r.state['monsters'] if o[9]==uid and o[4]>0),None)
   if imp is None or r.state['health']<=0:break
   r.goto(r.state['x']+100,r.state['y'],speed=0,shoot_at=(imp[1],imp[2]),maxn=1)
  for p in [(96,-2440),(280,-2376),(400,-2368),(448,-2256),(352,-2160),(336,-2112),(448,-2016),(496,-1872),(352,-1760)]:
   if not r.goto(*p,fire=True,rad=14,maxn=250):break
  if r.state['health']>0 and abs(r.state['x']-352)<40 and abs(r.state['y']+1760)<40:
   r.face(90,n=20);r.step(b=2);r.step(n=10)
   if r.state['health']>best:
    best=r.state['health'];r.save('work/impswitch7.lmp');open('work/impswitch7.best','w').write(str((delay,avoid,pri,len(r.t),best)))
 r.close()
 if best>=35:break
