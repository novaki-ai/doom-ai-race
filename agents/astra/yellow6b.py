from sim import Sim
from lmp import oku
r=Sim(6);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/yellow6.lmp')[1]][:1578]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
for p in [(-904,-1952),(-856,-1952),(-840,-1928),(-760,-1776),(-448,-1696),(-280,-1696),(-264,-1672),(-264,-1624),(-352,-1424),(-344,-1376),(-544,-1328),(-144,-1176),(-32,-1032),(-32,-856),(56,-840),(560,-800),(736,-816),(800,-800),(800,-960),(992,-944),(1184,-928),(992,-800),(992,-736),(1088,-608)]:
 if not r.goto(*p,fire=True,rad=20,maxn=600,stucklimit=500):break
r.save('work/yellow6b.lmp');r.draw();r.report();r.close()
