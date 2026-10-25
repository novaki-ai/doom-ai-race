from sim import Sim
from lmp import oku
import itertools,json
prefix=[(f,s,a//256,b) for f,s,a,b in oku('work/west5.lmp')[1]][:1417]
best=-1
for delay,avoid,lock,fire in itertools.product(range(15),[False,True],[False,True],[True,False]):
 r=Sim(5);r.replay(prefix);r.smartturn=True;r.auto_doors=True;r.avoid=avoid;r.combat_lock=lock;r.weapon_policy=True
 r.step(n=delay)
 for p in [(-750,832),(-1000,832)]:
  if not r.goto(*p,fire=fire,rad=20):break
 score=r.state['health'] if r.state['x']<-970 else -1
 if score>best:
  best=score;r.save('work/searchgate5.lmp');open('work/searchgate5.json','w').write(json.dumps({'health':score,'delay':delay,'avoid':avoid,'lock':lock,'fire':fire,'tics':len(r.t)}));print('BEST',score,flush=True)
 r.close()
 if best>=60:break
