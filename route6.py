from sim import Sim
r=Sim(6);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
for p in [(-544,-1376),(-376,-1384),(-352,-1390),(-352,-1460),(-264,-1632),(-264,-1680),(-288,-1696),(-752,-1768),(-840,-1912),(-840,-1936),(-864,-1952),(-912,-1952),(-1152,-1712)]:
 if p==(-352,-1460):r.face(270,n=14);r.step(b=2);r.step(n=45)
 if not r.goto(*p,fire=True,rad=16,maxn=500,stucklimit=400):break
r.save('work/route6.lmp');r.draw();r.report();r.close()
