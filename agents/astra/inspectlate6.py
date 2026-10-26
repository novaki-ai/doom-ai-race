from sim import Sim
from lmp import oku
import math
r=Sim(6);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/latesoul6.lmp')[1]][:5013]);r.report()
print('M', [o for o in r.state['monsters'] if o[4]>0 and o[5]&4 and math.hypot(o[1]+1664,o[2]-1472)<250]);print('T',[o for o in r.wad.th if math.hypot(o[0]+1664,o[1]-1472)<150]);r.close()
