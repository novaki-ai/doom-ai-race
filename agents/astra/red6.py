from sim import Sim
from lmp import oku
r=Sim(6);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/route6.lmp')[1]][:35]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
for p in [(-144,-1176),(-32,-1032),(-32,-856),(-8,-840),(56,-840),(784,-1248),(1400,-1312),(1680,-1344)]:
 if not r.goto(*p,fire=True,rad=20,maxn=450):break
r.save('work/red6.lmp');r.draw();r.report();r.close()
