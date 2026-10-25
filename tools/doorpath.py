"""Shortest path with doors listed. usage: doorpath.py E1M7 ax ay bx by [blocked_special,...]"""
import sys, math
from nav import Nav
def run(mp, a, b, blocked_specials=()):
    N = Nav(mp); m = N.m
    door_of = {}
    for i, (v1, v2, fl, sp, tg, s1, s2) in enumerate(m.lines):
        if sp in (1, 26, 27, 28, 31, 32, 33, 34, 117, 118) and m.lsec[i][1] >= 0:
            door_of.setdefault(m.lsec[i][1], set()).add((i, sp))
    bl = {s for s, v in door_of.items() if any(sp in blocked_specials for _, sp in v)}
    for k in range(N.W * N.H):
        if N.sec[k] in bl: N.ok[k] = 0
    r = N.path(a, b)
    if r is None: print('no path'); return
    pts, secs = r
    seen = []
    for s in secs:
        if s in door_of and (not seen or seen[-1] != s): seen.append(s)
    L = sum(math.hypot(p[0] - q[0], p[1] - q[1]) for p, q in zip(pts, pts[1:]))
    print('len', round(L), 'doors', [(s, sorted(door_of[s])) for s in seen])
    sm = N.smooth(pts); print([(round(x), round(y)) for x, y in sm])
if __name__ == '__main__':
    mp = sys.argv[1]; a = tuple(map(float, sys.argv[2:4])); b = tuple(map(float, sys.argv[4:6]))
    bs = tuple(int(x) for x in sys.argv[6].split(',')) if len(sys.argv) > 6 else ()
    run(mp, a, b, bs)
