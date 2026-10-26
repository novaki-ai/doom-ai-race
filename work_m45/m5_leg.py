import sys, random, time, json; sys.path.insert(0, '../tools_m45')
from follow import follow
from wad import read_map
from dbg import load
import sim
m = read_map('E1M5')
FA = False
def run(pre_file, P, n, seed, out, ul=(), rep=(), jit=15, mt=800, st=70, fixed_last=True, extra_last=None):
    pre = load(pre_file) if pre_file else []
    rng = random.Random(seed); t0 = time.time(); best = None
    for k in range(n):
        W = []
        for i, p in enumerate(P):
            x, y = p[:2]; r = p[2] if len(p) > 2 else 30
            if k and not (fixed_last and i == len(P) - 1) and not (len(p) > 3 and p[3]):
                x += rng.uniform(-jit, jit); y += rng.uniform(-jit, jit)
            W.append(dict(x=x, y=y, r=r))
        if extra_last: W[-1].update(extra_last)
        if FA:
            for w in W: w['fire_ahead'] = 1
        tics, r = follow(5, W, prefix=pre, max_tics=mt, K=rng.choice([3, 4, 4, 5]) if k else 4, m=m, uselines=set(ul), repeat_use=set(rep), stop_at_end=True, stuck_tics=st)
        ok = getattr(r, 'reached', False) and not r.dead
        print(k, 'ok', ok, 'tics', len(tics), 'pos', [round(v) for v in r.pos[-1][:3]] if r.pos else None, 'dead', r.dead, round(time.time() - t0), flush=True)
        if ok and (best is None or len(tics) < best):
            best = len(tics); sim.write_lmp(out, 5, tics)
    print('BEST', best)
    return best
