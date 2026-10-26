from sim import Sim
from lmp import oku
import itertools,contextlib,math
base=[(f,s,a//256,b) for f,s,a,b in oku('work/exit3b.lmp')[1]][:2570]
best=0
for delay,mode,avoid,pri in itertools.product([0,3,7,12,20,30],range(4),[False,True],[True,False]):
 r=Sim(3);r.replay(base);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=avoid;r.combat_lock=True;r.hitscan_priority=pri;r.combat_range=1100;r.step(n=delay)
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  if mode==0:route=[(-200,-1600),(0,-1600)]
  elif mode==1:route=[(-200,-1600),(-160,-1800),(128,-1800),(128,-1400),(-160,-1400),(-160,-1800),(128,-1800),(128,-1400),(128,-1600)]
  elif mode==2:route=[(-600,-1624),(-440,-1600),(-200,-1600),(-160,-1800),(128,-1800),(128,-1600)]
  else:route=[(-200,-1600),(0,-1600),(-160,-1600),(-400,-1600),(-160,-1600),(0,-1600)]
  for p in route:
   if not r.goto(*p,fire=True,rad=14,maxn=350,stucklimit=300):break
  if r.state['health']>0:
   for p in [(480,-1600),(480,-1728),(448,-1792),(560,-1600),(704,-1600),(704,-1728)]:
    if not r.goto(*p,fire=True,rad=14,maxn=650,stucklimit=600):break
  r.face(270,n=40);r.step(b=2);r.step(n=10)
 score=r.state['x']+r.state['health']*5
 if score>best:
  best=score;r.save('work/beststair3.lmp');print('BEST',delay,mode,avoid,pri,flush=True);r.report()
 if r.state['state']!=0:
  r.save('work/win3.lmp');r.report();r.close();break
 r.close()
