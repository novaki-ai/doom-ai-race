import sys; sys.path.insert(0, '/race/opus/tools_m67')
import pickle
N = pickle.load(open('/race/opus/work/m67/nav6.pkl','rb'))
S=(32,-1376)
for g in [(0,2300),(-600,1280),(1680,-1344),(-1536,-1728)]:
    pts, secs = N.path(S, g)
    seen=[]
    for s in secs:
        if not seen or seen[-1]!=s: seen.append(s)
    print(g, 'doors', [(s, N.doorsec.get(s)) for s in seen if s in N.doorsec])
    print('  wps', [(round(p[0]),round(p[1])) for p in N.smooth(pts)])
from q import sector_at
print(sector_at(N.m, -720, 1280), N.m.sectors[37])
