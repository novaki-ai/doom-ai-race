from sim import Sim
from lmp import oku
import itertools,json
base=[(f,s,a//256,b) for f,s,a,b in oku('work/upper3.lmp')[1]];best=0
for delay,avoid,fire in itertools.product([0,1,3,7,12,20],[False,True],[False,True]):
 r=Sim(3);r.replay(base);r.step(n=delay);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=avoid
 for p in [(-160,-488),(-168,-456),(-328,-416),(-384,-416),(-416,-432),(-416,-512),(-496,-672),(-576,-672),(-688,-704),(-832,-736),(-860,-704),(-960,-648),(-1080,-620),(-1240,-632),(-1350,-700),(-1450,-768),(-1615,-803),(-1700,-820),(-1760,-992),(-1824,-1496),(-1856,-1608),(-1880,-1744),(-1864,-2040),(-1864,-2400),(-1896,-2440),(-1896,-2488),(-1824,-3024),(-1792,-3040),(-1208,-3040),(-1192,-3016),(-1192,-2616),(-1304,-2544),(-1344,-2528)]:
  if not r.goto(*p,fire=fire,rad=12,maxn=200):break
 if r.state['health']>best and r.state['x']>-1400 and r.state['y']<-2450:
  best=r.state['health'];r.save('work/returnsearch3.lmp');json.dump({'delay':delay,'avoid':avoid,'fire':fire,'health':best,'tics':len(r.t)},open('work/returnsearch3.json','w'));print('BEST',best,flush=True)
 r.close()
 if best>=25:break
