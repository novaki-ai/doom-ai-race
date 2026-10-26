import sys; sys.path.insert(0, '../tools_m45')
from nav import Nav
from wad import read_map
import math
m = read_map('E1M5')
def reach(N, start):
    W=N.W
    si,sj=N.cell(*start); sk=sj*W+si
    seen={sk}; st=[sk]
    while st:
        k=st.pop(); i,j=k%W,k//W
        for di,dj in ((1,0),(-1,0),(0,1),(0,-1)):
            kk=(j+dj)*W+i+di
            if kk in seen: continue
            if N.can_step(k,kk): seen.add(kk); st.append(kk)
    return set(N.sec[k] for k in seen)
base = {58:(None, m.sectors[58][0]), 109:(None, m.sectors[109][0]), 15:(None, m.sectors[15][0])}
N0 = Nav('E1M5', overrides=base); r0 = reach(N0, (-224,-624))
o = dict(base); o[91] = (56, None)
N1 = Nav('E1M5', overrides=o); r1 = reach(N1, (-224,-624))
print('with 91 raised, new sectors:', sorted(r1 - r0))
o2 = dict(o); del o2[15]
N2 = Nav('E1M5', overrides=o2); r2 = reach(N2, (-224,-624))
print('plus yellow door open, new:', sorted(r2 - r1))
print('130 reachable?', 130 in r2, '100?', 100 in r2, '119?', 119 in r2)
print('=== with 82 open (switch 189)')
o3 = dict(base); o3[82] = (None, 164)
N3 = Nav('E1M5', overrides=o3); r3 = reach(N3, (-224,-624))
print('new:', sorted(r3 - r0)); print('130?', 130 in r3, '100?', 100 in r3, '119?', 119 in r3)
o4 = dict(o3); del o4[58]; del o4[109]
N4 = Nav('E1M5', overrides=o4); r4 = reach(N4, (-224,-624))
print('with blue doors too, 113?', 113 in r4)
