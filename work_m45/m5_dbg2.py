import sys, random, time; sys.path.insert(0, '../tools_m45')
from follow import follow
from wad import read_map
from dbg import load
import sim
m = read_map('E1M5')
pre = load('m5L1_best.lmp')
P = [(860, 200), (600, 176), (300, 176), (210, 190), (204, 428), (404, 508), (520, 545), (700, 600), (880, 680), (1000, 740), (1065, 770)]
W = [dict(x=x, y=y, r=30) for x, y in P]
W += [dict(x=1070, y=830, r=20), dict(x=980, y=880, r=30), dict(x=780, y=870, r=30), dict(x=692, y=804, r=14)]
tics, r = follow(5, W, prefix=pre, max_tics=700, K=4, m=m, uselines=set(), stop_at_end=True, stuck_tics=150)
for i in range(110, len(r.pos), 10): print(i, [round(v) for v in r.pos[i][:4]], r.pos[i][4:6], tics[i][3] if i < len(tics) else None)
