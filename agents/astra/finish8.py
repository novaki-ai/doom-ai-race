from sim import Sim
from lmp import oku
r=Sim(8);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/fight8.lmp')[1]]);r.smartturn=True;r.weapon_policy=True;r.combat_range=900
for p in [(416,3500),(416,3904),(416,4032),(416,3500),(680,3100),(640,2800),(416,2700)]:
 if not r.goto(*p,fire=True,rad=24,maxn=400):break
for k in range(15):
 r.goto(300 if k%2==0 else 530,2700,fire=True,rad=1,maxn=100,stucklimit=200,speed=10)
 bs=[o for o in r.state['monsters'] if o[0]==15 and o[4]>0];print('BOSSES',[(o[4],o[1],o[2]) for o in bs],flush=True)
 if not bs or r.state['health']<=0:break
r.save('work/deadboss8.lmp');r.draw();r.report();r.close()
