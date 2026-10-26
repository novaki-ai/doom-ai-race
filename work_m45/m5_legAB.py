import sys; sys.path.insert(0, '../tools_m45')
from m5s import search_leg
P = [(-148,-36), (524,176), (840,200), (888,300), (930,470), (1000,620), (1070,760)]
base = [dict(x=x, y=y, r=35) for x, y in P] + [dict(x=1070, y=830, r=20, fixed=1), dict(x=900, y=880, r=30), dict(x=764, y=876, r=30), dict(x=692, y=804, r=14, fixed=1)]
search_leg('m5AB', (), base, int(sys.argv[1]), 25, mt=700, seed=int(sys.argv[2]), st=220)
