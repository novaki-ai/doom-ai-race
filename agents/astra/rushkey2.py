from sim import Sim
import itertools,contextlib
best=900
for delay,fire,avoid in itertools.product([0,3,7,12,20],[False,True],[True,False]):
 r=Sim(2);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=avoid;r.combat_lock=True;r.hitscan_priority=True;r.step(n=delay)
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  for p in [(400,-10),(780,0),(920,0),(1450,0),(1500,350),(1140,352),(1500,350),(1450,0),(900,0),(700,0),(600,600),(0,976)]:
   if not r.goto(*p,fire=fire,rad=22,maxn=250,speed=30,brake=1):break
 if r.state['keys'][2] and r.state['armor']>=90 and r.state['health']>=30 and len(r.t)<best:
  best=len(r.t);r.save('work/rushkey2.lmp');print('BEST',delay,fire,avoid,len(r.t),r.state['health'],r.state['owned'],flush=True)
 r.close()
