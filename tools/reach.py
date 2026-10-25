"""Render reachability: cells reachable from A (green) and cells that can reach B (blue). usage: reach.py E1M7 ax ay bx by out.png"""
import sys
from collections import deque
from nav import Nav
from render import Img, render
def flood(N, start, reverse=False):
    W, H = N.W, N.H
    si, sj = N.cell(*start); k0 = sj * W + si
    seen = bytearray(W * H); seen[k0] = 1; q = deque([k0])
    while q:
        k = q.popleft(); i, j = k % W, k // W
        for di, dj in ((1,0),(-1,0),(0,1),(0,-1)):
            ii, jj = i + di, j + dj
            if not (0 <= ii < W and 0 <= jj < H): continue
            kk = jj * W + ii
            if seen[kk]: continue
            if (N.can_step(kk, k) if reverse else N.can_step(k, kk)) and N.ok[kk]:
                seen[kk] = 1; q.append(kk)
    return seen
if __name__ == '__main__':
    mp = sys.argv[1]; ax, ay, bx, by = map(float, sys.argv[2:6]); out = sys.argv[6]
    N = Nav(mp)
    A = flood(N, (ax, ay)); B = flood(N, (bx, by), reverse=True)
    sc = 0.25
    render(mp, out, sc)
    # overlay: re-render manually
    import zlib, struct
    from wad import read_map
    m = N.m
    xs = [v[0] for v in m.verts]; ys = [v[1] for v in m.verts]
    x0, y0, x1, y1 = min(xs) - 64, min(ys) - 64, max(xs) + 64, max(ys) + 64
    Wp, Hp = int((x1 - x0) * sc) + 1, int((y1 - y0) * sc) + 1
    im = Img(Wp, Hp)
    for k in range(N.W * N.H):
        if A[k] or B[k]:
            cx, cy = N.center(k % N.W, k // N.W)
            px, py = int((cx - x0) * sc), int((y1 - cy) * sc)
            c = (0, 120, 0) if A[k] and not B[k] else (0, 0, 160) if B[k] and not A[k] else (0, 160, 160)
            for a in range(2):
                for b in range(2): im.put(px + a, py + b, c)
    for i, (v1, v2, fl, sp, tg, s1, s2) in enumerate(m.lines):
        (xa, ya), (xb, yb) = m.verts[v1], m.verts[v2]
        c = (255, 255, 0) if sp else (200, 200, 200) if m.lsec[i][1] < 0 else (100, 100, 100)
        im.line(int((xa - x0) * sc), int((y1 - ya) * sc), int((xb - x0) * sc), int((y1 - yb) * sc), c)
        if sp:
            im.text(int(((xa + xb) / 2 - x0) * sc) + 2, int((y1 - (ya + yb) / 2) * sc) + 2, f'L{i}', (255, 255, 0))
    im.save(out)
    print('reachable from A:', sum(A), ' can reach B:', sum(B))
