"""Plan with nav + follow with the engine. legs: list of (goal_x, goal_y) or dicts; uselines: lines to press use on."""
import sys, math
from nav import Nav
from follow import follow
from wad import read_map
import sim

def plan(mapname, start, goals, overrides=None, cost_sec=None, r=40):
    N = Nav(mapname, overrides)
    wps = []
    cur = start
    for g in goals:
        gx, gy = g[:2]
        res = N.path(cur, (gx, gy), cost_sec=cost_sec)
        if res is None:
            raise RuntimeError(f'no path {cur} -> {g}')
        pts, secs = res
        sm = N.smooth(pts)
        for p in sm[1:]:
            wps.append(dict(x=p[0], y=p[1], r=r))
        if len(g) > 2 and isinstance(g[2], dict):
            wps[-1].update(g[2])
        cur = (gx, gy)
    return wps
