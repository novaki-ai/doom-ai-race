import sys; sys.path.insert(0, '../tools_m45')
from wad import read_map
m = read_map(sys.argv[1])
x0,y0,x1,y1 = map(float, sys.argv[2:6])
for li,(v1,v2,fl,sp,tg,s1,s2) in enumerate(m.lines):
    (ax,ay),(bx,by) = m.verts[v1], m.verts[v2]
    if min(ax,bx) <= x1 and max(ax,bx) >= x0 and min(ay,by) <= y1 and max(ay,by) >= y0:
        fs,bs = m.lsec[li]
        print(li, (ax,ay),(bx,by), 'fl',fl,'sp',sp,'tg',tg,'F',fs, m.sectors[fs][:2] if fs>=0 else None,'B',bs, m.sectors[bs][:2] if bs>=0 else None)
