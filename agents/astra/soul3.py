from sim import Sim
from lmp import oku
from nav import Nav
r=Sim(3);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/base3.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
r.goto(-1936,-2038,rad=10,fire=True);r.face(270,n=40);r.step(b=2);r.step(n=40)
r.report();print('door',r.state['sectors'][121]);r.save('work/switch3.lmp');n=Nav(r.wad,8,20);path=n.path((r.state['x'],r.state['y']),(-2336,-2464),sectors=r.state['sectors']);print('PATH',path,flush=True)
for p in path[1:]:
 if not r.goto(*p,fire=True,rad=12,maxn=500,stucklimit=400):break
r.save('work/soul3.lmp');r.draw();r.report();r.close()
