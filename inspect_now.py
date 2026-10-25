from sim import Sim
from lmp import oku
import math
for m,path,t in [(3,'work/exit3b.lmp',2570),(7,'work/exit7.lmp',5684)]:
 r=Sim(m);r.replay([(f,s,a//256,b) for f,s,a,b in oku(path)[1]][:t]);r.report()
 print('monsters', [o for o in r.state['monsters'] if o[4]>0 and o[5]&4 and math.hypot(o[1]-r.state['x'],o[2]-r.state['y'])<800])
 print('things',[o for o in r.wad.th if math.hypot(o[0]-r.state['x'],o[1]-r.state['y'])<400])
 print('lines',[(i,r.wad.v[a],r.wad.v[b],sp,r.wad.s[rs][-1],r.wad.s[ls][-1] if ls!=65535 else None) for i,(a,b,fl,sp,tag,rs,ls) in enumerate(r.wad.l) if math.hypot((r.wad.v[a][0]+r.wad.v[b][0])/2-r.state['x'],(r.wad.v[a][1]+r.wad.v[b][1])/2-r.state['y'])<220])
 r.close()
