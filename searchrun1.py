from sim import Sim
import itertools,contextlib
best=418
for delay,dist,rad in itertools.product(range(0,21,2),[40,52,62],[24,32]):
 r=Sim(1);r.step(n=delay);r.smartturn=True;r.auto_doors=True;r.auto_dist=dist;r.avoid=True
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  for p in [(1312,-2880),(1352,-2584),(1472,-2536),(1672,-2536),(2328,-2664),(2528,-2664),(2768,-2768),(2904,-2880),(2968,-3688),(3000,-3960),(3044,-4110),(3000,-4550),(3000,-4688),(2944,-4768)]:
   if not r.goto(*p,fire=False,rad=rad,speed=30,maxn=250,brake=1):break
  r.face(180,n=8);r.step(b=2);r.step(n=10)
 if r.state['state']!=0 and len(r.t)<best:
  best=len(r.t);r.save('work/run1.lmp');print('BEST',delay,dist,rad,len(r.t),r.state['health'],flush=True)
 r.close()
