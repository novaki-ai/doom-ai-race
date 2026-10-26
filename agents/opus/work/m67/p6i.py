import sys, math; sys.path.insert(0, '/race/opus/tools_m67')
from nav import Nav
from wad import read_map
m = read_map('E1M6')
def closed(sec): return (None, m.sectors[sec][0])
def plen(pts): return sum(math.hypot(b[0]-a[0], b[1]-a[1]) for a,b in zip(pts,pts[1:]))
N = Nav('E1M6', {187:closed(187)})
for a,g in [((1680,-1344),(-1536,-1728)), ((32,-1376),(1680,-1344)), ((1680,-1344),(32,-1376))]:
    r = N.path(a, g)
    print(a, g, 'OK' if r else 'NO')
    if r:
        seen=[]
        for s in r[1]:
            if not seen or seen[-1]!=s: seen.append(s)
        sm=N.smooth(r[0]); print(round(plen(sm)), [(round(p[0]),round(p[1])) for p in sm], [(s, N.doorsec.get(s)) for s in seen if s in N.doorsec])
