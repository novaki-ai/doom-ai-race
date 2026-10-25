from sim import Sim
from lmp import oku
r=Sim(8);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/search8.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
for p in [(416,880),(664,880),(992,864),(864,928),(928,928),(928,800),(864,800),(664,880),(416,880),(416,1400),(416,2380),(416,2450),(416,2600),(416,2700)]:
 if not r.goto(*p,fire=True,rad=16,maxn=400,stucklimit=350):break
r.save('work/gun8.lmp');r.report();r.close()
