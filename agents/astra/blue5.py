from sim import Sim
from lmp import oku
r=Sim(5);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/switch5.lmp')[1]]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True
print('door82',r.state['sectors'][82])
for p in [(-1440,744),(-1600,600),(-1700,800),(-1776,824),(-1856,824),(-1856,480),(-1856,448),(-1780,560),(-1750,900),(-1700,1200),(-1500,1320),(-1170,1390),(-992,1296),(-992,1240),(-880,1296),(-800,1400),(-800,1530)]:
 if not r.goto(*p,fire=True,rad=20,maxn=400):break
r.save('work/westdone5.lmp');r.draw();r.report();r.close()
