from sim import Sim
from lmp import oku
import math
r=Sim(8);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/boss8.lmp')[1]]);r.smartturn=True;r.weapon_policy=True;r.combat_range=800;r.avoid=False
for k in range(250):
 a=k*math.tau/12;x=416+250*math.cos(a);y=3270+220*math.sin(a)
 r.goto(x,y,fire=True,rad=28,maxn=110,speed=12)
 bosses=[o for o in r.state['monsters'] if o[0]==15 and o[4]>0]
 if k%12==0:print('BOSSES',[(o[4],o[1],o[2]) for o in bosses],r.state['ammo'],flush=True)
 if not bosses or r.state['health']<=0:break
r.save('work/fight8.lmp');r.draw();r.report();r.close()
