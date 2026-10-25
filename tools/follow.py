"""Closed-loop waypoint follower: the engine is the simulator (replayed every K tics), a simple Doom movement model
plans the tics in between. Respects the race input limits (turn <= 46 per tic, <= 6 reversals / 35 tics,
use presses >= 3 apart and <= 6 / 35, fire presses >= 5 apart and <= 6 / 35)."""
import math, sys
import sim

F = 0xe800 / 65536
TU = 360 / 256          # degrees per turn unit
MAXT = 46

def wrap(d):
    while d > 180: d -= 360
    while d <= -180: d += 360
    return d

class Limits:
    def __init__(s):
        s.rev = []        # tic indices of turn reversals
        s.last = 0
        s.use = []
        s.fire = []
    def can_turn(s, i, t):
        d = (t > 0) - (t < 0)
        if d == 0 or s.last == 0 or d == s.last: return True
        return sum(1 for r in s.rev if r > i - 35) < 6
    def do_turn(s, i, t):
        d = (t > 0) - (t < 0)
        if d and s.last and d != s.last: s.rev.append(i)
        if d: s.last = d
    def can_press(s, lst, i, gap):
        if lst and i - lst[-1] < gap: return False
        return sum(1 for r in lst if r > i - 35) < 6

def rebuild_limits(tics):
    L = Limits()
    prev_b = 0
    for i, (f, s, t, b) in enumerate(tics):
        L.do_turn(i, t)
        if b & 2 and not prev_b & 2: L.use.append(i)
        if b & 1 and not prev_b & 1: L.fire.append(i)
        prev_b = b
    return L

def fs_for(rel):
    """forward/side for a thrust direction rel degrees (ccw) from facing, max magnitude."""
    c, s = math.cos(math.radians(rel)), -math.sin(math.radians(rel))
    m = max(abs(c), abs(s))
    return int(round(50 * c / m)), int(round(50 * s / m))

def thrust_vec(a, f, s):
    ar = math.radians(a)
    k = 2048 / 65536
    return (f * k * math.cos(ar) + s * k * math.sin(ar), f * k * math.sin(ar) - s * k * math.cos(ar))

def plan_tic(i, x, y, a, mx, my, tx, ty, L, deadband=2.0, vmax=23.5, slow=None, face=None):
    """Choose (f, s, turn) to steer toward (tx, ty). face: optional absolute facing to turn to."""
    dx, dy = tx - x, ty - y
    dist = math.hypot(dx, dy) or 1e-6
    v = vmax if slow is None else min(vmax, slow)
    vdx, vdy = v * dx / dist, v * dy / dist
    # want next movement (mom + thrust) ~ desired velocity
    wx, wy = vdx - mx, vdy - my
    phi = math.degrees(math.atan2(wy, wx))
    best = None
    if face is not None:
        best = wrap(face - a)
    else:
        for k in range(4):
            fc = phi + 45 + 90 * k
            d = wrap(fc - a)
            if best is None or abs(d) < abs(best): best = d
    if abs(best) <= deadband:
        t = 0
    else:
        t = int(round(best / TU))
        t = max(-MAXT, min(MAXT, t))
        if not L.can_turn(i, t): t = 0
    na = a + t * TU
    f, s = fs_for(wrap(phi - na))
    return f, s, t

def step_model(x, y, a, mx, my, f, s, t):
    a = a + t * TU
    th = thrust_vec(a, f, s)
    mvx, mvy = mx + th[0], my + th[1]
    return x + mvx, y + mvy, a, mvx * F, mvy * F

def use_hit(m, x, y, a, uselines):
    """first line hit by the 64-unit use ray; returns line index if it is in uselines."""
    ar = math.radians(a)
    ex, ey = x + 64 * math.cos(ar), y + 64 * math.sin(ar)
    best = None
    for li, (v1, v2, fl, sp, tg, s1, s2) in enumerate(m.lines):
        (ax, ay), (bx, by) = m.verts[v1], m.verts[v2]
        d = (ex - x) * (by - ay) - (ey - y) * (bx - ax)
        if d == 0: continue
        t = ((ax - x) * (by - ay) - (ay - y) * (bx - ax)) / d
        u = ((ax - x) * (ey - y) - (ay - y) * (ex - x)) / d
        if 0 <= t <= 1 and 0 <= u <= 1 and (best is None or t < best[0]):
            fs, bs = m.lsec[li]
            if sp or bs < 0 or fl & 1 or True:
                # two-sided non-special lines with an opening are passed through
                if not sp and bs >= 0:
                    f1, c1 = m.sectors[fs][:2]; f2, c2 = m.sectors[bs][:2]
                    if min(c1, c2) - max(f1, f2) > 0: continue
                best = (t, li)
    if best and best[1] in uselines: return best[1]
    return None

