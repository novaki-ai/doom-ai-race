from sim import Sim
from lmp import oku
r=Sim(8);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/gun8.lmp')[1]]);r.smartturn=True;r.auto_doors=False;r.weapon_policy=False;r.avoid=False;r.combat_range=800
r.step(b=28)
for k in range(100):
 p=[(200,2660),(200,2520),(640,2520),(640,2660)][k%4]
 r.goto(*p,fire=True,rad=20,maxn=150,speed=14)
 if r.state['ammo'][0]==0 and r.state['weapon']!=2:r.step(b=20)
 bosses=[o for o in r.state['monsters'] if o[0]==15 and o[4]>0]
 if k%4==0:print('BOSS',[(o[4],o[1],o[2]) for o in bosses],r.state['ammo'],flush=True)
 if not bosses or r.state['health']<=0:break
r.save('work/front8.lmp');r.draw();r.report();r.close()
