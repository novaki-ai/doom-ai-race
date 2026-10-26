import sys; sys.path.insert(0, '../tools_m45')
from wad import read_map
m = read_map('E1M5')
for s in (92, 130, 93, 131, 132, 129):
    print('sector', s, m.sectors[s])
tags = {}
for i,sec in enumerate(m.sectors):
    if sec[6]: tags.setdefault(sec[6], []).append(i)
print('tagged sectors', tags)
for li,(v1,v2,fl,sp,tg,s1,s2) in enumerate(m.lines):
    fs,bs=m.lsec[li]
    if 92 in (fs,bs) or 130 in (fs,bs):
        print('line', li, m.verts[v1], m.verts[v2], 'fl', fl, 'sp', sp, 'tg', tg, 'F', fs, m.sectors[fs][:2], 'B', bs, m.sectors[bs][:2] if bs>=0 else None)
