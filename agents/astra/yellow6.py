from sim import Sim
from lmp import oku
r=Sim(6);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/blue6.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
for p in [(-1224,-1888),(-1200,-1880),(-1160,-1832),(-1152,-1712),(-1200,-1760),(-1450,-1740),(-1320,-1352),(-1344,-1176),(-1288,-1128),(-896,-1088),(-664,-1008),(-176,-840),(56,-840),(560,-800),(800,-800),(800,-960),(992,-944),(992,-800),(992,-736),(1088,-608)]:
 if not r.goto(*p,fire=True,rad=20,maxn=550,stucklimit=450):break
r.save('work/yellow6.lmp');r.draw();r.report();r.close()
