from sim import Sim
from lmp import oku
r=Sim(4)
for i,(f,s,a,b) in enumerate(oku('submit/E1M4.lmp')[1]):
 r.step(f,s,a//256,b)
 if 790<i<835:print(i,round(r.state['x'],2),round(r.state['y'],2),round(r.state['z'],2),round(r.state['vx'],2),round(r.state['vy'],2),f,s,a//256,b,flush=True)
 if i>=835:break
r.close()
