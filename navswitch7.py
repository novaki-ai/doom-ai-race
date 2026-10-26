from sim import Sim
from lmp import oku
from nav import Nav
r=Sim(7);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/saferocket7.lmp')[1]]);n=Nav(r.wad,8,24)
for a,b in [((176,-2560),(400,-2368)),((r.state['x'],r.state['y']),(352,-1760)),((1110,-2018),(1232,-1744))]:
 try:print(a,b,n.path(a,b,sectors=r.state['sectors'],allow_lifts=False,forbidden_doors=[72,104]))
 except Exception as e:print(e)
r.close()
