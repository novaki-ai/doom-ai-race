from sim import Sim
from lmp import oku
r=Sim(4)
for i,(f,s,a,b) in enumerate(oku('submit/E1M4.lmp')[1]):
 r.step(f,s,a//256,b)
 if i>550 and i%20==0:print(i,r.state['health'],round(r.state['x']),round(r.state['y']),r.state['z'],r.state['sector'],flush=True)
r.close()
