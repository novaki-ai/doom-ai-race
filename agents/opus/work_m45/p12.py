import sys; sys.path.insert(0, '../tools_m45')
from p11 import show, m
from nav import Nav
base = {58:(None, m.sectors[58][0]), 109:(None, m.sectors[109][0]), 15:(None, m.sectors[15][0]), 71:(None, 0)}
N = Nav('E1M5', overrides=base)
show(N, (-224,-624), (-1120, 832))
