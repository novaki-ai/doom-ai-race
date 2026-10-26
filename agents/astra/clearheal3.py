from sim import Sim
from lmp import oku
r=Sim(3);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/searchblue3.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=False;r.combat_lock=True;r.combat_range=300
for p in [(-160,-760),(-264,-760)]:r.goto(*p,fire=True,rad=10,maxn=120)
for k in range(10):
 r.goto(-240 if k%2==0 else -290,-760,rad=1,fire=True,maxn=35,stucklimit=200,speed=8)
 if not any(o[4]>0 and o[0]==11 and -340<o[1]<-200 and o[2]>-720 for o in r.state['monsters']):break
for p in [(-264,-560),(-272,-528),(-304,-528)]:r.goto(*p,fire=True,rad=12,maxn=200)
r.save('work/clearheal3.lmp');r.draw();r.report();r.close()
