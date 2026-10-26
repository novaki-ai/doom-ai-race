from sim import Sim
from lmp import oku
for path,t in [('work/shortsouth7.lmp',3722),('work/searchshort7.lmp',4026)]:
 r=Sim(7);r.replay([(f,s,a//256,b) for f,s,a,b in oku(path)[1]][:t]);r.report()
 print('ENEMIES', [m for m in r.state['monsters'] if m[4]>0 and abs(m[1]-r.state['x'])+abs(m[2]-r.state['y'])<1600]);r.close()
