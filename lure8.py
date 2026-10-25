from sim import Sim
from lmp import oku
import math
r=Sim(8);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/deadboss8.lmp')[1]][:3910]);r.smartturn=True;r.weapon_policy=True;r.combat_range=900;r.avoid=True
for p in [(416,3100),(416,2740),(416,2660),(416,3100)]:r.goto(*p,fire=True,rad=20,maxn=120)
r.avoid=False
for k in range(240):
 a=k*math.tau/12;r.goto(416+210*math.cos(a),3190+220*math.sin(a),fire=True,rad=25,maxn=90,speed=10)
 bs=[o for o in r.state['monsters'] if o[0]==15 and o[4]>0]
 if k%12==0:print('BOSSES',[(o[4],o[1],o[2]) for o in bs],flush=True)
 if not bs or r.state['health']<=0:break
r.save('work/lure8.lmp');r.report();r.close()
