from sim import Sim
r=Sim(4);r.near=True
for p in [(1900,1150),(1780,1150),(1460,1150),(1240,1350),(1240,1550),(1000,1720),(400,1720)]:
 if not r.goto(*p,fire=True):break
r.report();print([o for o in r.state['monsters'] if abs(o[1]-r.state['x'])<150 and abs(o[2]-r.state['y'])<150]);r.draw();r.save('work/probe4.lmp');r.close()
