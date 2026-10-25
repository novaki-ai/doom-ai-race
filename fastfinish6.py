from sim import Sim
from lmp import oku
import itertools,json
base=[(f,s,a//256,b) for f,s,a,b in oku('work/pinklate6.lmp')[1]]
for delay,avoid,lock,fire in itertools.product([0,1,3,7,12,20],[False,True],[False,True],[True,False]):
 r=Sim(6);r.replay(base);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=avoid;r.combat_lock=lock;r.step(n=delay)
 for p in [(-1648,1384),(-1840,1540),(-1984,1520),(-2016,1584),(-2016,1800),(-2016,1880),(-2016,1940),(-1944,1952),(-1920,2016)]:
  if not r.goto(*p,fire=fire,rad=12,maxn=300):break
 r.face(0,n=40);r.step(b=2);r.step(n=10)
 if r.state['state']!=0:
  r.save('work/fastwin6.lmp');json.dump({'delay':delay,'avoid':avoid,'lock':lock,'fire':fire,'tics':len(r.t)},open('work/win6.json','w'));r.close();break
 r.close()
