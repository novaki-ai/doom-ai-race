import sys; sys.path.insert(0, '../tools')
from nav import Nav
import math
N = Nav('E1M4')
res = N.path((2032,1120), (-1580, 1888))
pts, secs = res
sm = N.smooth(pts)
print(len(pts)*8, 'approx len')
L=0
for a,b in zip(sm, sm[1:]): L+=math.hypot(b[0]-a[0], b[1]-a[1])
print('smooth len', L)
print([(round(x),round(y)) for x,y in sm])
seen=[]
for s in secs:
    if not seen or seen[-1]!=s: seen.append(s)
print(seen)
