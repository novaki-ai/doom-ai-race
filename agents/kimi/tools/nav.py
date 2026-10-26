#!/usr/bin/env python3
import heapq
import math
from collections import defaultdict

from race import Wad, DOOR_SPECIALS, EXIT_SPECIALS

RADIUS = 15


def cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def intersect(a, b, c, d):
    return cross(a, b, c) * cross(a, b, d) <= 0 and cross(c, d, a) * cross(c, d, b) <= 0


def point_dist(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    if dx == dy == 0:
        return math.hypot(p[0] - a[0], p[1] - a[1])
    t = max(0, min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy)))
    return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)


def segment_dist(a, b, c, d):
    if intersect(a, b, c, d):
        return 0.0
    return min(point_dist(a, c, d), point_dist(b, c, d), point_dist(c, a, b), point_dist(d, a, b))


def line_intersection(a, b, c, d):
    den = (b[0] - a[0]) * (d[1] - c[1]) - (b[1] - a[1]) * (d[0] - c[0])
    if not den:
        return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    t = ((c[0] - a[0]) * (d[1] - c[1]) - (c[1] - a[1]) * (d[0] - c[0])) / den
    return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))


class Navigator:
    def __init__(self, mapnum, grid=32):
        self.map = Wad().map(mapnum)
        self.grid = grid
        self.lines = []
        self.door_sectors = set()
        for l in self.map.lines:
            if l["special"] in DOOR_SPECIALS:
                for side in ("right", "left"):
                    if l[side] != 65535:
                        self.door_sectors.add(self.map.sidedefs[l[side]]["sector"])
        for l in self.map.lines:
            p, q = self.map.point(l), self.map.point(l, False)
            front = self.map.sidedefs[l["right"]]["sector"] if l["right"] != 65535 else None
            back = self.map.sidedefs[l["left"]]["sector"] if l["left"] != 65535 else None
            door = l["special"] in DOOR_SPECIALS or front in self.door_sectors or back in self.door_sectors
            solid = back is None or bool(l["flags"] & 1)
            if not solid and not door:
                sf, sb = self.map.sectors[front], self.map.sectors[back]
                if abs(sf["floor"] - sb["floor"]) > 24 or min(sf["ceiling"], sb["ceiling"]) - max(sf["floor"], sb["floor"]) < 56:
                    solid = True
            self.lines.append(dict(line=l, p=p, q=q, solid=solid, door=door,
                                   bbox=(min(p[0], q[0]), min(p[1], q[1]), max(p[0], q[0]), max(p[1], q[1]))))
        self.spatial = defaultdict(list)
        for i, l in enumerate(self.lines):
            x0, y0, x1, y1 = l["bbox"]
            for x in range(math.floor((x0 - RADIUS) / 128), math.floor((x1 + RADIUS) / 128) + 1):
                for y in range(math.floor((y0 - RADIUS) / 128), math.floor((y1 + RADIUS) / 128) + 1):
                    self.spatial[x, y].append(i)

    def nearby(self, a, b):
        cells = set()
        steps = max(1, int(math.dist(a, b) / 96) + 1)
        for j in range(steps + 1):
            t = j / steps
            x, y = a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    cells.add((math.floor(x / 128) + dx, math.floor(y / 128) + dy))
        ids = set()
        for cell in cells:
            ids.update(self.spatial[cell])
        return ids

    def crossings(self, a, b, doors_only=False):
        result = []
        x0, x1 = sorted((a[0], b[0]))
        y0, y1 = sorted((a[1], b[1]))
        for i in self.nearby(a, b):
            l = self.lines[i]
            if doors_only and not l["door"]:
                continue
            bx0, by0, bx1, by1 = l["bbox"]
            if bx1 < x0 - RADIUS or bx0 > x1 + RADIUS or by1 < y0 - RADIUS or by0 > y1 + RADIUS:
                continue
            if l["solid"]:
                if segment_dist(a, b, l["p"], l["q"]) < RADIUS:
                    return None
            elif intersect(a, b, l["p"], l["q"]):
                if l["door"]:
                    result.append((l["line"]["id"], line_intersection(a, b, l["p"], l["q"])))
        return result

    def walkable(self, a, b):
        return self.crossings(a, b) is not None

    def path(self, start, goal):
        g = self.grid
        def key(p):
            return (round(p[0] / g), round(p[1] / g))
        def point(k):
            return (k[0] * g, k[1] * g)
        sk, gk = key(start), key(goal)
        start = point(sk)
        goal = point(gk)
        queue = [(math.dist(start, goal), 0, sk)]
        costs = {sk: 0}
        parent = {}
        dirs = [(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1) if x or y]
        counter = 0
        while queue:
            _, _, cur = heapq.heappop(queue)
            cp = point(cur)
            expected = costs.get(cur)
            if expected is None:
                continue
            if cur == gk:
                keys = [cur]
                while cur in parent:
                    cur = parent[cur]
                    keys.append(cur)
                keys.reverse()
                return [point(k) for k in keys]
            for dx, dy in dirs:
                nxt = (cur[0] + dx, cur[1] + dy)
                np = point(nxt)
                if abs(np[0]) > 32767 or abs(np[1]) > 32767:
                    continue
                cost = expected + math.hypot(dx, dy) * g
                if cost >= costs.get(nxt, 1e100):
                    continue
                if not self.walkable(cp, np):
                    continue
                costs[nxt] = cost
                parent[nxt] = cur
                counter += 1
                heapq.heappush(queue, (cost + math.dist(np, goal), counter, nxt))
            if counter > 1000000:
                break
        raise RuntimeError(f"No path {start} -> {goal}")

    def simplify(self, path):
        if len(path) < 3:
            return path
        result = [path[0]]
        anchor = 0
        while anchor < len(path) - 1:
            best = anchor + 1
            for j in range(anchor + 2, len(path) + 1):
                if j == len(path):
                    break
                direct_doors = self.crossings(path[anchor], path[j])
                if direct_doors is None:
                    break
                original_doors = []
                for k in range(anchor, j):
                    ds = self.crossings(path[k], path[k + 1], doors_only=True)
                    if ds is None:
                        break
                    original_doors.extend(x[0] for x in ds)
                if sorted(x[0] for x in direct_doors) != sorted(original_doors):
                    if j == anchor + 2:
                        best = anchor + 1
                    break
                best = j
            result.append(path[best])
            anchor = best
        return result

    def actions(self, path):
        result = []
        for a, b in zip(path, path[1:]):
            doors = self.crossings(a, b, doors_only=True)
            if doors is None:
                raise RuntimeError((a, b))
            if result and result[-1][0] == "go" and result[-1][1] == a:
                pass
            else:
                result.append(("go", a))
            for _, p in doors:
                result.append(("use", p))
            result.append(("go", b))
        return result


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("map", type=int)
    ap.add_argument("sx", type=float)
    ap.add_argument("sy", type=float)
    ap.add_argument("gx", type=float)
    ap.add_argument("gy", type=float)
    ap.add_argument("--grid", type=int, default=32)
    args = ap.parse_args()
    nav = Navigator(args.map, args.grid)
    path = nav.path((args.sx, args.sy), (args.gx, args.gy))
    path[0] = (args.sx, args.sy)
    path[-1] = (args.gx, args.gy)
    path = nav.simplify(path)
    print("PATH", len(path))
    for p in path:
        print(p)
    print("ACTIONS")
    for action in nav.actions(path):
        print(action)


if __name__ == "__main__":
    main()
