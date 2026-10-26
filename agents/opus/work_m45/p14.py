import sys; sys.path.insert(0, '../tools_m45')
from nav import Nav
from wad import read_map
from p13 import show, m
base = {58:(None, m.sectors[58][0]), 109:(None, m.sectors[109][0]), 15:(None, m.sectors[15][0]), 52:(None, -8)}
N = Nav('E1M5', overrides=base)
show(N, (-224,-624), (888, 230))
show(N, (888, 270), (700, 650))
o = dict(base); o[91] = (56, None)
N2 = Nav('E1M5', overrides=o)
show(N2, (888, 270), (688, 800))
o2 = dict(o); del o2[15]
N3 = Nav('E1M5', overrides=o2)
show(N3, (688, 800), (-620, 832))
