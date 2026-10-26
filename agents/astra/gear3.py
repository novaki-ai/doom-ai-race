from sim import Sim
from lmp import oku
r=Sim(3);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/normal3.lmp')[1]][:285]);r.smartturn=True;r.auto_doors=True;r.avoid=True
pts=[(-1864,-2208),(-1860,-2040),(-2070,-2000),(-2130,-1940),(-2144,-1800),(-2144,-1760),(-2144,-1600),(-2048,-1536),(-2032,-1440),(-2112,-1440)]
for p in pts:
 if not r.goto(*p,fire=True,rad=16):break
r.save('work/gear3.lmp');r.draw();r.report();r.close()
