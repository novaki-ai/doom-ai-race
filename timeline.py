from sim import Sim
from lmp import oku
import sys
m=int(sys.argv[1]);r=Sim(m)
for i,(f,s,a,b) in enumerate(oku('submit/E1M%d.lmp'%m)[1]):
 r.step(f,s,a//256,b)
 if i%100==0:print(i,r.state['health'],r.state['armor'],r.state['ammo'][1],r.state['keys'][:3],round(r.state['x']),round(r.state['y']),r.state['z'],r.state['sector'],flush=True)
r.close()
