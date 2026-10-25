from sim import Sim
r=Sim(3);r.auto_doors=True;r.avoid=True
points=[(-1440,-3232),(-1500,-3120),(-1640,-3060),(-1840,-3060),(-1840,-2850),(-1840,-2670),(-1900,-2500),(-1920,-2360),(-1864,-2208),(-1860,-2040),(-2130,-2000),(-2144,-1800),(-2080,-1600),(-2048,-1536)]
for p in points:
 if not r.goto(*p,fire=False):break
r.draw();r.save('work/fast3.lmp');r.report();r.close()
