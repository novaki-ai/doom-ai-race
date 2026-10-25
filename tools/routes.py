#!/usr/bin/env python3
import argparse
import shutil
import subprocess
import sys

from race import ROOT, Router, dist
from nav import Navigator


def follow(r, goal):
    start = (r.last["x"], r.last["y"])
    nav = Navigator(r.demo.mapnum)
    sx, sy = round(start[0] / 32), round(start[1] / 32)
    gx, gy = round(goal[0] / 32), round(goal[1] / 32)
    starts = [(x * 32, y * 32) for x in range(sx - 2, sx + 3) for y in range(sy - 2, sy + 3)]
    goals = [(x * 32, y * 32) for x in range(gx - 1, gx + 2) for y in range(gy - 1, gy + 2)]
    starts.sort(key=lambda p: dist(start, p))
    goals.sort(key=lambda p: dist(goal, p))
    path = None
    for sp in starts:
        if not nav.walkable(start, sp):
            continue
        for gp in goals:
            if not nav.walkable(gp, goal):
                continue
            try:
                path = [start] + nav.path(sp, gp) + [goal]
                break
            except RuntimeError:
                pass
        if path:
            break
    if path is None:
        raise RuntimeError(f"Cannot attach route {start} -> {goal}")
    simplified = nav.simplify(path)
    for point in simplified[1:]:
        if dist((r.last["x"], r.last["y"]), point) > 2:
            r.servo(point, maxtics=300)
    return r


def route1():
    r = Router(1)
    follow(r, (1490, -2528))
    r.use((1536, -2528), wait=35)
    follow(r, (3008, -3984))
    r.use((3008, -4016), wait=35)
    r.go((3008, -4608), maxtics=45, settle=0, buttons=1)
    r.use((3008, -4640), wait=35)
    r.go((2960, -4768), maxtics=8, settle=0)
    r.use((2912, -4768), wait=4)
    return r


ROUTES = {1: route1}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("maps", nargs="+", type=int)
    ap.add_argument("--no-submit", action="store_true")
    args = ap.parse_args()
    for n in args.maps:
        r = ROUTES[n]()
        path = r.save("final")
        result = r.run()
        print(result["levelstat"], result["analysis"], sep="\n")
        if not args.no_submit:
            shutil.copyfile(path, ROOT / "submit" / f"E1M{n}.lmp")
            subprocess.run([sys.executable, str(ROOT / "check.py"), str(ROOT / "submit" / f"E1M{n}.lmp")])


if __name__ == "__main__":
    main()
