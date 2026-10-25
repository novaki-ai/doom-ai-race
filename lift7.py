from sim import Sim
from lmp import oku
r=Sim(7);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/blue7.lmp')[1]][:2230]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True;r.combat_lock=True
print('near',[o[:5] for o in r.state['monsters'] if o[4]>0 and o[5]&4 and (o[1]+1400)**2+(o[2]+64)**2<400**2])
r.goto(r.state['x']+100,r.state['y'],speed=0,rad=5,fire=True,maxn=150,stucklimit=500)
for p in [(-1376,-64),(-1200,-160),(-1152,-576),(-960,-224),(-600,-320),(-608,-96)]:
 if not r.goto(*p,fire=True,rad=12,maxn=500,stucklimit=400):break
r.save('work/lift7.lmp');r.draw();r.report();r.close()
