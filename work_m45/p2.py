import sys; sys.path.insert(0, '../tools')
from nav import Nav
import math
def show(N, a, b):
    res = N.path(a, b)
    if res is None: print('NO PATH', a, b); return
    pts, secs = res
    sm = N.smooth(pts)
    L=0
    for p,q in zip(sm, sm[1:]): L+=math.hypot(q[0]-p[0], q[1]-p[1])
    print(a, b, 'smooth len', round(L), [(round(x),round(y)) for x,y in sm])
    seen=[]
    for s in secs:
        if not seen or seen[-1]!=s: seen.append(s)
    print('  secs', seen)
N = Nav('E1M4', overrides={52:(184,None)})
show(N, (2032,1120), (-1580,1888))
show(N, (2032,1120), (-1248,1280))
show(N, (-1248,1280), (-1088,1560))
show(N, (-1088,1560), (-1580,1888))
