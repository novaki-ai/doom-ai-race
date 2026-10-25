from sim import Sim
from lmp import oku
import itertools,json
base=[(f,s,a//256,b) for f,s,a,b in oku('work/key5.lmp')[1]][:3027];best=0
for delay,avoid,lock,fire in itertools.product([0,1,3,7,12,20,30],[False,True],[False,True],[True,False]):
 r=Sim(5);r.replay(base);r.step(n=delay);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=avoid;r.combat_lock=lock
 for p in [(400,856),(696,1048),(880,1112),(1376,1096),(1432,1032),(1456,904),(1536,888),(1560,920),(1560,1352),(1520,1392),(1448,1400),(976,1400),(328,1336),(280,1304),(272,1272),(192,1040)]:
  if not r.goto(*p,fire=fire,rad=22,maxn=220):break
 if r.state['keys'][0] and r.state['health']>best:
  best=r.state['health'];r.save('work/searchkey5.lmp');json.dump({'health':best,'delay':delay,'avoid':avoid,'lock':lock,'fire':fire,'tics':len(r.t)},open('work/searchkey5.json','w'));print('BEST',best,flush=True)
 r.close()
 if best>=80:break
