from sim import Sim
from lmp import oku
import itertools,json,contextlib
base=[(f,s,a//256,b) for f,s,a,b in oku('work/route8.lmp')[1]][:430]
best=0
for approach,delay,avoid,fire in itertools.product(range(3),range(0,161,20),[False,True],[True,False]):
 r=Sim(8);r.replay(base);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=avoid
 r.goto(416,928,fire=True)
 if delay:r.goto(416 if approach==0 else 520,1100 if approach<2 else 750,fire=True,rad=1,maxn=delay,stucklimit=500)
 for p in [(168,896),(-160,864),(-96,928),(-96,800),(-32,864),(168,880),(416,864),(416,1400)]:
  if not r.goto(*p,fire=fire,rad=20,maxn=180):break
 if r.state['health']>best and r.state['y']>1350 and r.state['owned'][2]:
  best=r.state['health'];r.save('work/search8.lmp');json.dump({'health':best,'approach':approach,'delay':delay,'avoid':avoid,'fire':fire,'tics':len(r.t)},open('work/search8.json','w'));print('BEST',best,flush=True)
 r.close()
 if best>=130:break
