import sys; sys.path.insert(0, '../tools_m45')
from m5s import search_leg
base = [dict(x=-148, y=-36, r=40), dict(x=524, y=176, r=40), dict(x=840, y=200, r=30), dict(x=888, y=285, r=20, fixed=1)]
search_leg('m5A', (), base, int(sys.argv[1]), 30, mt=400, seed=int(sys.argv[2]))
