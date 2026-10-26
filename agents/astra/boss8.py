from sim import Sim
from lmp import oku
r=Sim(8);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/search8.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
for p in [(416,2380),(416,2450),(416,2600),(416,2760),(416,3100)]:
 if not r.goto(*p,fire=True,rad=20,maxn=600,stucklimit=500):break
r.save('work/boss8.lmp');r.draw();r.report();print('boss',[(o[:6]) for o in r.state['monsters'] if o[4]>0 and o[5]&4]);r.close()
