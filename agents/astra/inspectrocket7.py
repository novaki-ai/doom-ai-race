from sim import Sim
from lmp import oku
r=Sim(7);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/rocketswitch7.lmp')[1]]);r.report();print('door104',r.state['sectors'][104]);r.close()
