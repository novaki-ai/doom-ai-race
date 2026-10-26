import sys, math, random, time; sys.path.insert(0, '../tools_m45')
from m4opt import BASE, stageB, runup, finish, m, UL, NAV
from follow import follow
import sim
TXS = (-260, -300, -230, -330)
def stageA2(rng, k):
    wps = [dict(w) for w in BASE]
    if k > 0:
        for i in range(4, 8):
            if rng.random() < 0.5: wps[i]['x'] += rng.uniform(-25, 25); wps[i]['y'] += rng.uniform(-25, 25)
        for i in range(9, 17):
            if rng.random() < 0.3: wps[i]['x'] += rng.uniform(-15, 15); wps[i]['y'] += rng.uniform(-15, 15)
        if rng.random() < 0.5:
            wps.insert(4, dict(x=rng.uniform(820, 1000), y=rng.uniform(1540, 1640), r=40))
    return follow(4, wps, max_tics=500, K=rng.choice([3, 4, 4, 5]) if k else 4, m=m, uselines=UL, repeat_use={554}, stop_at_end=True)
if __name__ == '__main__':
    n, seed, best = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
    rng = random.Random(seed); t0 = time.time()
    for k in range(n):
        tA, rA = stageA2(rng, k)
        uses = [i for i, t in enumerate(tA) if t[3] & 2 and i > 200]
        if rA.dead or not getattr(rA, 'reached', False) or not uses:
            print(k, 'A fail', len(tA), flush=True); continue
        if len(tA) > 340:
            print(k, 'A slow', len(tA), flush=True); continue
        for TX in TXS:
            tB, rB = stageB(tA, TX)
            if rB.dead or not getattr(rB, 'reached', False):
                print(k, 'B fail', len(tA), len(tB), TX, flush=True); continue
            pre = runup(tB)
            if pre is None:
                print(k, 'jump fail', len(tA), len(tB), TX, flush=True); continue
            tics, r = finish(pre)
            print(k, 'A', len(tA), 'B', len(tB), 'TX', TX, 'exit', r.exit_time, 'tics', len(tics), round(time.time() - t0), flush=True)
            if r.exit_time and r.exit_time < best:
                best = r.exit_time
                sim.write_lmp(f'm4opt2_{seed}_{k}.lmp', 4, tics)
                print('NEW BEST', best, flush=True)
            break
