"""Minimal WAD map reader for DOOM1.WAD (vanilla format)."""
import struct, os
WAD = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'game', 'DOOM1.WAD')

class Map:
    pass

def read_map(name, wad=WAD):
    b = open(wad, 'rb').read()
    ident, n, ofs = struct.unpack('<4sii', b[:12])
    lumps = []
    for i in range(n):
        p, s, nm = struct.unpack('<ii8s', b[ofs + 16 * i: ofs + 16 * i + 16])
        lumps.append((nm.rstrip(b'\0').decode(), p, s))
    idx = [l[0] for l in lumps].index(name)
    d = {}
    for nm, p, s in lumps[idx + 1: idx + 11]:
        d[nm] = b[p:p + s]
    m = Map()
    m.name = name
    m.things = [struct.unpack('<5h', d['THINGS'][i:i + 10]) for i in range(0, len(d['THINGS']), 10)]
    m.lines = [struct.unpack('<7h', d['LINEDEFS'][i:i + 14]) for i in range(0, len(d['LINEDEFS']), 14)]
    m.sides = []
    for i in range(0, len(d['SIDEDEFS']), 30):
        xo, yo, t, bo, mi, sec = struct.unpack('<hh8s8s8sh', d['SIDEDEFS'][i:i + 30])
        m.sides.append((xo, yo, t.rstrip(b'\0').decode(), bo.rstrip(b'\0').decode(), mi.rstrip(b'\0').decode(), sec))
    m.verts = [struct.unpack('<2h', d['VERTEXES'][i:i + 4]) for i in range(0, len(d['VERTEXES']), 4)]
    m.sectors = []
    for i in range(0, len(d['SECTORS']), 26):
        fh, ch, ft, ct, li, sp, tg = struct.unpack('<hh8s8shhh', d['SECTORS'][i:i + 26])
        m.sectors.append((fh, ch, ft.rstrip(b'\0').decode(), ct.rstrip(b'\0').decode(), li, sp, tg))
    # line -> (front sector, back sector)
    m.lsec = []
    for (v1, v2, fl, sp, tg, s1, s2) in m.lines:
        fs = m.sides[s1][5] if s1 >= 0 else -1
        bs = m.sides[s2][5] if s2 >= 0 and s2 != -1 else -1
        m.lsec.append((fs, bs))
    return m

THING_NAMES = {1: 'P1', 2: 'P2', 3: 'P3', 4: 'P4', 11: 'DM', 3004: 'zombie', 9: 'sarge', 3001: 'imp', 3002: 'demon', 58: 'spectre',
               3003: 'baron', 3006: 'soul', 3005: 'caco', 5: 'BLUEKEY', 6: 'YELLOWKEY', 13: 'REDKEY', 38: 'REDSKULL', 39: 'YELSKULL', 40: 'BLUSKULL',
               2001: 'shotgun', 2002: 'chaingun', 2003: 'launcher', 2004: 'plasma', 2005: 'chainsaw', 2006: 'bfg', 2011: 'stim', 2012: 'medikit',
               2013: 'soulsphere', 2014: 'hbonus', 2015: 'abonus', 2018: 'garmor', 2019: 'barmor', 2022: 'invuln', 2023: 'berserk', 2024: 'invis', 2025: 'suit',
               2026: 'map', 2045: 'goggles', 2035: 'barrel', 14: 'teledest'}
MONSTERS = {3004, 9, 3001, 3002, 58, 3003, 3006, 3005, 16, 7, 64, 65, 66, 67, 68, 69, 71, 84}

if __name__ == '__main__':
    import sys
    m = read_map(sys.argv[1])
    print('things', len(m.things), 'lines', len(m.lines), 'sectors', len(m.sectors))
    for t in m.things:
        x, y, a, ty, fl = t
        if ty in THING_NAMES and ty not in (2, 3, 4, 11, 2014, 2015, 2035):
            uv = 'UV' if fl & 4 else '--'
            print(f'thing {THING_NAMES[ty]:10s} ({x},{y}) ang {a} {uv} flags {fl}')
    for i, (v1, v2, fl, sp, tg, s1, s2) in enumerate(m.lines):
        if sp:
            a, b = m.verts[v1], m.verts[v2]
            fs, bs = m.lsec[i]
            print(f'line {i} special {sp} tag {tg} {a}->{b} flags {fl} front {fs} back {bs}')
    for i, s in enumerate(m.sectors):
        if s[5] or s[6]:
            print(f'sector {i} floor {s[0]} ceil {s[1]} light {s[4]} special {s[5]} tag {s[6]}')
