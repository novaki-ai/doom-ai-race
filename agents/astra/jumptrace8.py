from sim import Sim
from lmp import oku
import contextlib
r=Sim(8);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/fastboss8.lmp')[1]]);r.smartturn=True;r.avoid=False
for p in [(128,3100),(416,3500),(416,4130)]:r.goto(*p,rad=16,maxn=250,brake=1,speed=30)
while r.state['sectors'][30][0]>24:r.step()
r.report();print('wall',r.state['sectors'][30])
for target in [(416,4280),(336,4432)]:
 for k in range(50):
  with open('/dev/null','w') as out,contextlib.redirect_stdout(out):done=r.goto(*target,rad=12,speed=30,brake=100,maxn=1)
  s=r.state;print('STEP',target,k,len(r.t),round(s['x'],1),round(s['y'],1),round(s['z'],1),s['sectors'][30][0],flush=True)
  if done:break
r.save('work/jumptrace8.lmp');r.close()
