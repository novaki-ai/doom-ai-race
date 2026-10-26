from sim import Sim
from lmp import oku
r=Sim(7);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/central7.lmp')[1]][:856]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
for p in [(408,-696),(256,-672),(256,-744),(256,-800),(472,-816),(504,-888),(552,-936),(680,-936),(704,-960),(736,-1056),(576,-1056),(96,-1088),(96,-1400),(-336,-1344)]:
 if not r.goto(*p,fire=True,rad=12,maxn=600,stucklimit=500):break
r.save('work/gear7.lmp');r.draw();r.report();r.close()
