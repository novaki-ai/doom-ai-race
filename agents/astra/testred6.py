from sim import Sim
from lmp import oku
from nav import Nav
r=Sim(6);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/red6.lmp')[1]]);r.report()
print([(i,s,r.state['sectors'][i]) for i,s in enumerate(r.wad.sec) if s[-1] in [4,9,10] or i in [241,242]])
r.step(n=100);n=Nav(r.wad,8,20)
try:print(n.path((r.state['x'],r.state['y']),(2624,-2240),sectors=r.state['sectors']))
except Exception as e:print(e)
r.close()
