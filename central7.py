from sim import Sim
from lmp import oku
r=Sim(7);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/route7.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
for p in [(1248,-248),(1248,-392),(1216,-416),(960,-640),(720,-704),(600,-704),(576,-960),(736,-1056),(576,-1056),(216,-880),(96,-1088),(-336,-1344),(-200,-1504),(-560,-1504)]:
 if not r.goto(*p,fire=True,rad=14,maxn=450,stucklimit=350):break
r.face(180,n=14);r.step(b=2);r.step(n=30)
r.save('work/central7.lmp');r.draw();r.report();r.close()
