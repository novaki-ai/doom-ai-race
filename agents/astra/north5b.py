from sim import Sim
from lmp import oku
r=Sim(5);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/north5.lmp')[1]][:3928]);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=False
for p in [(56,1736),(56,1784),(32,1856),(-8,2064),(-64,2152),(-72,2272),(-152,2336),(-240,2336),(-256,2368),(-288,2456)]:
 if not r.goto(*p,fire=True,rad=20,maxn=500,stucklimit=400):break
r.face(90,n=14);r.step(b=2);r.step(n=10)
r.save('work/north5b.lmp');r.draw();r.report();r.close()
