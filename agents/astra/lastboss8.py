from sim import Sim
from lmp import oku
import math
r=Sim(8);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/lure8.lmp')[1]]);r.smartturn=True;r.weapon_policy=True;r.combat_range=900
for p in [(800,3300),(1264,3312),(800,3300),(416,3100),(416,2740)]:r.goto(*p,fire=True,rad=22,maxn=200)
for k in range(180):
 a=k*math.tau/12;r.goto(416+180*math.cos(a),3090+280*math.sin(a),fire=True,rad=25,maxn=50,speed=10)
 bs=[o for o in r.state['monsters'] if o[0]==15 and o[4]>0]
 if k%12==0:print('BOSSES',[(o[4],o[1],o[2]) for o in bs],flush=True)
 if not bs or r.state['health']<=0:break
r.save('work/lastboss8.lmp');r.report();r.close()
