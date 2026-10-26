from sim import Sim
from lmp import oku
r=Sim(3);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/returncircle3.lmp')[1]][:2239]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
for p in [(-1400,-3072),(-1200,-3072),(-1192,-3016),(-1192,-2616),(-1304,-2544),(-1344,-2528),(-1280,-2440),(-1256,-2400),(-1256,-2352),(-1280,-2320),(-1312,-2160)]:
 if not r.goto(*p,fire=True,rad=12,maxn=350):break
r.save('work/mainexit3.lmp');r.draw();r.report();r.close()
