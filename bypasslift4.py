from sim import Sim
import itertools,contextlib
best=498
routes=[[(1360,1184),(1184,1376),(1184,1456),(1136,1496),(608,1712),(296,1712),(144,1600),(32,1448),(32,1368),(0,1208),(-536,704),(-560,696)],[(1500,1000),(1440,704),(1440,504),(1408,480),(1184,256),(1184,120),(1152,96),(704,-96),(112,-96),(0,128),(-560,696)]]
for route,fire,brake in itertools.product(range(2),[False,True],[.5,1,.3]):
 r=Sim(4);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=True;r.combat_lock=True;r.hitscan_priority=True
 with open('/dev/null','w') as out,contextlib.redirect_stdout(out):
  for p in [(1900,1150),(1770,1150)]+routes[route]+[(-640,904),(-640,1032),(-296,1328),(-296,1416),(-368,1552),(-448,1592),(-480,1640),(-550,1790),(-550,1888)]:
   if not r.goto(*p,fire=fire or p[0]<-250 and p[1]>1300,rad=14 if p in [(1184,1456),(0,1208),(-448,1592)] else 22,maxn=200,speed=30,brake=brake):break
 print('TRY',route,fire,brake,len(r.t),r.state['health'],round(r.state['x']),round(r.state['y']),flush=True)
 if r.state['health']>=30 and abs(r.state['x']+550)<40 and abs(r.state['y']-1888)<40 and len(r.t)<best:
  best=len(r.t);r.save('work/bypasslift4.lmp');print('BEST',best,r.state['health'],flush=True)
 r.close()
