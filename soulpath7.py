from sim import Sim
from lmp import oku
from nav import Nav
r=Sim(7);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/rocket7.lmp')[1]]);n=Nav(r.wad,8,18)
print('actual',r.state['x'],r.state['y'],r.state['sectors'][119])
for end in [(-608,-96),(-336,-1344),(-640,-1400)]:
 try:print(n.path((r.state['x'],r.state['y']),end,sectors=r.state['sectors'],allow_lifts=False,forbidden_doors=[72]))
 except Exception as e:print(e)
r.close()
