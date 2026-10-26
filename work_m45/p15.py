import sys; sys.path.insert(0, '../tools_m45')
from nav import Nav
from p13 import show, m
from p10 import reach
base = {58:(None, m.sectors[58][0]), 109:(None, m.sectors[109][0]), 52:(None, -8), 91:(56, None), 12:(-104, None)}
N = Nav('E1M5', overrides=base)
show(N, (-620, 832), (-1150, 832))
# out of the pit: lift 48 down
o = dict(base); o[48] = (-152, None)
N2 = Nav('E1M5', overrides=o)
show(N2, (-1150, 832), (-990, 1250))
o3 = dict(base); o3[82] = (None, 164)
N3 = Nav('E1M5', overrides=o3)
show(N3, (-930, 1280), (192, 1040))
