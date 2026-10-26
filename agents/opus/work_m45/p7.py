import sys; sys.path.insert(0, '../tools_m45')
from nav import Nav
from wad import read_map
import math
def show(N, a, b):
    res = N.path(a, b)
    if res is None: print('NO PATH', a, b); return None
    pts, secs = res
    sm = N.smooth(pts)
    L=0
    for p,q in zip(sm, sm[1:]): L+=math.hypot(q[0]-p[0], q[1]-p[1])
    print(a, b, 'smooth len', round(L), [(round(x),round(y)) for x,y in sm])
    seen=[]
    for s in secs:
        if not seen or seen[-1]!=s: seen.append(s)
    print('  secs', seen)
    return sm
m = read_map('E1M5')
N = Nav('E1M5', overrides={58:(None, m.sectors[58][0]), 109:(None, m.sectors[109][0]), 15:(None, m.sectors[15][0])})
# where can we reach from start? sample reachable sectors
import heapq
W=N.W
si,sj=N.cell(-224,-624); sk=sj*W+si
seen={sk}; st=[sk]
while st:
    k=st.pop(); i,j=k%W,k//W
    for di,dj in ((1,0),(-1,0),(0,1),(0,-1)):
        kk=(j+dj)*W+i+di
        if kk in seen: continue
        if N.can_step(k,kk): seen.add(kk); st.append(kk)
secs=sorted(set(N.sec[k] for k in seen))
print('reachable sectors (no key doors):', secs)
for nm,(x,y) in (('yellow',(688,800)),('blue',(192,1040))):
    i,j=N.cell(x,y); print(nm, 'sector', N.sec[j*W+i])
