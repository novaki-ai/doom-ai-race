import sys, random; sys.path.insert(0, '../tools_m45')
from follow import follow
from dbg import load
from m5drive import LEGS, W_, m
pre = load('m5_L0_best.lmp')
L = LEGS['L1']
W = W_(L['pts'])
tics, r = follow(5, W, prefix=pre, max_tics=400, K=3, m=m, uselines=set(L['ul']), stop_at_end=True, verbose=True)
for i in range(112, len(r.pos), 3): print(i, [round(v) for v in r.pos[i][:4]], tics[i] if i < len(tics) else None)
