#!/usr/bin/env python3
import argparse
import math
import os
from pathlib import Path
import re
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent.parent
WAD = ROOT / "game" / "DOOM1.WAD"
ENGINE = os.environ.get("RACE_DSDA", "dsda-doom")
FRAC = 65536.0
ANGLE = 360.0 / (1 << 32)

THING_NAMES = {
    1: "P1", 2: "P2", 3: "P3", 4: "P4", 11: "DM",
    5: "BKEY", 6: "YKEY", 13: "RKEY", 38: "BSKULL", 39: "RSKULL", 40: "YSKULL",
    2001: "SHOTGUN", 2002: "CHAINGUN", 2003: "ROCKETS", 2004: "PLASMA", 2005: "CHAINSAW", 2006: "BFG",
    2007: "CLIP", 2008: "SHELLS", 2010: "ROCKET", 2047: "CELL", 2048: "AMMOBOX", 2049: "SHELLBOX",
    2011: "STIM", 2012: "MEDI", 2013: "SOUL", 2014: "BONUS", 2015: "HELMET",
    2018: "GREENARMOR", 2019: "BLUEARMOR", 2022: "INVULN", 2023: "BERSERK", 2024: "BLUR", 2025: "SUIT", 2026: "MAP", 2045: "GOGGLES",
    3001: "IMP", 3002: "DEMON", 3003: "BARON", 3004: "TROOPER", 3005: "CACO", 9: "SERGEANT", 58: "SPECTRE",
    16: "CYBER", 7: "SPIDER", 65: "BRUISER",
}
EXIT_SPECIALS = {11, 51, 52, 124}
DOOR_SPECIALS = set(range(1, 5)) | set(range(26, 35)) | set(range(99, 101)) | {117, 118}
KEY_SPECIALS = {26, 27, 28, 32, 33, 34, 99, 100, 133, 134, 135, 136, 137}


def clamp_byte(x):
    return max(-128, min(127, int(x)))


class Demo:
    def __init__(self, mapnum, tics=None):
        self.mapnum = mapnum
        self.tics = list(tics or [])

    def write(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        header = struct.pack("13B", 109, 3, 1, self.mapnum, 0, 0, 0, 0, 0, 1, 0, 0, 0)
        body = bytearray()
        for f, s, a, b in self.tics:
            if not (-50 <= f <= 50 and -50 <= s <= 50 and -11776 <= a <= 11776 and a % 256 == 0):
                raise ValueError((f, s, a, b))
            body += struct.pack("bbbB", f, s, a // 256, b)
        path.write_bytes(header + body + b"\x80")

    def extend(self, tics):
        self.tics.extend(tics)


def read_ghost(path):
    data = Path(path).read_bytes()
    if len(data) < 8:
        return []
    version, count = struct.unpack_from("<ii", data)
    if version != 2 or count != 1:
        raise ValueError((version, count))
    frames = []
    for off in range(8, len(data), 36):
        x, y, z, angle, sprite, frame, mapnum, episode, tic = struct.unpack_from("<iiiIiiiii", data, off)
        frames.append(dict(x=x / FRAC, y=y / FRAC, z=z / FRAC, angle=angle * ANGLE,
                           raw_angle=angle, sprite=sprite, frame=frame, map=mapnum, tic=tic))
    return frames


def replay(path, keep=None):
    path = Path(path).resolve()
    with tempfile.TemporaryDirectory(dir=ROOT / "tools") as tmp:
        tmp = Path(tmp)
        cmd = [ENGINE, "-iwad", str(WAD), "-complevel", "2", "-fastdemo", str(path),
               "-nodraw", "-nosound", "-nomusic", "-levelstat", "-analysis", "-export_ghost", "trace"]
        proc = subprocess.run(cmd, cwd=tmp, capture_output=True, text=True, timeout=120)
        frames = read_ghost(tmp / "trace.gst") if (tmp / "trace.gst").exists() else []
        levelstat = (tmp / "levelstat.txt").read_text() if (tmp / "levelstat.txt").exists() else ""
        analysis = (tmp / "analysis.txt").read_text() if (tmp / "analysis.txt").exists() else ""
        if keep:
            keep = Path(keep)
            keep.mkdir(parents=True, exist_ok=True)
            (keep / "stdout.txt").write_text(proc.stdout + proc.stderr)
            (keep / "levelstat.txt").write_text(levelstat)
            (keep / "analysis.txt").write_text(analysis)
            if frames:
                (keep / "trace.txt").write_text("\n".join(
                    f"{f['tic']:5} {f['x']:10.3f} {f['y']:10.3f} {f['z']:8.2f} {f['angle']:8.3f}" for f in frames) + "\n")
        return dict(frames=frames, levelstat=levelstat, analysis=analysis, output=proc.stdout + proc.stderr, returncode=proc.returncode)


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def angle_to(a, b):
    return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])) % 360


