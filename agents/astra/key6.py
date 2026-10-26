from sim import Sim
from lmp import oku
from nav import Nav
r=Sim(6);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/maze6.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
n=Nav(r.wad,8,22)
print('sector242',r.state['sectors'][242]);path=n.path((r.state['x'],r.state['y']),(1088,-608),sectors=r.state['sectors']);print(path)
for p in path[1:]:
 if not r.goto(*p,fire=True,rad=12,maxn=600,stucklimit=500):break
r.save('work/key6.lmp');r.draw();r.report();r.close()
