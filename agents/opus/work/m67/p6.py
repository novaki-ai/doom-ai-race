import sys; sys.path.insert(0, '/race/opus/tools_m67')
from nav import Nav
import time
t=time.time()
N = Nav('E1M6')
print('nav built', time.time()-t)
m = N.m
res = N.path((32,-1376), (-1920, 2016))
pts, secs = res
print(len(pts))
# door sectors crossed
seen=[]
for s in secs:
    if not seen or seen[-1]!=s: seen.append(s)
print([ (s, N.doorsec.get(s)) for s in seen if s in N.doorsec])
sm = N.smooth(pts)
print([(round(p[0]),round(p[1])) for p in sm])
