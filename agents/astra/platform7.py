from sim import Sim
from lmp import oku
r=Sim(7);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/gear7.lmp')[1]][:1028]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
for p in [(256,-912),(464,-912),(552,-936),(704,-936),(736,-1056),(576,-1056),(560,-912),(448,-912),(256,-912),(256,-744),(256,-640),(-120,-800),(-400,-800),(-416,-768),(-480,-120)]:
 if not r.goto(*p,fire=True,rad=12,maxn=500,stucklimit=400):break
r.save('work/platform7.lmp');r.draw();r.report();r.close()
