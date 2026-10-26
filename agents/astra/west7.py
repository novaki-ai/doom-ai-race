from sim import Sim
from lmp import oku
r=Sim(7);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/switch7.lmp')[1]][:1357]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
for p in [(160,-1680),(160,-1856),(128,-1880),(48,-1936),(0,-1952),(-72,-1960),(-160,-2020),(-256,-1984),(-560,-1952),(-624,-1880),(-720,-1704),(-800,-1520),(-848,-1344),(-896,-1288),(-896,-672),(-1120,-288),(-1192,-144),(-1552,160),(-1680,160),(-1696,192),(-1696,328),(-1672,344),(-1424,384),(-1424,336)]:
 if not r.goto(*p,fire=True,rad=12,maxn=500,stucklimit=400):break
r.save('work/west7.lmp');r.draw();r.report();r.close()
