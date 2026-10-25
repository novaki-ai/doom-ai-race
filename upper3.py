from sim import Sim
from lmp import oku
import itertools,json
base=[(f,s,a//256,b) for f,s,a,b in oku('work/gearedblue3.lmp')[1]][:947];best=0
for delay,avoid,lock,fire in itertools.product([0,1,3,5,8,12,20],[False,True],[False,True],[False,True]):
 r=Sim(3);r.replay(base);r.step(n=delay);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=avoid;r.combat_lock=lock
 for p in [(-1450,-768),(-1350,-700),(-1240,-632),(-1080,-620),(-960,-648),(-860,-704),(-792,-768),(-688,-704),(-576,-672),(-496,-672),(-416,-512),(-416,-432),(-384,-416),(-328,-416),(-168,-456),(-160,-488),(-160,-864)]:
  if not r.goto(*p,fire=fire,rad=10,maxn=200):break
 if r.state['keys'][0] and r.state['health']>best:
  best=r.state['health'];r.save('work/upper3.lmp');json.dump({'delay':delay,'avoid':avoid,'lock':lock,'fire':fire,'health':best,'tics':len(r.t)},open('work/upper3.json','w'));print('BEST',best,flush=True)
 r.close()
 if best>=35:break
