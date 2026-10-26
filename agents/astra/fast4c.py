from sim import Sim
r=Sim(4);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
points=[(1900,1150),(1770,1150),(1500,1000),(1400,800),(1312,800),(1100,740),(920,560),(736,392),(736,304),(704,288),(400,290),(0,330),(-250,470),(-560,700),(-630,900),(-630,1030),(-440,1220),(-290,1340),(-290,1430),(-380,1560),(-480,1610),(-452,1684),(-550,1790),(-550,1888),(-700,1888)]
for p in points:
 if not r.goto(*p,fire=True,rad=16,maxn=300):break
r.save('work/fastbase4.lmp');r.report();r.draw();r.close()
