from sim import Sim
from lmp import oku
r=Sim(3);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/route3b.lmp')[1]][:92]);r.auto_doors=True
r.goto(-1845,-3146,fire=True,rad=8,maxn=250)
r.report();print([o for o in r.state['monsters'] if abs(o[1]+1900)<250 and abs(o[2]+3000)<250]);r.save('work/fight3.lmp');r.close()
