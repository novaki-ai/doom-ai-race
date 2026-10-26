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
print('177 nbrs', [(n, m.sectors[n][:2]) for n in nbr[177]], '187 nbrs', [(n, m.sectors[n][:2]) for n in nbr[187]])
for i,(fs,bs) in enumerate(m.lsec):
    if 177 in (fs,bs) or 187 in (fs,bs):
        v1,v2=m.lines[i][:2]; print(i, m.verts[v1], m.verts[v2], fs, bs, m.lines[i][3])
N = Nav('E1M6', {174:closed(174),175:closed(175),177:opened(177),187:opened(187)})
for g in [(-1536,-1728)]:
    r = N.path((32,-1376), g)
    print(g, 'OK' if r else 'NO')
    if r:
        seen=[]
        for s in r[1]:
            if not seen or seen[-1]!=s: seen.append(s)
        print([(round(p[0]),round(p[1])) for p in N.smooth(r[0])], seen)
