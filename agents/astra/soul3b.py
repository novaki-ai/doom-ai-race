from sim import Sim
from lmp import oku
from nav import Nav
r=Sim(3);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/searchgear3.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
for p in [(-2144,-1820),(-2120,-1980),(-2080,-2104),(-2056,-2120),(-1960,-2120),(-1936,-2104)]:r.goto(*p,fire=True,rad=10,maxn=350)
r.face(90,n=40);r.report();r.step(b=2);r.goto(-1860,-2200,fire=True,rad=15,maxn=300)
r.report();print('door',r.state['sectors'][121]);r.save('work/switch3b.lmp')
n=Nav(r.wad,8,18)
try:
 path=n.path((r.state['x'],r.state['y']),(-2336,-2464),sectors=r.state['sectors']);print('PATH',path,flush=True)
 for p in path[1:]:
  if not r.goto(*p,fire=True,rad=12,maxn=500,stucklimit=400):break
except Exception as e:print(e)
r.save('work/soul3b.lmp');r.draw();r.report();r.close()
