from sim import Sim
from lmp import oku
from nav import Nav
r=Sim(7);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/east7b.lmp')[1]]);n=Nav(r.wad,8,24)
for end in [(392,-1640),(352,-1760),(1920,-2304)]:
 try:print(end,n.path((r.state['x'],r.state['y']),end,sectors=r.state['sectors'],allow_lifts=False,forbidden_doors=[72]))
 except Exception as e:print(e)
r.close()
