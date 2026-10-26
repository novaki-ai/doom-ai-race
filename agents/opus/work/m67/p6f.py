import sys; sys.path.insert(0, '/race/opus/tools_m67')
from nav import Nav
from wad import read_map
m = read_map('E1M6')
nbr = {i:set() for i in range(len(m.sectors))}
for fs,bs in m.lsec:
    if fs>=0 and bs>=0: nbr[fs].add(bs); nbr[bs].add(fs)
def opened(sec):
    c = min(m.sectors[n][1] for n in nbr[sec] if n!=sec)
    return (None, c-4)
for s in (28,25,106,19,104,37):
    print(s, m.sectors[s], 'nbrs', [(n, m.sectors[n][:2]) for n in nbr[s]])
S=(-600,1280)
for name, ov in {'37':{37:opened(37)}, '37+28':{37:opened(37),28:opened(28)}, '37+14':{37:opened(37),25:opened(25),106:opened(106)}, 'all':{37:opened(37),28:opened(28),25:opened(25),106:opened(106)}}.items():
    N = Nav('E1M6', ov)
    r = N.path(S, (-1920,2016))
    print(name, 'OK' if r else 'NO')
    if r:
        print([(round(p[0]),round(p[1])) for p in N.smooth(r[0])])
        seen=[]
        for s in r[1]:
            if not seen or seen[-1]!=s: seen.append(s)
        print(seen)
