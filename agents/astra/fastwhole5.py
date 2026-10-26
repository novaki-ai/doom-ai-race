from sim import Sim
from lmp import oku
r=Sim(5);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/yellow5.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=True;r.combat_lock=True;r.hitscan_priority=True
pts=[(856,880),(1048,832),(1048,776),(704,640),(416,520),(200,420),(120,176),(48,168),(-64,240),(-64,400),(-440,688),(-590,832),(-750,832),(-1000,832),(-1064,552),(-1112,512),(-1170,448),(-1320,448),(-1488,448),(-1624,540),(-1624,576),(-1440,744),(-1120,832)]
for p in pts:
 if not r.goto(*p,fire=True,rad=20,maxn=250):break
r.face(0,n=20);r.step(b=2);r.step(n=5)
r.save('work/fastswitch5.lmp');r.report();r.close()
