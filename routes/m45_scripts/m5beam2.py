import sys, random, time; sys.path.insert(0, '../tools_m45')
from follow import follow
from optimize import jittered, pain_count
from dbg import load
import sim
from m5beam import STAGES
import os
TAG = os.environ.get('TAG', '')
def beam(stage, legs, prefixes, n, bw, jit, seed, final):
    rng = random.Random(seed)
    for li, (leg, kw0) in enumerate(legs):
        last = final and li == len(legs) - 1
        cands = []
        t0 = time.time()
        for pi, pre in enumerate(prefixes):
            for k in range(n * 2 if last else n):
                wps = leg if k == 0 else jittered(leg, jit, rng, keep_last=True)
                kw = dict(kw0); kw['K'] = 4 if k == 0 else rng.choice([3, 4, 4, 5])
                tics, res = follow(5, wps, prefix=pre, stop_at_end=not last, **kw)
                ok = (res.exit_time is not None) if last else (getattr(res, 'reached', False) and not res.dead)
                if ok:
                    key = (res.exit_time,) if last else (pain_count(res), len(tics))
                    cands.append((key, tics))
                    if last: break
        print(f'{stage} leg {li}: {len(cands)} ok of {len(prefixes)}x{n}, best {cands and min(cands)[0]}, {round(time.time()-t0)}s', flush=True)
        if not cands:
            return None, prefixes
        cands.sort(key=lambda c: c[0])
        prefixes = [c[1] for c in cands[:bw]]
        sim.write_lmp(f'{TAG}m5b_{stage}_leg{li}.lmp', 5, prefixes[0])
        for j, p in enumerate(prefixes): sim.write_lmp(f'{TAG}m5b_{stage}_p{j}.lmp', 5, p)
    return cands[0], prefixes
if __name__ == '__main__':
    stage = sys.argv[1]; pres = sys.argv[2].split(','); n, bw, seed = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    prefixes = [load(p) for p in pres]
    best, prefixes = beam(stage, STAGES[stage], prefixes, n, bw, 12, seed, final=(stage == 'S7'))
    print('DONE', stage, best[0] if best else None)
