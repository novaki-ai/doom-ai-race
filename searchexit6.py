from sim import Sim
from lmp import oku
import itertools,json
base=[(f,s,a//256,b) for f,s,a,b in oku('work/recover6.lmp')[1]];best=0
for delay,avoid,lock,fire in itertools.product([0,1,3,7,12,20],[False,True],[False,True],[True,False]):
 r=Sim(6);r.replay(base);r.step(n=delay);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=avoid;r.combat_lock=lock
 for p in [(-96,1816),(-312,1568),(-512,1480),(-544,1336),(-576,1312),(-928,1320),(-960,1280),(-992,1368),(-1192,1432),(-1440,1496),(-1648,1496),(-1664,1472),(-1664,1400),(-1640,1384),(-1496,1384)]:
  if not r.goto(*p,fire=fire,rad=12,maxn=240):break
 if r.state['health']>best and r.state['x']<-1470 and r.state['x']>-1530 and abs(r.state['y']-1384)<25:
  r.face(0,n=14);r.step(b=2);r.step(n=35);best=r.state['health'];r.save('work/searchend6.lmp');json.dump({'health':best,'delay':delay,'avoid':avoid,'lock':lock,'fire':fire,'tics':len(r.t)},open('work/searchend6.json','w'));print('BEST',best,flush=True)
 r.close()
 if best>=45:break