DR_SPECIALS = {1, 26, 27, 28, 117}
D1_SPECIALS = {31, 32, 33, 34, 118}
_door_cache = {}
def door_info(m):
    """door sector -> open height (top - floor) for manual doors"""
    key = id(m)
    if key in _door_cache: return _door_cache[key]
    nbr = {}
    for (fs, bs) in m.lsec:
        if fs >= 0 and bs >= 0:
            nbr.setdefault(fs, set()).add(bs); nbr.setdefault(bs, set()).add(fs)
    info = {}
    for i, (v1, v2, fl, sp, tg, s1, s2) in enumerate(m.lines):
        if (sp in DR_SPECIALS or sp in D1_SPECIALS) and m.lsec[i][1] >= 0:
            ds = m.lsec[i][1]
            top = min((m.sectors[n][1] for n in nbr.get(ds, ()) if n != ds), default=m.sectors[ds][1]) - 4
            info[ds] = max(0, top - m.sectors[ds][0])
    _door_cache[key] = info
    return info

def prefix_door_presses(m, prefix, pos):
    """door sector -> last tic a use press hit one of its lines (reconstructed from the replay)."""
    out = {}
    if m is None: return out
    dl = {i for i, l in enumerate(m.lines) if l[3] in DR_SPECIALS or l[3] in D1_SPECIALS}
    prev = 0
    for i, t in enumerate(prefix):
        if t[3] & 2 and not prev & 2 and i >= 1 and i < len(pos):
            hit = use_hit(m, pos[i - 1][0], pos[i - 1][1], pos[i][3], dl)
            if hit is not None:
                out[m.lsec[hit][1]] = (i, m.lines[hit][3])
        prev = t[3]
    return out

