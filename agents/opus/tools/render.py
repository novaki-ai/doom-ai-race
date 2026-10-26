"""Render a map to PNG (pure python). Usage: render.py E1M1 out.png [scale] [x0 y0 x1 y1]"""
import sys, zlib, struct
from wad import read_map, THING_NAMES, MONSTERS

FONT = {'0': '111101101101111', '1': '010110010010111', '2': '111001111100111', '3': '111001111001111', '4': '101101111001001',
        '5': '111100111001111', '6': '111100111101111', '7': '111001001001001', '8': '111101111101111', '9': '111101111001111',
        '-': '000000111000000', 'L': '100100100100111', 'S': '111100111001111', 'T': '111010010010010', 'E': '111100111100111',
        'X': '101101010101101', 'K': '101110100110101', 'D': '110101101101110', 'R': '110101110101101', 'B': '110101110101110',
        'Y': '101101010010010', 'P': '111101111100100', 'U': '101101101101111', 'W': '101101101111101', 'M': '101111111101101',
        'A': '010101111101101', 'C': '111100100100111', 'F': '111100110100100', 'G': '111100101101111', 'H': '101101111101101',
        'I': '111010010010111', 'N': '110101101101101', 'O': '111101101101111', 'V': '101101101101010', ' ': '000000000000000',
        ':': '000010000010000', '.': '000000000000010', '+': '000010111010000'}

class Img:
    def __init__(s, w, h):
        s.w, s.h = w, h
        s.p = bytearray(w * h * 3)
    def put(s, x, y, c):
        if 0 <= x < s.w and 0 <= y < s.h:
            i = (y * s.w + x) * 3
            s.p[i:i + 3] = bytes(c)
    def line(s, x0, y0, x1, y1, c):
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
        err = dx + dy
        while True:
            s.put(x0, y0, c)
            if x0 == x1 and y0 == y1: break
            e2 = 2 * err
            if e2 >= dy: err += dy; x0 += sx
            if e2 <= dx: err += dx; y0 += sy
    def text(s, x, y, t, c, sc=1):
        for ch in t.upper():
            g = FONT.get(ch, FONT[' '])
            for r in range(5):
                for q in range(3):
                    if g[r * 3 + q] == '1':
                        for a in range(sc):
                            for b in range(sc):
                                s.put(x + q * sc + a, y + r * sc + b, c)
            x += 4 * sc
    def save(s, fn):
        raw = b''.join(b'\0' + bytes(s.p[y * s.w * 3:(y + 1) * s.w * 3]) for y in range(s.h))
        def chunk(t, d):
            return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
        open(fn, 'wb').write(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', s.w, s.h, 8, 2, 0, 0, 0)) +
                             chunk(b'IDAT', zlib.compress(raw, 6)) + chunk(b'IEND', b''))

def render(mapname, fn, scale=0.25, box=None, path=None, grid=256, labels=True):
    m = read_map(mapname)
    xs = [v[0] for v in m.verts]; ys = [v[1] for v in m.verts]
    if box:
        x0, y0, x1, y1 = box
    else:
        x0, y0, x1, y1 = min(xs) - 64, min(ys) - 64, max(xs) + 64, max(ys) + 64
    W, H = int((x1 - x0) * scale) + 1, int((y1 - y0) * scale) + 1
    im = Img(W, H)
    T = lambda x, y: (int((x - x0) * scale), int((y1 - y) * scale))
    # grid
    g0 = (x0 // grid) * grid
    for gx in range(int(g0), int(x1) + 1, grid):
        px = T(gx, 0)[0]
        for py in range(0, H, 3): im.put(px, py, (40, 40, 60))
    g0 = (y0 // grid) * grid
    for gy in range(int(g0), int(y1) + 1, grid):
        py = T(0, gy)[1]
        for px in range(0, W, 3): im.put(px, py, (40, 40, 60))
    for i, (v1, v2, fl, sp, tg, s1, s2) in enumerate(m.lines):
        a, b = m.verts[v1], m.verts[v2]
        fs, bs = m.lsec[i]
        if sp in (11, 51, 52, 124, 197, 198):
            c = (255, 0, 0)
        elif sp in (26, 32, 99, 133):
            c = (60, 100, 255)
        elif sp in (27, 34, 136, 137):
            c = (255, 255, 0)
        elif sp in (28, 33, 134, 135):
            c = (255, 80, 200)
        elif sp in (1, 31, 117, 118, 29, 63, 103, 61, 50, 42, 2, 3, 4, 16, 46, 90, 86, 76, 75, 108, 109, 111, 112, 113, 114, 115, 116):
            c = (0, 200, 255)  # doors
        elif sp in (39, 97, 125, 126):
            c = (255, 128, 0)  # teleport
        elif sp:
            c = (0, 255, 0)
        elif bs < 0:
            c = (220, 220, 220)
        elif fl & 1:
            c = (170, 60, 255)   # two-sided but blocking (window)
        else:
            f1, f2 = m.sectors[fs][0], m.sectors[bs][0]
            c1, c2 = m.sectors[fs][1], m.sectors[bs][1]
            if abs(f1 - f2) > 24 or min(c1, c2) - max(f1, f2) < 56:
                c = (150, 110, 60)   # impassable step / low ceiling
            else:
                c = (90, 90, 90)
        im.line(*T(*a), *T(*b), c)
        if labels and sp:
            mx, my = T((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            im.text(mx + 2, my + 2, f'L{i}', c)
    for (x, y, an, ty, fl) in m.things:
        if not fl & 4 and ty not in (1,): continue
        px, py = T(x, y)
        if ty == 1: c = (0, 255, 0)
        elif ty in MONSTERS: c = (255, 40, 40)
        elif ty in (5, 40): c = (60, 100, 255)
        elif ty in (6, 39): c = (255, 255, 0)
        elif ty in (13, 38): c = (255, 80, 200)
        elif ty == 14: c = (255, 128, 0)
        else: c = (160, 160, 255)
        r = 2 if ty not in (1, 5, 6, 13, 38, 39, 40) else 4
        for ddx in range(-r, r + 1):
            for ddy in range(-r, r + 1):
                im.put(px + ddx, py + ddy, c)
        if ty in (1, 5, 6, 13, 38, 39, 40, 14):
            im.text(px + 5, py - 2, THING_NAMES.get(ty, str(ty))[:4], c)
    if path:
        for (ax, ay), (bx, by) in zip(path, path[1:]):
            im.line(*T(ax, ay), *T(bx, by), (255, 0, 255))
    # grid labels
    g0 = (x0 // grid) * grid
    for gx in range(int(g0), int(x1) + 1, grid * 2):
        im.text(T(gx, 0)[0] + 1, 1, str(gx), (120, 120, 200))
    g0 = (y0 // grid) * grid
    for gy in range(int(g0), int(y1) + 1, grid * 2):
        im.text(1, T(0, gy)[1] + 1, str(gy), (120, 120, 200))
    im.save(fn)
    return W, H

if __name__ == '__main__':
    mp, fn = sys.argv[1], sys.argv[2]
    sc = float(sys.argv[3]) if len(sys.argv) > 3 else 0.25
    box = tuple(map(int, sys.argv[4:8])) if len(sys.argv) > 7 else None
    print(render(mp, fn, sc, box))
