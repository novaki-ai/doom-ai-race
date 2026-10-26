from sim import Sim
from lmp import oku
import itertools,contextlib
base=[(f,s,a//256,b) for f,s,a,b in oku('work/starkey5.lmp')[1]]
best=3805
for delay,avoid,lock,near,brake in itertools.product([0,3,7],[True,False],[False,True],[True,False],[.5,1]):
 r=Sim(5);r.replay(base);r.step(n=delay);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=avoid;r.combat_lock=lock;r.near=near;r.combat_range=600
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  for p in [(256,928),(128,1232),(104,1416),(0,1544),(0,1640),(56,1736),(56,1784),(32,1856),(-8,2064),(-64,2152),(-72,2272),(-152,2336),(-240,2336),(-256,2368),(-288,2456)]:
   if not r.goto(*p,fire=True,rad=20,maxn=250,stucklimit=180,speed=30,brake=brake):break
  r.face(90,n=10);r.step(b=2);r.step(n=10)
 if r.state['state']!=0 and len(r.t)<best:
  best=len(r.t);r.save('work/starfastend5.lmp');print('BEST',delay,avoid,lock,near,brake,best,r.state['health'],flush=True)
 r.close()
