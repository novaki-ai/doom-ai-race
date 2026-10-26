from sim import Sim
from lmp import oku
r=Sim(5);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/star5.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
for p in [(120,176),(-24,296),(-8,608),(48,792),(400,856),(696,1048),(768,1072),(832,1096),(880,1112),(1376,1096),(1432,1032),(1456,904),(1504,888),(1536,888),(1560,920),(1560,1352),(1520,1392),(1448,1400),(976,1400),(328,1336),(280,1304),(272,1272),(192,1040)]:
 if not r.goto(*p,fire=True,rad=20,maxn=500,stucklimit=400):break
r.save('work/key5.lmp');r.draw();r.report();r.close()
