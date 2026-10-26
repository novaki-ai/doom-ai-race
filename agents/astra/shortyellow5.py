from sim import Sim
from lmp import oku
r=Sim(5);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/route5.lmp')[1]][:288]);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=True;r.combat_lock=True;r.hitscan_priority=True
for p in [(256,424),(208,424),(192,400),(192,176),(224,160),(840,192),(864,224),(900,300),(864,224),(224,160),(192,176),(200,420),(200,600),(360,528),(416,520),(704,640),(912,712),(1048,776),(1048,832),(968,880),(856,880),(688,800),(688,848)]:
 if not r.goto(*p,fire=True,rad=16,maxn=350):break
r.save('work/shortyellow5.lmp');r.report();r.close()
