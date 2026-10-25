from sim import Sim
from lmp import oku
import itertools,json
base=[(f,s,a//256,b) for f,s,a,b in oku('work/fastkey5.lmp')[1]]
for delay,avoid,lock,fire in itertools.product([0,1,3,7,12,20],[True,False],[False,True],[True,False]):
 r=Sim(5);r.replay(base);r.step(n=delay);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=avoid;r.combat_lock=lock
 for p in [(256,928),(128,1232),(104,1416),(0,1544),(0,1640),(56,1736),(56,1784),(32,1856),(-8,2064),(-64,2152),(-72,2272),(-152,2336),(-240,2336),(-256,2368),(-288,2456)]:
  if not r.goto(*p,fire=fire,rad=20,maxn=300,stucklimit=200):break
 r.face(90,n=14);r.step(b=2);r.step(n=10)
 if r.state['state']!=0:
  r.save('work/fastexit5.lmp');json.dump({'delay':delay,'avoid':avoid,'lock':lock,'fire':fire,'tics':len(r.t)},open('work/win5.json','w'));r.close();break
 r.close()
