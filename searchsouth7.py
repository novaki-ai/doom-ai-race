from sim import Sim
from lmp import oku
import itertools,json
base=[(f,s,a//256,b) for f,s,a,b in oku('work/east7b.lmp')[1]];best=0
for delay,avoid,lock,fire in itertools.product([0,1,3,7,12,20],[False,True],[False,True],[True,False]):
 r=Sim(7);r.replay(base);r.step(n=delay);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=avoid;r.combat_lock=lock
 for p in [(-592,304),(-416,296),(-384,280),(-104,240),(96,136),(624,160),(184,-264),(184,-280),(160,-384),(136,-416),(920,-448),(992,-528),(976,-632),(840,-704),(600,-704),(600,-832),(816,-832),(816,-1120),(392,-1200),(96,-1272),(96,-1424),(392,-1640),(592,-1640),(648,-1688),(664,-1728)]:
  if not r.goto(*p,fire=fire,rad=12,maxn=250):break
 if r.state['health']>best and r.state['x']>640 and -1750<r.state['y']<-1700:
  best=r.state['health'];r.save('work/searchsouth7.lmp');json.dump({'delay':delay,'avoid':avoid,'lock':lock,'fire':fire,'health':best,'tics':len(r.t)},open('work/searchsouth7.json','w'));print('BEST',best,flush=True)
 r.close()
 if best>=40:break
