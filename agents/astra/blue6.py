from sim import Sim
from lmp import oku
r=Sim(6);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/red6.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
for p in [(1400,-1312),(784,-1248),(448,-1064),(56,-840),(-176,-840),(-664,-1008),(-896,-1200),(-896,-1400),(-992,-1536),(-1168,-1512),(-1536,-1728)]:
 if not r.goto(*p,fire=True,rad=20,maxn=1600,stucklimit=1500):break
r.save('work/blue6.lmp');r.draw();r.report();r.close()
