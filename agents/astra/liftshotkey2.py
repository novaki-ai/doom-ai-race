from sim import Sim
import itertools,contextlib
best=1200
for delay,avoid,brake in itertools.product([0,3,7,12],[True,False],[1,.5]):
 r=Sim(2);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=avoid;r.combat_lock=True;r.hitscan_priority=True;r.step(n=delay)
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  for p in [(-32,20),(-32,264),(-64,288),(-144,288),(-160,320),(-176,496),(-160,304),(-112,280),(-56,280),(32,192),(48,160),(400,-10),(780,0),(920,0),(1450,0),(1500,350),(1140,352),(1500,350),(1450,0),(900,0),(700,0),(600,600),(0,700),(0,976)]:
   if not r.goto(*p,fire=True,rad=12,maxn=500,stucklimit=400,speed=30,brake=brake):break
 if r.state['keys'][2] and r.state['armor']>=90 and r.state['health']>=30 and len(r.t)<best:
  best=len(r.t);r.save('work/liftshotkey2.lmp');print('BEST',delay,avoid,brake,len(r.t),r.state['health'],r.state['ammo'],flush=True)
 r.close()