def signed_angle(x):
    return (x + 180) % 360 - 180


def turn_tics(frame, target_angle):
    current = frame["raw_angle"] >> 24
    target = int(round(target_angle / 360 * 256)) % 256
    delta = ((target - current + 128) % 256) - 128
    sign = 1 if delta >= 0 else -1
    tics = []
    while delta:
        step = max(-46, min(46, delta))
        tics.append((0, 0, step * 256, 0))
        delta -= step
    return tics


class Router:
    def __init__(self, mapnum, work="tools/work"):
        self.demo = Demo(mapnum)
        self.work = ROOT / work / f"E1M{mapnum}"
        self.work.mkdir(parents=True, exist_ok=True)
        start = next(t for t in Wad().map(mapnum).things if t["type"] == 1)
        self.last = dict(x=float(start["x"]), y=float(start["y"]), z=0.0,
                         angle=float(start["angle"]), raw_angle=start["angle"] * (1 << 32) // 360)
        self.trace = []
        self.log = []

    def save(self, name="route"):
        path = self.work / f"{name}.lmp"
        self.demo.write(path)
        return path

    def run(self):
        path = self.save()
        result = replay(path)
        self.trace = result["frames"]
        if self.trace:
            self.last = self.trace[-1]
        return result

    def turn(self, target):
        if self.last is None:
            self.run()
        if isinstance(target, (tuple, list)):
            target = angle_to((self.last["x"], self.last["y"]), target)
        count = 0
        for _ in range(16):
            tics = turn_tics(self.last, target)
            if not tics:
                break
            self.demo.extend(tics)
            count += len(tics)
            self.demo.tics.append((0, 0, 0, 0))
            self.run()
            self.demo.tics.pop()
        else:
            raise RuntimeError(f"Turn did not reach {target}: {self.last['angle']}")
        self.log.append(f"turn {target:.2f}: {count} tics, end {self.pos()}")
        return self

    def pos(self):
        return None if self.last is None else (round(self.last["x"], 2), round(self.last["y"], 2))

    def go(self, target, maxtics=300, threshold=24, forward=50, side=0, buttons=0, name="go", settle=10):
        if self.last is None:
            self.run()
        start_len = len(self.demo.tics)
        move_angle = angle_to((self.last["x"], self.last["y"]), target) + math.degrees(math.atan2(side, forward))
        self.turn(move_angle)
        move_start = len(self.demo.tics)
        self.demo.extend([(forward, side, 0, buttons)] * maxtics)
        result = self.run()
        frames = self.trace
        candidates = []
        for i in range(move_start, len(frames)):
            f = frames[i]
            d = math.hypot(f["x"] - target[0], f["y"] - target[1])
            candidates.append((d, i))
        if not candidates:
            raise RuntimeError("No movement frames")
        best_d, best_i = min(candidates)
        keep = best_i + 1 - move_start
        self.demo.tics = self.demo.tics[:move_start] + self.demo.tics[move_start:move_start + keep]
        self.demo.extend([(0, 0, 0, 0)] * settle)
        self.run()
        self.log.append(f"{name} -> {target}: {keep} tics, miss {best_d:.1f}, end {self.pos()}, total {len(self.demo.tics)}")
        print(self.log[-1], flush=True)
        (self.work / "route.log").write_text("\n".join(self.log) + "\n")
        return best_d <= threshold

    def legal_turn(self, step):
        if not step:
            return 0
        sign = 1 if step > 0 else -1
        last = 0
        reversals = []
        for i, (_, _, a, _) in enumerate(self.demo.tics):
            direction = (a > 0) - (a < 0)
            if direction and last and direction != last:
                reversals.append(i)
            if direction:
                last = direction
        now = len(self.demo.tics)
        if last and sign != last and sum(now - r < 35 for r in reversals) >= 6:
            return 0
        return step

    def servo(self, target, maxtics=300, threshold=2, **_):
        self.turn(angle_to((self.last["x"], self.last["y"]), target))
        facing = math.radians(self.last["angle"])
        forward_unit = (math.cos(facing), math.sin(facing))
        side_unit = (math.sin(facing), -math.cos(facing))
        if len(self.trace) >= 2:
            velocity = [self.trace[-1]["x"] - self.trace[-2]["x"], self.trace[-1]["y"] - self.trace[-2]["y"]]
        else:
            velocity = [0.0, 0.0]
        stalled = 0
        start_len = len(self.demo.tics)
        for n in range(maxtics):
            old = self.last
            dx, dy = target[0] - old["x"], target[1] - old["y"]
            distance = math.hypot(dx, dy)
            speed = math.hypot(*velocity)
            if distance < threshold and speed < 1.8:
                break
            desired_speed = min(14.0, distance * 0.3)
            desired = [dx / distance * desired_speed, dy / distance * desired_speed] if distance else [0.0, 0.0]
            correction = [desired[0] - velocity[0], desired[1] - velocity[1]]
            forward = max(-50, min(50, round(32 * (correction[0] * forward_unit[0] + correction[1] * forward_unit[1]))))
            side = max(-50, min(50, round(32 * (correction[0] * side_unit[0] + correction[1] * side_unit[1]))))
            attack = 1 if stalled >= 4 else 0
            self.demo.tics.append((forward, side, 0, attack))
            self.demo.tics.append((0, 0, 0, attack))
            self.run()
            self.demo.tics.pop()
            velocity = [self.last["x"] - old["x"], self.last["y"] - old["y"]]
            if math.hypot(*velocity) < 0.05 and distance >= threshold:
                stalled += 1
            else:
                stalled = 0
            if stalled >= 120:
                raise RuntimeError(f"Servo stuck at {self.pos()} -> {target}")
        else:
            raise RuntimeError(f"Servo timed out at {self.pos()} -> {target}")
        self.log.append(f"servo -> {target}: {len(self.demo.tics) - start_len} tics, end {self.pos()}, total {len(self.demo.tics)}")
        print(self.log[-1], flush=True)
        return True

    def wait(self, n, buttons=0):
        self.demo.extend([(0, 0, 0, buttons)] * n)
        self.run()
        self.log.append(f"wait {n}: end {self.pos()}, total {len(self.demo.tics)}")
        return self

    def use(self, target=None, wait=18):
        if target is not None:
            self.turn(target)
        self.demo.extend([(50, 0, 0, 2)] + [(50, 0, 0, 0)] * (wait + 1))
        self.demo.tics.append((0, 0, 0, 0))
        self.run()
        self.demo.tics.pop()
        self.log.append(f"use {target}: end {self.pos()}, total {len(self.demo.tics)}")
        print(self.log[-1], flush=True)
        return self

    def fire(self, n, target=None):
        if target is not None:
            self.turn(target)
        self.demo.extend([(0, 0, 0, 1)] * n + [(0, 0, 0, 0)])
        self.run()
        self.log.append(f"fire {n}: end {self.pos()}, total {len(self.demo.tics)}")
        print(self.log[-1], flush=True)
        return self


class Wad:
    def __init__(self, path=WAD):
        self.data = Path(path).read_bytes()
        magic, count, directory = struct.unpack_from("<4sii", self.data)
        if magic != b"IWAD":
            raise ValueError(magic)
        self.entries = []
        self.order = []
        for i in range(count):
            pos, size, name = struct.unpack_from("<ii8s", self.data, directory + i * 16)
            name = name.rstrip(b"\0").decode("ascii")
            self.entries.append((name, self.data[pos:pos + size]))
            self.order.append(name)

    def map(self, mapnum):
        name = f"E1M{mapnum}"
        start = self.order.index(name)
        lumps = dict(self.entries[start + 1:start + 11])
        return DoomMap(name, lumps)


class DoomMap:
    def __init__(self, name, lumps):
        self.name = name
        self.things = [dict(x=x, y=y, angle=a, type=t, flags=f) for x, y, a, t, f in
                       struct.iter_unpack("<hhHHH", lumps["THINGS"])]
        self.vertices = list(struct.iter_unpack("<hh", lumps["VERTEXES"]))
        self.lines = []
        for i, (v1, v2, flags, special, tag, right, left) in enumerate(struct.iter_unpack("<HHHHHHH", lumps["LINEDEFS"])):
            self.lines.append(dict(id=i, v1=v1, v2=v2, flags=flags, special=special, tag=tag, right=right, left=left))
        self.sidedefs = []
        for raw in struct.iter_unpack("<hh8s8s8sH", lumps["SIDEDEFS"]):
            self.sidedefs.append(dict(xoff=raw[0], yoff=raw[1], upper=raw[2], lower=raw[3], middle=raw[4], sector=raw[5]))
        self.sectors = []
        for raw in struct.iter_unpack("<hh8s8sHHH", lumps["SECTORS"]):
            self.sectors.append(dict(floor=raw[0], ceiling=raw[1], floortex=raw[2], ceiltex=raw[3], light=raw[4], special=raw[5], tag=raw[6]))

    def point(self, line, first=True):
        return self.vertices[line["v1" if first else "v2"]]

    def describe(self):
        out = [self.name, f"{len(self.things)} things, {len(self.lines)} lines, {len(self.sectors)} sectors"]
        for i, t in enumerate(self.things):
            if t["type"] in THING_NAMES and (t["type"] < 100 or 2000 <= t["type"] < 3000):
                out.append(f"thing {i:3}: {THING_NAMES[t['type']]:10} ({t['x']},{t['y']}) angle {t['angle']}")
        out.append("Special lines:")
        for l in self.lines:
            if l["special"]:
                p, q = self.point(l), self.point(l, False)
                out.append(f"line {l['id']:4}: special {l['special']:3} tag {l['tag']:3} {p}->{q}")
        return "\n".join(out)

    def render(self, path, labels=False):
        from PIL import Image, ImageDraw
        xs = [p[0] for p in self.vertices]
        ys = [p[1] for p in self.vertices]
        margin = 60
        scale = min(1500 / (max(xs) - min(xs) + 1), 1100 / (max(ys) - min(ys) + 1))
        w = int((max(xs) - min(xs)) * scale) + margin * 2
        h = int((max(ys) - min(ys)) * scale) + margin * 2
        im = Image.new("RGB", (w, h), "#101018")
        d = ImageDraw.Draw(im)
        def xy(p):
            return (margin + (p[0] - min(xs)) * scale, h - margin - (p[1] - min(ys)) * scale)
        for l in self.lines:
            p, q = xy(self.point(l)), xy(self.point(l, False))
            color = "#555566" if l["left"] != 65535 else "#dddddd"
            width = 1 if l["left"] != 65535 else 2
            if l["special"] in EXIT_SPECIALS:
                color, width = "#ff30d0", 4
            elif l["special"] in KEY_SPECIALS:
                color, width = "#ffee20", 4
            elif l["special"] in DOOR_SPECIALS:
                color, width = "#30c8ff", 3
            elif l["special"]:
                color = "#888833"
            d.line((p, q), fill=color, width=width)
            if labels and l["special"]:
                mid = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
                d.text(mid, f"{l['id']}:{l['special']}", fill=color)
        for i, t in enumerate(self.things):
            p = xy((t["x"], t["y"]))
            typ = t["type"]
            if typ == 1:
                color, r = "#40ff60", 8
            elif typ in (5, 6, 13, 38, 39, 40):
                color, r = {5: "#4080ff", 38: "#4080ff", 6: "#ffff40", 40: "#ffff40"}.get(typ, "#ff4040"), 7
            elif 2000 <= typ < 3000:
                color, r = "#ffffff", 4
            elif typ in THING_NAMES:
                color, r = "#ff5050", 2
            else:
                continue
            d.ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), fill=color)
            if labels and (typ == 1 or typ in (5, 6, 13, 38, 39, 40) or 2000 <= typ < 3000):
                d.text((p[0] + 5, p[1] + 4), f"{i}:{THING_NAMES.get(typ, typ)}", fill=color)
        d.text((10, 10), f"{self.name}  scale {scale:.3f}", fill="white")
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        im.save(path)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("map")
    p.add_argument("maps", nargs="+", type=int)
    p.add_argument("--labels", action="store_true")
    p = sub.add_parser("trace")
    p.add_argument("demo")
    p.add_argument("--keep")
    args = ap.parse_args()
    wad = Wad()
    if args.cmd == "map":
        for n in args.maps:
            m = wad.map(n)
            (ROOT / "tools" / "work").mkdir(parents=True, exist_ok=True)
            (ROOT / "tools" / "work" / f"E1M{n}.txt").write_text(m.describe())
            m.render(ROOT / "tools" / "work" / f"E1M{n}.png", args.labels)
            print(m.describe())
    elif args.cmd == "trace":
        result = replay(args.demo, args.keep)
        print(result["output"])
        print(result["levelstat"])
        print(result["analysis"])
        for f in result["frames"]:
            print(f"{f['tic']:5} {f['x']:10.3f} {f['y']:10.3f} {f['z']:8.2f} {f['angle']:8.3f}")


if __name__ == "__main__":
    main()
