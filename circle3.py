from sim import Sim
from lmp import oku
import math
r=Sim(3);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/upper3.lmp')[1]]);r.smartturn=True;r.weapon_policy=True;r.combat_lock=True;r.combat_range=400
r.goto(-240,-800,rad=10,fire=True,maxn=150)
for k in range(96):
 a=k*math.tau/12;r.goto(-240+50*math.cos(a),-800+64*math.sin(a),fire=True,rad=8,speed=8,maxn=30)
 enemies=[o for o in r.state['monsters'] if o[0]==11 and o[4]>0 and -340<o[1]<-128 and -900<o[2]<-500]
 if k%12==0:print('IMPS',[(o[:5]) for o in enemies],flush=True)
 if not enemies or r.state['health']<=0:break
for p in [(-264,-704),(-264,-560),(-272,-528),(-304,-528)]:r.goto(*p,fire=True,rad=12,maxn=200)
r.save('work/circle3.lmp');r.draw();r.report();r.close()