def follow(mapnum, wps, prefix=(), max_tics=3000, K=4, verbose=False, stuck_tics=70, m=None, uselines=(), repeat_use=(), stop_at_end=False, nav=None):
    """wps: list of dicts {x, y, r=radius, use=bool, fire=bool, wait=tics, slow=v}. Returns (tics, result)."""
    tics = list(prefix)
    L = rebuild_limits(tics)
    wi = 0
    wi_conf = 0
    used = set(); used_at = {}
    door_press = None
    pending = []          # (tic, line) presses not yet verified against the real replay
    best_prog = (0, 1e9); last_prog_tic = len(tics)
    res = None
    while len(tics) < max_tics:
        res = sim.run(mapnum, tics)
        if res.exit_time is not None:
            return tics, res
        if res.pos and (res.pos[-1][5] & 0x7fff) >= 7 and res.pos[-1][4] == 28:
            if verbose: print('dead at tic', len(tics), res.pos[-1][:2])
            res.dead = True
            return tics, res
        stuck = False
        if len(res.pos) > 8:
            p1, p0 = res.pos[-1], res.pos[-7]
            if math.hypot(p1[0] - p0[0], p1[1] - p0[1]) < 6: stuck = True
        if tics and not res.pos:
            res.dead = True
            return tics, res
        if door_press is None:
            door_press = prefix_door_presses(m, tics, res.pos) if (m is not None and tics) else {}
        if pending and m is not None:
            keep = []
            for (pi_, li_) in pending:
                if pi_ >= len(res.pos):
                    keep.append((pi_, li_)); continue
                act = use_hit(m, res.pos[pi_ - 1][0], res.pos[pi_ - 1][1], res.pos[pi_][3], set(uselines)) if pi_ >= 1 else li_
                if act != li_:
                    # the press missed in reality: forget it so the door gets faced and pressed again
                    grp = {lj for lj in uselines if set(m.lsec[lj]) & ({m.lsec[li_][1]} - {-1})} | {li_}
                    for lj in grp: used.discard(lj)
                    ds_ = m.lsec[li_][1]
                    if ds_ in door_press and door_press[ds_][0] == pi_: door_press.pop(ds_)
                    if act is not None:
                        used.add(act); used_at[act] = pi_
                        if m.lines[act][3] in DR_SPECIALS | D1_SPECIALS: door_press[m.lsec[act][1]] = (pi_, m.lines[act][3])
            pending = keep
        if tics:
            p = res.pos
            if len(p) < len(tics):   # ghost may lag one record
                pass
            x, y, z, a = p[-1][:4]
            if len(p) >= 2:
                mx, my = (p[-1][0] - p[-2][0]) * F, (p[-1][1] - p[-2][1]) * F
            else:
                mx, my = 0, 0
            # ghost has len(tics)-1 records: last record = after tic len(tics)-1; approximate by model step of last tic
            if len(p) == len(tics) - 1:
                f, s, t, b = tics[-1]
                x, y, a, mx, my = step_model(x, y, a, mx, my, f, s, t)
        else:
            x, y, a, mx, my = START[mapnum]
        wi = wi_conf
        for k in range(K):
            i = len(tics)
            # advance waypoints
            while wi < len(wps):
                w = wps[wi]
                if math.hypot(w['x'] - x, w['y'] - y) < w.get('r', 40):
                    wi += 1
                elif (nav is not None and wi + 1 < len(wps) and not (set(w) & {'face', 'use', 'hard', 'fire'})
                      and math.hypot(w['x'] - x, w['y'] - y) < 160 and nav.los((x, y), (wps[wi + 1]['x'], wps[wi + 1]['y']))):
                    wi += 1   # next waypoint already visible: cut the corner
                else:
                    break
            if k == 0:
                wi_conf = wi       # advancement checked against the engine's actual position
                if stop_at_end and wi_conf >= len(wps):
                    res.dead = bool(res.pos and (res.pos[-1][5] & 0x7fff) >= 7)
                    res.reached = True
                    return tics, res
            if wi >= len(wps):
                if stop_at_end:
                    break
                w = wps[-1]
            else:
                w = wps[wi]
            fo = None
            if m is not None:
                for li in uselines:
                    if li in used and li not in repeat_use: continue
                    v1, v2 = m.lines[li][0], m.lines[li][1]
                    (ax, ay), (bx, by) = m.verts[v1], m.verts[v2]
                    vx, vy = bx - ax, by - ay
                    tt = max(0.15, min(0.85, ((x - ax) * vx + (y - ay) * vy) / (vx * vx + vy * vy)))
                    cx, cy = ax + tt * vx, ay + tt * vy
                    if math.hypot(cx - x, cy - y) < 110:
                        fo = math.degrees(math.atan2(cy - y, cx - x)); break
            fire_now = False
            near_door = False
            if m is not None:
                for li in uselines:
                    v1, v2 = m.lines[li][0], m.lines[li][1]
                    (ax, ay), (bx, by) = m.verts[v1], m.verts[v2]
                    if math.hypot((ax + bx) / 2 - x, (ay + by) / 2 - y) < 90: near_door = True
            tap = False
            if w.get('fire_ahead') and fo is None and not near_door:
                if stuck and 'aim' in w:
                    fo = math.degrees(math.atan2(w['aim'][1] - y, w['aim'][0] - x))
                else:
                    fo = math.degrees(math.atan2(w['y'] - y, w['x'] - x))
                fire_now = True; tap = True
            if stuck and fo is None and not near_door:
                if 'aim' in w:
                    ax_, ay_ = w['aim']; fo = math.degrees(math.atan2(ay_ - y, ax_ - x)); fire_now = True; tap = True
                else:
                    fo = math.degrees(math.atan2(w['y'] - y, w['x'] - x)); fire_now = True
            f, s, t = plan_tic(i, x, y, a, mx, my, w['x'], w['y'], L, slow=w.get('slow'), face=fo)
            if 'face' in w and math.hypot(w['x'] - x, w['y'] - y) < w.get('facer', 0):
                d = wrap(w['face'] - a)
                t = max(-MAXT, min(MAXT, int(round(d / TU))))
                if not L.can_turn(i, t): t = 0
                na = a + t * TU
                ph = math.degrees(math.atan2(w['y'] - y, w['x'] - x))
                f, s = fs_for(wrap(ph - na))
            b = 0
            if m is not None and uselines:
                hit = use_hit(m, x, y, a + t * TU, uselines)
                if hit is not None and hit in used and hit not in repeat_use and stuck and i - used_at.get(hit, 0) > 45:
                    used.discard(hit)
                if hit is not None and hit not in repeat_use and m.lsec[hit][1] in door_press:
                    t0, sp0 = door_press[m.lsec[hit][1]]
                    H = door_info(m).get(m.lsec[hit][1], 72)
                    if sp0 in D1_SPECIALS or i - t0 < H / 2 + 150:
                        used.add(hit); used_at.setdefault(hit, i)   # still open (or opening): never press
                    elif hit in used and i - used_at.get(hit, 0) > 45:
                        used.discard(hit)
                if hit is not None and (hit not in used or hit in repeat_use) and L.can_press(L.use, i, 6) and not (tics and tics[-1][3] & 2):
                    b |= 2; used.add(hit); used_at[hit] = i
                    pending.append((i, hit))
                    if m.lsec[hit][1] >= 0 and m.lines[hit][3] in DR_SPECIALS | D1_SPECIALS:
                        door_press[m.lsec[hit][1]] = (i, m.lines[hit][3])
                    # all lines of the same door sector count as used (pressing the far side would close it)
                    for lj in uselines:
                        if lj != hit and set(m.lsec[lj]) & ({m.lsec[hit][1]} - {-1}):
                            used.add(lj); used_at[lj] = i
            # use presses near 'use' waypoints (current or just passed)
            for ww in wps[max(0, wi - 1): wi + 1]:
                if ww.get('use') and math.hypot(ww['x'] - x, ww['y'] - y) < ww.get('user', 96):
                    if L.can_press(L.use, i, 6) and not (tics and tics[-1][3] & 2):
                        b |= 2
            if w.get('fire') and L.can_press(L.fire, i, 6) and not (tics and tics[-1][3] & 1):
                b |= 1
            if fire_now and tap:
                lastp = L.fire[-1] if L.fire else -999
                if i - lastp < 6 and tics and tics[-1][3] & 1:
                    b |= 1                      # keep holding until the shot goes off
                elif i - lastp >= 20 and L.can_press(L.fire, i, 6) and not (tics and tics[-1][3] & 1):
                    b |= 1
            elif fire_now and (tics and tics[-1][3] & 1 or L.can_press(L.fire, i, 6)):
                b |= 1
            L.do_turn(i, t)
            if b & 2 and not (tics and tics[-1][3] & 2): L.use.append(i)
            if b & 1 and not (tics and tics[-1][3] & 1): L.fire.append(i)
            tics.append((f, s, t, b))
            x, y, a, mx, my = step_model(x, y, a, mx, my, f, s, t)
        # progress tracking
        prog = (wi, math.hypot(wps[min(wi, len(wps)-1)]['x'] - x, wps[min(wi, len(wps)-1)]['y'] - y))
        if prog[0] > best_prog[0] or (prog[0] == best_prog[0] and prog[1] < best_prog[1] - 8):
            best_prog = prog; last_prog_tic = len(tics)
        if len(tics) - last_prog_tic > stuck_tics:
            if verbose: print('stuck at wp', wi, 'pos', x, y, 'tic', len(tics))
            break
        if verbose and len(tics) % 40 < K:
            print(f'tic {len(tics)} wp {wi} pos {x:.0f},{y:.0f} ang {a:.0f}')
    res = sim.run(mapnum, tics)
    res.dead = bool(res.pos and (res.pos[-1][5] & 0x7fff) >= 7)
    return tics, res

START = {}
def init_starts():
    from wad import read_map
    for n in range(1, 9):
        m = read_map(f'E1M{n}')
        for (x, y, an, ty, fl) in m.things:
            if ty == 1:
                START[n] = (x, y, an, 0.0, 0.0)
init_starts()
