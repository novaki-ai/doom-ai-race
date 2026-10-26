"""Grid navigation over a Doom map: BSP sector lookup, player-box standability, A* path, line-of-sight smoothing.
Usage from code: N = Nav('E1M1'); path = N.path((x0,y0), (x1,y1), overrides={sector: (floor, ceil)})"""
import struct, math, heapq
from wad import read_map, WAD

CELL = 8
DOOR_SPECIALS = {1, 26, 27, 28, 31, 32, 33, 34, 117, 118}

class Nav:
    def __init__(s, name, overrides=None):
        s.m = m = read_map(name)
        b = open(WAD, 'rb').read()
        ident, n, ofs = struct.unpack('<4sii', b[:12])
        lumps = []
        for i in range(n):
            p, sz, nm = struct.unpack('<ii8s', b[ofs + 16 * i: ofs + 16 * i + 16])
            lumps.append((nm.rstrip(b'\0').decode(), p, sz))
        idx = [l[0] for l in lumps].index(name)
        d = {nm: b[p:p + sz] for nm, p, sz in lumps[idx + 1: idx + 11]}
        s.nodes = [struct.unpack('<4h8h2H', d['NODES'][i:i + 28]) for i in range(0, len(d['NODES']), 28)]
        s.ssec = [struct.unpack('<2h', d['SSECTORS'][i:i + 4]) for i in range(0, len(d['SSECTORS']), 4)]
        s.segs = [struct.unpack('<6h', d['SEGS'][i:i + 12]) for i in range(0, len(d['SEGS']), 12)]
        xs = [v[0] for v in m.verts]; ys = [v[1] for v in m.verts]
        s.x0, s.y0 = min(xs) - 64, min(ys) - 64
        s.W = (max(xs) + 64 - s.x0) // CELL + 1
        s.H = (max(ys) + 64 - s.y0) // CELL + 1
        s.floor = [s_[0] for s_ in m.sectors]
        s.ceil = [s_[1] for s_ in m.sectors]
        s.doorsec = {}
        for i, (v1, v2, fl, sp, tg, s1, s2) in enumerate(m.lines):
            if sp in DOOR_SPECIALS and m.lsec[i][1] >= 0:
                s.doorsec[m.lsec[i][1]] = sp
        # open doors: ceiling = lowest neighbouring ceiling - 4
        s.nbr = {i: set() for i in range(len(m.sectors))}
        for i, (fs, bs) in enumerate(m.lsec):
            if fs >= 0 and bs >= 0:
                s.nbr[fs].add(bs); s.nbr[bs].add(fs)
        for ds in s.doorsec:
            c = min((s.ceil[n] for n in s.nbr[ds] if n != ds), default=s.ceil[ds])
            s.ceil[ds] = max(s.ceil[ds], c - 4)
        if overrides:
            for sec, (f, c) in overrides.items():
                if f is not None: s.floor[sec] = f
                if c is not None: s.ceil[sec] = c
        s.build()
        # solid decorations block movement
        SOLID = {25,26,27,28,29,30,31,32,33,35,36,37,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,70,72,73,74,75,76,77,78,85,86,2028,2035}
        for (tx, ty, an, typ, fl) in s.m.things:
            if typ in SOLID and (fl & 4) and not (fl & 16):
                rad = 16 + (32 if typ == 54 else 16 if typ != 2035 else 10)
                i0, j0 = s.cell(tx - rad, ty - rad); i1, j1 = s.cell(tx + rad, ty + rad)
                for jj in range(max(0, j0), min(s.H, j1 + 1)):
                    for ii in range(max(0, i0), min(s.W, i1 + 1)):
                        s.ok[jj * s.W + ii] = 0

    def sector_at(s, x, y):
        n = len(s.nodes) - 1
        while True:
            nx, ny, dx, dy = s.nodes[n][:4]
            side = 1 if (y - ny) * dx >= dy * (x - nx) else 0
            if not dx: side = (1 if dy > 0 else 0) if x <= nx else (1 if dy < 0 else 0)
            elif not dy: side = (1 if dx < 0 else 0) if y <= ny else (1 if dx > 0 else 0)
            # R_PointOnSide returns 1 for back; children[0]=right(front), children[1]=left(back)
            c = s.nodes[n][12 + side]
            if c & 0x8000:
                ss = c & 0x7fff
                seg = s.segs[s.ssec[ss][1]]
                ld = s.m.lines[seg[3]]
                sd = ld[5] if seg[4] == 0 else ld[6]
                return s.m.sides[sd][5]
            n = c

    def build(s):
        W, H, m = s.W, s.H, s.m
        s.sec = [-1] * (W * H)
        for j in range(H):
            for i in range(W):
                s.sec[j * W + i] = s.sector_at(s.x0 + i * CELL + CELL / 2, s.y0 + j * CELL + CELL / 2)
        # blocking lines rasterized
        wall = bytearray(W * H)
        for li, (v1, v2, fl, sp, tg, s1, s2) in enumerate(m.lines):
            fs, bs = m.lsec[li]
            if bs >= 0 and not fl & 1: continue
            (ax, ay), (bx, by) = m.verts[v1], m.verts[v2]
            L = math.hypot(bx - ax, by - ay)
            nsteps = int(L / 2) + 1
            for k in range(nsteps + 1):
                px = ax + (bx - ax) * k / nsteps; py = ay + (by - ay) * k / nsteps
                i, j = int((px - s.x0) // CELL), int((py - s.y0) // CELL)
                if 0 <= i < W and 0 <= j < H: wall[j * W + i] = 1
        s.wall = wall
        R = 2  # 16 units
        near = bytearray(W * H)
        for j in range(H):
            for i in range(W):
                if wall[j * W + i]:
                    for jj in range(max(0, j - R), min(H, j + R + 1)):
                        for ii in range(max(0, i - R), min(W, i + R + 1)):
                            near[jj * W + ii] = 1
        s.near = near
        # box floor / ceil (max floor, min ceil within +-16)
        fl_ = [-32768] * (W * H); ce_ = [32767] * (W * H)
        for j in range(H):
            for i in range(W):
                sc = s.sec[j * W + i]
                if sc < 0:
                    continue
                f, c = s.floor[sc], s.ceil[sc]
                for jj in range(max(0, j - R), min(H, j + R + 1)):
                    for ii in range(max(0, i - R), min(W, i + R + 1)):
                        k = jj * W + ii
                        if f > fl_[k]: fl_[k] = f
                        if c < ce_[k]: ce_[k] = c
        s.bf, s.bc = fl_, ce_
        s.ok = bytearray(W * H)
        for k in range(W * H):
            if s.sec[k] >= 0 and not near[k] and s.bc[k] - s.bf[k] >= 56:
                s.ok[k] = 1

    def cell(s, x, y):
        return int((x - s.x0) // CELL), int((y - s.y0) // CELL)

    def center(s, i, j):
        return s.x0 + i * CELL + CELL / 2, s.y0 + j * CELL + CELL / 2

    def can_step(s, a, b):
        if not s.ok[b]: return False
        if s.bf[b] - s.bf[a] > 24: return False
        if s.bc[b] - s.bf[a] < 56: return False
        return True

    def path(s, start, goal, cost_sec=None, goal_r=12):
        """A* from start to goal (world coords). cost_sec: {sector: extra cost units}."""
        W, H = s.W, s.H
        si, sj = s.cell(*start); gi, gj = s.cell(*goal)
        sk = sj * W + si
        if not s.ok[sk]:
            # find nearest ok cell
            best = None
            for dj in range(-3, 4):
                for di in range(-3, 4):
                    k = (sj + dj) * W + si + di
                    if s.ok[k] and (best is None or abs(di) + abs(dj) < best[0]): best = (abs(di) + abs(dj), k)
            sk = best[1]
        gx, gy = goal
        dist = {sk: 0.0}; prev = {}
        pq = [(0.0, sk)]
        nb = [(1, 0, 1), (-1, 0, 1), (0, 1, 1), (0, -1, 1), (1, 1, 1.4142), (1, -1, 1.4142), (-1, 1, 1.4142), (-1, -1, 1.4142)]
        found = None
        while pq:
            d, k = heapq.heappop(pq)
            if d > dist.get(k, 1e18) + 1e-9: continue
            i, j = k % W, k // W
            cx, cy = s.center(i, j)
            if math.hypot(cx - gx, cy - gy) <= goal_r:
                found = k; break
            for di, dj, c in nb:
                ii, jj = i + di, j + dj
                if not (0 <= ii < W and 0 <= jj < H): continue
                kk = jj * W + ii
                if not s.can_step(k, kk): continue
                if di and dj and not (s.ok[j * W + ii] and s.ok[jj * W + i]): continue
                extra = 0
                if cost_sec:
                    extra = cost_sec.get(s.sec[kk], 0)
                nd = d + c * CELL + extra
                if nd < dist.get(kk, 1e18):
                    dist[kk] = nd; prev[kk] = k
                    hx, hy = s.center(ii, jj)
                    heapq.heappush(pq, (nd + math.hypot(hx - gx, hy - gy) * 0.0, kk))
        if found is None: return None
        cells = [found]
        while cells[-1] in prev: cells.append(prev[cells[-1]])
        cells.reverse()
        return [s.center(k % W, k // W) for k in cells], [s.sec[k] for k in cells]

    def los(s, a, b):
        """straight segment between world points a and b is walkable (sampled)"""
        (ax, ay), (bx, by) = a, b
        L = math.hypot(bx - ax, by - ay)
        n = int(L / 4) + 1
        pk = None
        for t in range(n + 1):
            x = ax + (bx - ax) * t / n; y = ay + (by - ay) * t / n
            i, j = s.cell(x, y)
            k = j * s.W + i
            if not s.ok[k]: return False
            if pk is not None and pk != k and not s.can_step(pk, k): return False
            pk = k
        return True

    def smooth(s, pts, maxlen=100000):
        out = [pts[0]]
        i = 0
        while i < len(pts) - 1:
            j = len(pts) - 1
            while j > i + 1 and not (s.los(pts[i], pts[j]) and math.hypot(pts[j][0]-pts[i][0], pts[j][1]-pts[i][1]) <= maxlen):
                j -= 1
            out.append(pts[j]); i = j
        return out
