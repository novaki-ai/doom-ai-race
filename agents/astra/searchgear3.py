from sim import Sim
from lmp import oku
import itertools,json
prefix=[(f,s,a//256,b) for f,s,a,b in oku('work/base3.lmp')[1]]
best=-100
for delay,avoid,lock in itertools.product(range(21),[False,True],[False,True]):
 r=Sim(3);r.replay(prefix);r.smartturn=True;r.auto_doors=True;r.avoid=avoid;r.combat_lock=lock
 r.step(n=delay)
 for p in [(-2070,-2000),(-2130,-1940),(-2144,-1800),(-2144,-1760),(-2144,-1600)]:
  if not r.goto(*p,fire=True,rad=16):break
 score=r.state['health'] if r.state['armor']>50 and r.state['y']>-1700 else -100
 if score>best:
  best=score;r.save('work/searchgear3.lmp');open('work/searchgear3.json','w').write(json.dumps({'health':score,'delay':delay,'avoid':avoid,'lock':lock,'tics':len(r.t)}));print('BEST',score,delay,avoid,lock,flush=True)
 r.close()
 if best>=60:break
