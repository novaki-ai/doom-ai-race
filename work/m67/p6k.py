import sys, math; sys.path.insert(0, '/race/opus/tools_m67')
from nav import Nav
from wad import read_map
m = read_map('E1M6')
nbr = {i:set() for i in range(len(m.sectors))}
for fs,bs in m.lsec:
    if fs>=0 and bs>=0: nbr[fs].add(bs); nbr[bs].add(fs)
def opened(sec):
    c = min(m.sectors[n][1] for n in nbr[sec] if n!=sec)
    return (None, c-4)
def closed(sec): return (None, m.sectors[sec][0])
def plen(pts): return sum(math.hypot(b[0]-a[0], b[1]-a[1]) for a,b in zip(pts,pts[1:]))
ov = {139:closed(139),142:closed(142),94:closed(94),146:opened(146),216:opened(216),242:opened(242),151:(48,None)}
N = Nav('E1M6', ov)
for a,g in [((1250,-256),(1088,-608)), ((1250,-280),(1300,-760)), ((1088,-608),(-64,2330)), ((1300,-760),(-64,2330)), ((1250,-256),(-64,2330))]:
    r = N.path(a, g)
    print(a, g, 'OK' if r else 'NO')
    if r:
        seen=[]
        for s in r[1]:
            if not seen or seen[-1]!=s: seen.append(s)
        sm=N.smooth(r[0]); print('  ', round(plen(sm)), [(round(p[0]),round(p[1])) for p in sm], [(s, N.doorsec.get(s)) for s in seen if s in N.doorsec or s in (146,216,242,151)])
