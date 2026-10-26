from sim import Sim
from lmp import oku
import json
states=[]
for p,k in [('work/circlereturn3.lmp',2363),('submit/E1M3.lmp',2431)]:
 r=Sim(3);r.replay([(f,s,a//256,b) for f,s,a,b in oku(p)[1]][:k]);r.report();states.append(r.state['angle']//2**24);r.close()
json.dump(states,open('work/splice3angles.json','w'))
