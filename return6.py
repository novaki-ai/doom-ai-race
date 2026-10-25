from sim import Sim
from lmp import oku
r=Sim(6);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/searchroom6.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True;r.combat_lock=True
for p in [(1152,-700),(1220,-760),(1300,-840),(1184,-928)]:
 if not r.goto(*p,fire=True,rad=14,maxn=300):break
r.save('work/return6.lmp');r.draw();r.report();r.close()
