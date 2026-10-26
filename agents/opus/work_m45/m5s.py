import sys, math, random, time, json, os; sys.path.insert(0, '../tools_m45')
from follow import follow
from wad import read_map
from dbg import load
import sim
m = read_map('E1M5')
def search_leg(name, prefix, base, n, jit, ul=(), rep=(), mt=3000, seed=1, keep=3, goal=None, st=70):
    """random jitter search for one leg; saves the best `keep` alive results as work_m45/<name>_k.lmp"""
    rng = random.Random(seed)
    res_list = []
    t0 = time.time()
    for k in range(n):
        if k == 0: wps = [dict(w) for w in base]
        else:
            wps = []
            for i, w in enumerate(base):
                w = dict(w)
                if not w.get('fixed'):
                    w['x'] += rng.uniform(-jit, jit); w['y'] += rng.uniform(-jit, jit)
                wps.append(w)
        Kk = 4 if k == 0 else rng.choice([3, 4, 4, 5])
        tics, r = follow(5, wps, prefix=prefix, max_tics=mt, K=Kk, m=m, uselines=set(ul), repeat_use=set(rep), stop_at_end=True, stuck_tics=st)
        ok = getattr(r, 'reached', False) and not r.dead
        hp = None
        print(f'{name} trial {k}: ok {ok} tics {len(tics)} pos {[round(v) for v in r.pos[-1][:3]] if r.pos else None} dead {r.dead} {round(time.time()-t0)}s', flush=True)
        if ok:
            res_list.append((len(tics), tics))
            res_list.sort(key=lambda a: a[0])
            res_list = res_list[:keep]
            for j, (L, tt) in enumerate(res_list):
                sim.write_lmp(f'{name}_{j}.lmp', 5, tt)
    return res_list
if __name__ == '__main__':
    pass
