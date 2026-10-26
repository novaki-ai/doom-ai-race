from sim import Sim
from lmp import oku
from nav import Nav
r=Sim(7);t=[(f,s,a//256,b) for f,s,a,b in oku('work/rocket7.lmp')[1]];r.replay(t[:2300])
for k in range(2300,2740,40):
 r.replay(t[k:k+40]);print(len(r.t),*(round(r.state[a],1) for a in ['x','y','health']))
n=Nav(r.wad,8,22)
for src in [(-1376,-104),(-960,-224),(-800,-400)]:
 try:print('PATH',src,n.path(src,(-608,-96),sectors=r.state['sectors'],forbidden_doors=[72]))
 except Exception as e:print(e)
r.close()
