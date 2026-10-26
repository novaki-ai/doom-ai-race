from sim import Sim
from lmp import oku
import math,itertools,contextlib
base=[(f,s,a//256,b) for f,s,a,b in oku('work/boss8.lmp')[1]]
best=2100
for rx,ry,speed,lock,avoid in itertools.product([170,230,300],[170,240],[14,20],[True,False],[False]):
 r=Sim(8);r.replay(base);r.smartturn=True;r.weapon_policy=True;r.combat_range=800;r.avoid=avoid;r.combat_lock=lock
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  for k in range(100):
   a=k*math.tau/12;r.goto(416+rx*math.cos(a),3270+ry*math.sin(a),fire=True,rad=24,maxn=100,speed=speed,brake=.6)
   ghosts=[o for o in r.state['monsters'] if o[0]==13 and o[4]>0]
   if not ghosts or r.state['health']<=0 or len(r.t)>2300:break
 if not ghosts and r.state['health']>90 and len(r.t)<best:
  best=len(r.t);r.save('work/ghost8.lmp');print('BEST',rx,ry,speed,lock,avoid,best,r.state['health'],r.state['ammo'],flush=True)
 r.close()
