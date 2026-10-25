"""Random search over waypoint jitter for follow(): keeps the fastest exiting run.
usage in code: best = search(mapnum, base_wps, n=50, jitter=24, follow_kw={...}, out='e1m1_best.lmp')"""
import random, math, copy, time, sys, os
from follow import follow
import sim

def jittered(wps, jit, rng, keep_last=True):
    out = []
    pick = set(rng.sample(range(max(1, len(wps) - 1)), min(2, max(1, len(wps) - 1))))
    for i, w in enumerate(wps):
        w = dict(w)
        if i in pick and not (keep_last and i == len(wps) - 1) and not w.get('fixed'):
            w['x'] += rng.uniform(-jit, jit); w['y'] += rng.uniform(-jit, jit)
            w['r'] = max(10, w.get('r', 40) + rng.uniform(-15, 25))
        out.append(w)
    return out

def search(mapnum, base_wps, n=50, jitter=24, follow_kw=None, out=None, seed=1, best_time=None, log=None, time_limit=None):
    rng = random.Random(seed)
    follow_kw = follow_kw or {}
    best = None
    t0 = time.time()
    for k in range(n):
        if time_limit and time.time() - t0 > time_limit: break
        wps = base_wps if k == 0 else jittered(best[2] if (best and rng.random() < 0.5) else base_wps, jitter, rng)
        kw = dict(follow_kw)
        if k > 0: kw['K'] = rng.choice([3, 4, 4, 5])
        tics, res = follow(mapnum, wps, **kw)
        et = res.exit_time
        msg = f'trial {k} exit {et} tics {len(tics)} dead {getattr(res, "dead", None)}'
        if et is not None and (best is None or et < best[0]):
            best = (et, tics, wps)
            if out and (best_time is None or et < best_time):
                sim.write_lmp(out, mapnum, tics)
                best_time = et
                msg += '  NEW BEST saved'
        print(msg, flush=True)
        if log: open(log, 'a').write(msg + '\n')
    return best


def pain_count(res):
    n, prev = 0, 0
    for p in res.pos:
        f = p[5] & 0x7fff
        if f == 6 and prev != 6: n += 1
        prev = f
    return n

def beam_legs(mapnum, legs, n=12, beam=3, jitter=20, follow_kw=None, seed=1, out=None, log=None, final_n=None):
    """legs: list of waypoint lists. Each leg except the last stops at its last waypoint; the last leg must exit.
    Keeps the `beam` best (fewest tics, then fewest pain hits) alive prefixes after each leg."""
    rng = random.Random(seed)
    follow_kw = dict(follow_kw or {})
    prefixes = [[]]
    for li, leg in enumerate(legs):
        last = li == len(legs) - 1
        cands = []
        for pi, pre in enumerate(prefixes):
            nn = (final_n or n) if last else n
            for k in range(nn):
                wps = leg if k == 0 else jittered(leg, jitter, rng, keep_last=last)
                kw = dict(follow_kw)
                kw['K'] = 4 if k == 0 else rng.choice([3, 4, 4, 5])
                tics, res = follow(mapnum, wps, prefix=pre, stop_at_end=not last, **kw)
                ok = (res.exit_time is not None) if last else (getattr(res, 'reached', False) and not res.dead)
                msg = f'leg {li} prefix {pi} trial {k}: ok {ok} tics {len(tics)} exit {res.exit_time} pain {pain_count(res)}'
                print(msg, flush=True)
                if log: open(log, 'a').write(msg + '\n')
                if ok:
                    key = (res.exit_time if last else len(tics), pain_count(res))
                    cands.append((key, tics, res))
        if not cands:
            print('leg', li, 'failed for all prefixes', flush=True)
            return None
        cands.sort(key=lambda c: c[0])
        # keep distinct prefixes
        prefixes = [c[1] for c in cands[:beam]]
        if last:
            best = cands[0]
            if out: sim.write_lmp(out, mapnum, best[1])
            return best
    return None
