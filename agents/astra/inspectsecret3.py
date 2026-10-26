from sim import Sim
from lmp import oku
from nav import Nav
r=Sim(3);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/base3.lmp')[1]]);r.report();n=Nav(r.wad,8,20)
for end in [(-1500,-1930),(-1700,-1670),(-1230,-1440),(-1100,-1470)]:
 try:print(end,n.path((r.state['x'],r.state['y']),end,sectors=r.state['sectors']))
 except Exception as e:print(end,e)
r.close()
