from sim import Sim
from lmp import oku
r=Sim(7);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/east7b.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.weapon_policy=True;r.avoid=True;r.combat_lock=True;r.hitscan_priority=True;r.combat_range=800
for p in [(-520,312),(-496,312),(-400,304),(-352,232),(-392,-48),(-416,-224),(-416,-784),(-256,-864),(-112,-864),(96,-1184),(96,-1424),(392,-1640),(592,-1640),(648,-1688),(664,-1728)]:
 if not r.goto(*p,fire=True,rad=14,maxn=350,stucklimit=300):break
r.save('work/shortsouth7.lmp');r.report();r.close()
