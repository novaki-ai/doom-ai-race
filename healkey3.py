from sim import Sim
from lmp import oku
import itertools,json
base=[(f,s,a//256,b) for f,s,a,b in oku('work/searchblue3.lmp')[1]];best=0
for delay,avoid,lock,fire in itertools.product([0,1,3,7,12,20],[False,True],[False,True],[False,True]):
 r=Sim(3);r.replay(base);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=avoid;r.combat_lock=lock;r.step(n=delay)
 for p in [(-160,-704),(-264,-704),(-264,-560),(-272,-528),(-304,-528),(-264,-704),(-160,-704),(-160,-488),(-192,-448),(-352,-416),(-400,-416),(-480,-576),(-480,-656),(-512,-672),(-688,-704),(-832,-736)]:
  if not r.goto(*p,fire=fire,rad=12,maxn=180):break
 if r.state['health']>best and r.state['x']<-800:
  best=r.state['health'];r.save('work/healkey3.lmp');json.dump({'delay':delay,'avoid':avoid,'lock':lock,'fire':fire,'health':best,'tics':len(r.t)},open('work/healkey3.json','w'));print('BEST',best,flush=True)
 r.close()
 if best>=35:break
