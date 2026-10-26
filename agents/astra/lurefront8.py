from sim import Sim
from lmp import oku
import math
r=Sim(8);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/gun8.lmp')[1]]);r.smartturn=True;r.weapon_policy=False;r.combat_range=800;r.avoid=True
r.step(b=28)
for p in [(160,2660),(64,2960),(160,3264),(416,3300)]:r.goto(*p,fire=True,rad=20,maxn=150)
r.avoid=False
for k in range(180):
 a=k*math.tau/12;r.goto(416+220*math.cos(a),3300+200*math.sin(a),fire=True,rad=20,speed=12,maxn=80)
 if r.state['ammo'][0]==0 and r.state['weapon']!=2:r.step(b=20)
 bs=[o for o in r.state['monsters'] if o[0]==15 and o[4]>0]
 if k%12==0:print('BOSS',[(o[4],o[1],o[2]) for o in bs],r.state['ammo'],flush=True)
 if not bs or r.state['health']<=0:break
r.save('work/lurefront8.lmp');r.draw();r.report();r.close()
