import sys; sys.path.insert(0, '../tools_m45')
from nav import Nav
from wad import read_map
import math
m = read_map('E1M5')
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
base = {58:(None, m.sectors[58][0]), 109:(None, m.sectors[109][0]), 15:(None, m.sectors[15][0])}
N = Nav('E1M5', overrides=base)
show(N, (-224,-624), (-1120, 832))
o3 = dict(base); o3[82] = (None, 164)
N3 = Nav('E1M5', overrides=o3)
show(N3, (-1120, 832), (192, 1040))
o4 = dict(o3); del o4[109]; del o4[58]
N4 = Nav('E1M5', overrides=o4)
show(N4, (192, 1040), (-288, 2470))
print('=== lift 48 down')
o5 = dict(o3); o5[48] = (-152, None)
N5 = Nav('E1M5', overrides=o5)
show(N5, (-1120, 832), (-990, 1240))
o6 = dict(o3)
N6 = Nav('E1M5', overrides=o6)
show(N6, (-930, 1280), (192, 1040))
