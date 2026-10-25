#!/usr/bin/env python3
"""Official checker for the Doom E1 race (video 020). Usage:
    python3 check.py submit/E1M1.lmp [more.lmp ...] [--json]
For each demo: header rules, input limits (measured from the human record demos), then an official replay in
DSDA-Doom 0.29.4 (complevel 2, shareware DOOM1.WAD) with -levelstat/-analysis. PASS only if the player exits the
level of the demo's own header with no death. The time is DSDA's level time (the leaderboard's time)."""
import json, os, re, shutil, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lmp import oku

DSDA = os.environ.get("RACE_DSDA", "/race/bin/dsda-doom")
IWAD = os.environ.get("RACE_IWAD", "/race/oyun/DOOM1.WAD")
ATTACK, USE = 1, 2
LIMITS = {
    "move_abs_max": 50,            # forwardmove and sidemove, any value in -50..50 (as in the human demos)
    "turn_abs_max": 11776,         # largest single-tic turn in the human record demos (64.7 degrees)
    "turn_reversals_per_35": 6,    # most turn-direction changes in any 35 tics in the human demos
    "attack_presses_per_35": 6, "attack_min_gap": 5,
    "use_presses_per_35": 6, "use_min_gap": 3,
}


def window_max(events, length):
    best = j = 0
    for i in range(len(events)):
        while events[i] - events[j] >= length:
            j += 1
        best = max(best, i - j + 1)
    return best


def input_problems(tics):
    p = []
    for i, (f, s, a, b) in enumerate(tics):
        if abs(f) > LIMITS["move_abs_max"] or abs(s) > LIMITS["move_abs_max"]:
            p.append(f"tic {i}: move {f},{s} outside -50..50"); break
    for i, (f, s, a, b) in enumerate(tics):
        if abs(a) > LIMITS["turn_abs_max"]:
            p.append(f"tic {i}: turn {a} > {LIMITS['turn_abs_max']}"); break
    rev, last = [], 0
    for i, (_, _, a, _) in enumerate(tics):
        d = (a > 0) - (a < 0)
        if d and last and d != last:
            rev.append(i)
        if d:
            last = d
    if window_max(rev, 35) > LIMITS["turn_reversals_per_35"]:
        p.append(f"turn reversals: {window_max(rev, 35)} in 35 tics > {LIMITS['turn_reversals_per_35']}")
    for bit, name in ((ATTACK, "attack"), (USE, "use")):
        ev = [i for i in range(len(tics)) if tics[i][3] & bit and not (tics[i][3] & 128) and (i == 0 or not tics[i - 1][3] & bit)]
        if window_max(ev, 35) > LIMITS[f"{name}_presses_per_35"]:
            p.append(f"{name}: {window_max(ev, 35)} new presses in 35 tics > {LIMITS[name + '_presses_per_35']}")
        gaps = [b - a for a, b in zip(ev, ev[1:])]
        if gaps and min(gaps) < LIMITS[f"{name}_min_gap"]:
            i = gaps.index(min(gaps))
            p.append(f"{name}: new presses {min(gaps)} tics apart at tic {ev[i + 1]} (< {LIMITS[name + '_min_gap']})")
    if any(t[3] & 128 for t in tics):
        p.append("special (pause/save) button events are not allowed")
    return p


def check(path):
    r = {"demo": path, "pass": False, "problems": []}
    try:
        head, tics, _ = oku(path)
    except Exception as e:
        r["problems"].append(f"cannot read demo: {e}"); return r
    m = f"E{head['bolum']}M{head['harita']}"
    r.update(map=m, tics=len(tics))
    if head["surum"] != 109: r["problems"].append(f"demo version {head['surum']} (must be 109, vanilla Doom 1.9)")
    if head["beceri"] != 3: r["problems"].append(f"skill byte {head['beceri']} (must be 3 = Ultra-Violence)")
    if head["bolum"] != 1 or not 1 <= head["harita"] <= 8: r["problems"].append(f"map {m} is not E1M1-E1M8")
    if head["dm"] or head["respawn"] or head["fast"] or head["nomonsters"]: r["problems"].append("deathmatch/respawn/fast/nomonsters set")
    if head["oyuncular"] != [1, 0, 0, 0] or head["oyuncu"] != 0: r["problems"].append("must be single player 1")
    r["problems"] += input_problems(tics)
    with tempfile.TemporaryDirectory() as d:
        raw = open(path, "rb").read()
        end = 13 + 4 * len(tics)
        open(os.path.join(d, "run.lmp"), "wb").write(raw[:end] + b"\x80")  # footer stripped
        try:
            subprocess.run([DSDA, "-iwad", IWAD, "-complevel", "2", "-fastdemo", "run.lmp", "-nodraw", "-nosound", "-nomusic",
                            "-levelstat", "-analysis"], cwd=d, capture_output=True, timeout=600)
        except subprocess.TimeoutExpired:
            r["problems"].append("replay timed out"); return r
        ls = open(os.path.join(d, "levelstat.txt")).read() if os.path.exists(os.path.join(d, "levelstat.txt")) else ""
        an = dict(x.split(" ", 1) for x in open(os.path.join(d, "analysis.txt")).read().splitlines() if " " in x) if os.path.exists(os.path.join(d, "analysis.txt")) else {}
    hit = re.search(rf"^{m} - (\d+):(\d+\.\d+)", ls, re.M)
    if not hit:
        r["problems"].append(f"the player does not exit {m} in the official replay")
    else:
        r["time"] = f"{int(hit.group(1))}:{hit.group(2)}"; r["seconds"] = round(int(hit.group(1)) * 60 + float(hit.group(2)), 2)
    if an.get("reborn", "0") != "0": r["problems"].append("the player died (reborn) in the replay")
    if an.get("turbo", "0") != "0": r["problems"].append("turbo detected")
    if an and an.get("skill") != "4": r["problems"].append(f"replay skill {an.get('skill')} (must be 4)")
    r["category"] = an.get("category")
    r["pass"] = not r["problems"]
    return r


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--json"]
    if not args:
        print(__doc__); sys.exit(2)
    out = [check(a) for a in args]
    if "--json" in sys.argv:
        print(json.dumps(out, indent=1))
    else:
        for r in out:
            print(f"{'PASS' if r['pass'] else 'FAIL'}  {r.get('map', '?')}  {r.get('time', '-')}  {r['demo']}")
            for p in r["problems"]:
                print("   -", p)
    sys.exit(0 if all(r["pass"] for r in out) else 1)
