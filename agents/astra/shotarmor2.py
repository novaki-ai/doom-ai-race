from sim import Sim
from lmp import oku
base=[(f,s,a//256,b) for f,s,a,b in oku('work/shotdebug2.lmp')[1]]
r=Sim(2);r.replay(base[:793])
for t in base[793:]:
 r.step(*t)
 if r.state['armor']>=90:break
r.save('work/shotarmor2.lmp');r.report();r.close()
