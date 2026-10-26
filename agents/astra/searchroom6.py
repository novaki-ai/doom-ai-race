from sim import Sim
from lmp import oku
import itertools,json
base=[(f,s,a//256,b) for f,s,a,b in oku('work/key6.lmp')[1]][:3137];best=0
for delay,avoid,lock,fire in itertools.product([0,1,3,5,8,12,20],[False,True],[False,True],[True,False]):
 r=Sim(6);r.replay(base);r.step(n=delay);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=avoid;r.combat_lock=lock
 for p in [(800,-750),(736,-816),(800,-880),(920,-912),(992,-880),(992,-760),(1088,-608)]:
  if not r.goto(*p,fire=fire,rad=18,maxn=250):break
 if r.state['keys'][1] and r.state['health']>best:
  best=r.state['health'];r.save('work/searchroom6.lmp');json.dump({'delay':delay,'avoid':avoid,'lock':lock,'fire':fire,'health':best,'tics':len(r.t)},open('work/searchroom6.json','w'));print('BEST',best,flush=True)
 r.close()
 if best>=50:break
