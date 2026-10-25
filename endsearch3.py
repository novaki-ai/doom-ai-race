from sim import Sim
from lmp import oku
import itertools,json
base=[(f,s,a//256,b) for f,s,a,b in oku('work/mainexit3.lmp')[1]]
for delay,avoid,lock,fire in itertools.product([0,1,3,7,12,20],[False,True],[False,True],[True,False]):
 r=Sim(3);r.replay(base);r.step(n=delay);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=avoid;r.combat_lock=lock
 for p in [(-1216,-2104),(-992,-1904),(-992,-1880),(-888,-1824),(-800,-1824),(-448,-1600),(-400,-1760),(-200,-1856),(448,-1792),(-200,-1856),(-400,-1760),(-448,-1600),(-200,-1600),(0,-1600),(480,-1600),(576,-1600),(704,-1600),(704,-1728)]:
  if not r.goto(*p,fire=fire,rad=14,maxn=300,stucklimit=250):break
 r.face(270,n=40);r.step(b=2);r.step(n=10)
 if r.state['state']!=0:
  r.save('work/win3.lmp');json.dump({'delay':delay,'avoid':avoid,'lock':lock,'fire':fire,'tics':len(r.t)},open('work/win3.json','w'));r.close();break
 r.close()
