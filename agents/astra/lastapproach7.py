from sim import Sim
from lmp import oku
r=Sim(7);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/rocketswitch7.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=True;r.combat_lock=True;r.hitscan_priority=True;r.combat_range=900
for p in [(344,-2288),(296,-2320),(216,-2368),(96,-2440),(96,-2528),(128,-2544),(200,-2560),(584,-2560),(672,-2464),(672,-2104),(688,-2064),(736,-2024),(864,-1960),(1000,-1960),(1120,-2024)]:
 if not r.goto(*p,fire=True,rad=14,maxn=300):break
r.save('work/lastapproach7.lmp');r.report();r.close()
