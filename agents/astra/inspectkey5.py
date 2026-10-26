from sim import Sim
from lmp import oku
for p in ['work/starkey5.lmp','work/fastkey5.lmp']:
 r=Sim(5);r.replay([(f,s,a//256,b) for f,s,a,b in oku(p)[1]]);r.report();r.close()
