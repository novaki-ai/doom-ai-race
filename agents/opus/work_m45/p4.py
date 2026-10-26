import sys; sys.path.insert(0, '../tools')
from wad import read_map
m = read_map('E1M4')
for want in (52, 66, 38, 65, 41, 40):
    print('sector', want, m.sectors[want])
    for li,(v1,v2,fl,sp,tg,s1,s2) in enumerate(m.lines):
        fs,bs = m.lsec[li]
        if want in (fs,bs):
            other = bs if fs==want else fs
            print('  line', li, m.verts[v1], m.verts[v2], 'flags', fl, 'sp', sp, 'front', fs, 'back', bs, 'other', other, m.sectors[other][:2] if other>=0 else None)
