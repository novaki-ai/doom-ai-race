from sim import Sim
from lmp import oku
r=Sim(3);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/upper3.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
for p in [(-160,-704),(-264,-704),(-264,-560),(-272,-528),(-304,-528),(-264,-704),(-160,-704),(-160,-488),(-192,-448),(-352,-416),(-400,-416),(-480,-576),(-480,-656),(-512,-672),(-688,-704),(-832,-736)]:
 if not r.goto(*p,fire=True,rad=12,maxn=350):break
r.save('work/heal3.lmp');r.draw();r.report();r.close()
