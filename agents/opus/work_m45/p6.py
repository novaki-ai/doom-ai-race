import sys; sys.path.insert(0, '../tools_m45')
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
N = Nav('E1M5')
show(N, (-224,-624), (-288,2470))
show(N, (-224,-624), (192,1040))
show(N, (192,1040), (-288,2470))
print('---- blue doors closed')
from wad import read_map
m = read_map('E1M5')
print('sec58', m.sectors[58], 'sec109', m.sectors[109], 'sec55', m.sectors[55], 'sec56', m.sectors[56])
N = Nav('E1M5', overrides={58:(None, m.sectors[58][0]), 109:(None, m.sectors[109][0])})
show(N, (-224,-624), (192,1040))
show(N, (-224,-624), (688,800))
