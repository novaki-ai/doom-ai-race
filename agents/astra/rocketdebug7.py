from sim import Sim
from lmp import oku
r=Sim(7);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/shortsouth7.lmp')[1]][:3722]);r.smartturn=True;r.auto_doors=True;r.auto_dist=52;r.avoid=False
r.step(b=36)
for p in [(-256,-864),(-112,-864)]:r.goto(*p,fire=False,rad=14,maxn=150)
r.report();print('before',[(o[:5]) for o in r.state['monsters'] if o[5]&4 and o[4]>0 and abs(o[1])<200 and -1200<o[2]<-700])
r.goto(0,-864,speed=0,fire=True,shoot_at=(30,-1040),maxn=50,stucklimit=200)
r.report();print('after',[(o[:5]) for o in r.state['monsters'] if o[5]&4 and o[4]>0 and abs(o[1])<200 and -1200<o[2]<-700]);r.save('work/rocketdebug7.lmp');r.close()
