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
def plen(pts):
    return sum(math.hypot(b[0]-a[0], b[1]-a[1]) for a,b in zip(pts,pts[1:]))
def show(N, a, b, label):
    r = N.path(a, b)
    if not r: print(label, 'NO'); return
    sm = N.smooth(r[0])
    seen=[]
    for s in r[1]:
        if not seen or seen[-1]!=s: seen.append(s)
    print(label, 'len', round(plen(sm)), [(round(p[0]),round(p[1])) for p in sm])
    print('   doors', [(s, N.doorsec.get(s)) for s in seen if s in N.doorsec])
N1 = Nav('E1M6', {151:(48,None), 216:opened(216), 242:opened(242), 146:opened(146)})
BK=(-1536,-1728); YK=(1088,-608)
show(N1, BK, (1216,-256), 'blue->L460')
show(N1, (1216,-256), YK, 'L460->yk')
show(N1, BK, (1696,-192), 'blue->bluedoor')
show(N1, (1696,-192), (2624,-2260), 'bluedoor->switch438')
show(N1, (2624,-2260), YK, 'switch438->yk')
show(N1, YK, (344,128), 'yk->ydoorE')
show(N1, YK, (-472,128), 'yk->ydoorW')
show(N1, (344,128), (-64,2340), 'ydoor->switch822')
show(N1, YK, (-64,2340), 'yk->switch822 (any)')
show(N1, (32,-1376), (1680,-1344), 'start->red')
show(N1, (1680,-1344), BK, 'red->blue')
