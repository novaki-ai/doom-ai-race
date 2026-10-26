from sim import Sim
from lmp import oku
from nav import Nav
r=Sim(7);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/shortsouth7.lmp')[1]][:3722]);n=Nav(r.wad,8,22)
for end in [(-48,-592),(-592,-1040),(-336,-1344),(-608,-96)]:
 try:print(end,n.path((r.state['x'],r.state['y']),end,sectors=r.state['sectors'],allow_lifts=False,forbidden_doors=[72]))
 except Exception as e:print(end,e)
r.close()
