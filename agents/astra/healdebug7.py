from sim import Sim
from lmp import oku
r=Sim(7);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/lastapproach7.lmp')[1]][:4704]);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=True;r.combat_lock=True;r.hitscan_priority=True;r.combat_range=600
for p in [(928,-1840),(1104,-1800),(1232,-1744),(1232,-1984),(1232,-2112),(1216,-2200),(1280,-2240),(1408,-2192),(1600,-2240),(1712,-2256),(1712,-2304),(1920,-2304)]:
 if not r.goto(*p,fire=True,rad=16,maxn=250,speed=30,brake=.5):break
r.save('work/healdebug7.lmp');r.report();r.close()
