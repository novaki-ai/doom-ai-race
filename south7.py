from sim import Sim
from lmp import oku
r=Sim(7);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/east7b.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True;r.combat_lock=True
for p in [(-592,304),(-416,296),(-384,280),(-104,240),(96,136),(184,-264),(184,-280),(160,-384),(136,-416),(920,-448),(992,-528),(976,-632),(840,-704),(600,-704),(600,-832),(816,-832),(816,-1120),(392,-1200),(96,-1272),(96,-1424),(392,-1640),(592,-1640),(648,-1688),(664,-1728),(664,-2480),(640,-2496),(512,-2560),(176,-2560),(104,-2536),(96,-2504),(96,-2440),(280,-2328),(344,-2288),(352,-1760)]:
 if not r.goto(*p,fire=True,rad=12,maxn=500,stucklimit=400):break
r.face(90,n=40);r.step(b=2);r.step(n=10)
r.save('work/south7.lmp');r.draw();r.report();r.close()
