from sim import Sim
import itertools,contextlib
best=434
for brake,rad in itertools.product([.5,1,100],[16,24,32]):
 fire=False;avoid=True;speed=30
 r=Sim(1);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=avoid;r.combat_lock=True;r.hitscan_priority=True
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  for p in [(1250,-3000),(1336,-2736),(1352,-2584),(1472,-2536),(1672,-2536),(2328,-2664),(2528,-2664),(2768,-2768),(2904,-2880),(2968,-3688),(3000,-3960),(3044,-4110),(3000,-4550),(3000,-4688),(2944,-4768)]:
   if not r.goto(*p,fire=fire,rad=rad,speed=speed,maxn=250,brake=brake):break
  r.face(180,n=8);r.step(b=2);r.step(n=10)
 print('TRY',brake,rad,r.state['health'],len(r.t),r.state['state'],r.state['x'],r.state['y'],flush=True)
 if r.state['state']!=0 and len(r.t)<best:best=len(r.t);r.save('work/nobrake1.lmp');r.report()
 r.close()
