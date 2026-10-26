"""Query map: sector at a point; list nearby two-sided line height changes. Usage: q.py E1M1 x y [x y ...]"""
import sys
from wad import read_map

def sector_at(m, px, py):
    best = None
    for i, (v1, v2, fl, sp, tg, s1, s2) in enumerate(m.lines):
        (x1, y1), (x2, y2) = m.verts[v1], m.verts[v2]
        if (y1 > py) == (y2 > py): continue
        t = (py - y1) / (y2 - y1)
        ix = x1 + t * (x2 - x1)
        if ix < px: continue
        if best is None or ix < best[0]:
            best = (ix, i, y2 > y1)
    if best is None: return -1
    ix, i, up = best
    fs, bs = m.lsec[i]
    # line going up (y2>y1): front side is to the right (east) => point (west) is on back side
    return bs if up else fs

if __name__ == '__main__':
    m = read_map(sys.argv[1])
    a = list(map(float, sys.argv[2:]))
    for j in range(0, len(a), 2):
        s = sector_at(m, a[j], a[j + 1])
        print(a[j], a[j + 1], 'sector', s, m.sectors[s] if s >= 0 else None)
