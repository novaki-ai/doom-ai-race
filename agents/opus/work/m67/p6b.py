import sys; sys.path.insert(0, '/race/opus/tools_m67')
from nav import Nav
import pickle
N = Nav('E1M6')
pickle.dump(N, open('/race/opus/work/m67/nav6.pkl','wb'))
S=(32,-1376)
for g in [(0,-700),(0,0),(0,300),(-64,520),(-64,800),(0,1200),(0,2300),(-600,1280),(-900,1280),(-1300,1300),(-1900,1300),(-1900,1700),(-1950,1950),(1088,-608),(1680,-1344),(-1536,-1728),(-2080,-2368)]:
    r = N.path(S, g)
    print(g, 'OK' if r else 'NO', N.sector_at(*g))
