from sim import Sim
from lmp import oku
r=Sim(8)
for i,(f,s,a,b) in enumerate(oku('submit/E1M8.lmp')[1]):
 r.step(f,s,a//256,b)
 if i%100==0:
  bs=[o[4] for o in r.state['monsters'] if o[0]==15 and o[4]>0];sp=sum(o[4]>0 and o[0]==13 for o in r.state['monsters'])
  print(i,r.state['health'],r.state['ammo'][1],r.state['kills'],sp,bs,round(r.state['x']),round(r.state['y']),flush=True)
r.close()
