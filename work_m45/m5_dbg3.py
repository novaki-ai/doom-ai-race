import sys; sys.path.insert(0, '../tools_m45')
from follow import follow
from wad import read_map
from dbg import load
m = read_map('E1M5')
pre = load('m5sg_1.lmp')
P = [(288, 352, 10), (320, 430), (204, 428), (204, 250), (215, 180), (430, 176)]
W = [dict(x=p[0], y=p[1], r=p[2] if len(p) > 2 else 30) for p in P]
tics, r = follow(5, W, prefix=pre, max_tics=400, K=4, m=m, uselines={310, 312}, stop_at_end=True, verbose=True)
for i in range(110, len(r.pos), 4): print(i, [round(v) for v in r.pos[i][:4]], r.pos[i][4:6], tics[i] if i < len(tics) else None)
