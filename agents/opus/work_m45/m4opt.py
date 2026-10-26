import sys, math, random, time; sys.path.insert(0, '../tools_m45')
from follow import follow
from auto import plan
from wad import read_map
from nav import Nav
import sim
m = read_map('E1M4')
NAV = Nav('E1M4')
UL = {648, 649, 468, 469, 547, 548, 554}
BASE = plan('E1M4', (2032, 1120), [(-468, 1580)]) + [dict(x=-530, y=1790, r=40), dict(x=-540, y=1860, r=30)]
def stageA(rng, k, use_nav):
    wps = []
    for i, w in enumerate(BASE):
        w = dict(w)
        if k > 0 and i < len(BASE) - 2 and rng.random() < 0.35:
            w['x'] += rng.uniform(-20, 20); w['y'] += rng.uniform(-20, 20)
        wps.append(w)
    kw = dict(nav=NAV) if use_nav else {}
    return follow(4, wps, max_tics=500, K=rng.choice([3, 4, 4, 5]) if k else 4, m=m, uselines=UL, repeat_use={554}, stop_at_end=True, **kw)
def stageB(tA, TX, TY=1888):
    WB = [dict(x=-470, y=TY, r=12), dict(x=TX, y=TY, r=25, face=135, facer=400)]
    return follow(4, WB, prefix=tA, max_tics=700, K=4, m=m, uselines={547, 548, 554}, repeat_use={554}, stop_at_end=True)
def runup(tB):
    for d in range(0, 3):
        for f0 in range(5, 51, 3):
            run = [(0, 0, 0, 0)] * d + [(f0, -f0, 0, 0)] + [(50, -50, 0, 0)] * 75
            res = sim.run(4, tB + run)
            P = res.pos
            for i in range(len(tB), len(P)):
                if P[i][0] < -1235:
                    if P[i][2] >= 190:
                        return (tB + run)[:i + 1]
                    break
    return None
def finish(pre):
    W = [dict(x=-1440, y=1888, r=20), dict(x=-1570, y=1888, r=10, face=180, facer=100)]
    return follow(4, W, prefix=pre, max_tics=800, K=4, m=m, uselines={547, 548, 554}, repeat_use={554})
if __name__ == '__main__':
    n, seed, best = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
    rng = random.Random(seed); t0 = time.time()
    for k in range(n):
        use_nav = rng.random() < 0.5
        tA, rA = stageA(rng, k, use_nav)
        uses = [i for i, t in enumerate(tA) if t[3] & 2 and i > 200]
        if rA.dead or not getattr(rA, 'reached', False) or not uses:
            print(k, 'A fail', len(tA), 'nav', use_nav, flush=True); continue
        TX = rng.uniform(-330, -200)
        tB, rB = stageB(tA, TX)
        if rB.dead or not getattr(rB, 'reached', False):
            print(k, 'B fail', len(tA), len(tB), flush=True); continue
        pre = runup(tB)
        if pre is None:
            print(k, 'jump fail', len(tA), len(tB), round(TX), flush=True); continue
        tics, r = finish(pre)
        print(k, 'A', len(tA), 'B', len(tB), 'TX', round(TX), 'nav', use_nav, 'exit', r.exit_time, 'tics', len(tics), round(time.time() - t0), flush=True)
        if r.exit_time and r.exit_time < best:
            best = r.exit_time
            sim.write_lmp(f'm4opt_{seed}_{k}.lmp', 4, tics)
            print('NEW BEST', best, flush=True)
