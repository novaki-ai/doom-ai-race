from sim import Sim
from lmp import oku
import math
r=Sim(8);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/lurefront8.lmp')[1]]);r.smartturn=True;r.weapon_policy=True;r.avoid=True;r.combat_lock=True;r.combat_range=1200
for p in [(160,3264),(64,2960),(160,2660),(416,2650)]:
 if not r.goto(*p,fire=True,rad=20,maxn=350,stucklimit=300):break
r.avoid=False
for k in range(100):
 a=k*math.tau/12
 r.goto(416+200*math.cos(a),2620+110*math.sin(a),fire=True,rad=16,speed=15,maxn=80,stucklimit=60)
 bs=[o for o in r.state['monsters'] if o[0]==15 and o[4]>0]
 if k%12==0:print('BOSS',[(o[4],o[1],o[2]) for o in bs],r.state['ammo'],flush=True)
 if not bs or r.state['health']<=0:break
r.save('work/frontfight8.lmp');r.draw();r.report();r.close()
