import sys; sys.path.insert(0, '/race/opus/tools_m67')
import pickle
N = pickle.load(open('/race/opus/work/m67/nav6.pkl','rb'))
S=(32,-1376)
for g in [(1400,-750),(1300,-760),(1250,-700),(1150,-650),(1100,-620),(1550,-900),(1200,-1000),(992,-800),(992,-840)]:
    r = N.path(S, g)
    print(g, 'OK' if r else 'NO', N.sector_at(*g))
from q import sector_at
m=N.m
for i in range(len(m.lines)):
    fs,bs=m.lsec[i]
    if 193 in (fs,bs) and bs>=0:
        o = bs if fs==193 else fs
        v1,v2=m.lines[i][:2]
        print('193 nb', o, m.sectors[o][:2], m.verts[v1], m.verts[v2], 'flags', m.lines[i][2])
