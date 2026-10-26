import sys; sys.path.insert(0, '../tools_m45')
from wad import read_map
m = read_map('E1M5')
for s in [int(a) for a in sys.argv[1:]]:
    print('sector', s, m.sectors[s])
    for li,(v1,v2,fl,sp,tg,s1,s2) in enumerate(m.lines):
        fs,bs=m.lsec[li]
        if s in (fs,bs) and bs>=0:
            o = bs if fs==s else fs
            print('   line', li, m.verts[v1], m.verts[v2], 'fl', fl, 'sp', sp, 'tg', tg, 'other', o, m.sectors[o][:2])
