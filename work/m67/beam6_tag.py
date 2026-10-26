import sys, math, time, json, random, pickle; sys.path.insert(0, '/race/opus/tools_m67')
from follow import follow
from auto import plan
from legs import hits, jitter
import sim
sys.argv_saved = list(sys.argv)
import m6
from m6 import LEGS, OV, m, D
_st, _goals, _ul = LEGS['Z']
LEGS['Zs'] = (_st, [_goals[0], (272, 1728, dict(r=16, hard=True))] + _goals[1:], _ul)
NV = pickle.load(open(D+'nav6ov2.pkl','rb'))
import os
FA = os.environ.get('FA') == '1'
FA_LEGS = set(os.environ.get('FAL','').split(','))
TAG = os.environ.get('TAG', 'x_')
def leg_wps(leg):
    st, goals, ul = LEGS[leg]
    ov = dict(OV)
    if leg.startswith('Hb'):
        ov[191] = (None, m.sectors[191][0]); ov[214] = (None, m.sectors[214][0])
    W = plan('E1M6', st, goals, overrides=ov)
    if leg in FA_LEGS:
        for w in W:
            if 'face' not in w: w['fire_ahead'] = 1
    if leg == 'Hb2' and 'Hb2east' in FA_LEGS:
        for w in W:
            if w['x'] > 400 and w['y'] < 0: w['fire_ahead'] = 1
    return W, ul
def alive_after(tics, extra=12):
    # check we are not dying shortly after (continue straight with zero input)
    r = sim.run(6, list(tics) + [(0,0,0,0)]*extra)
    return all((p[5] & 0x7fff) < 7 for p in r.pos[-extra-1:])
def expand(prefixes, leg, n, seed, final=False):
    W, ul = leg_wps(leg)
    rng = random.Random(seed)
    out = []
    for pi, pre in enumerate(prefixes):
        for k in range(n):
            Wk = W if k == 0 else jitter(W, rng, 24)
            K = 4 if k == 0 else rng.choice([3,4,5])
            tics, res = follow(6, Wk, prefix=list(pre), max_tics=len(pre)+1500, K=K, m=m, uselines=ul, stop_at_end=not final, nav=NV)
            dead = getattr(res,'dead',False)
            if final:
                ok = res.exit_time is not None
            else:
                p = res.pos[-1]
                ok = (not dead) and math.hypot(p[0]-W[-1]['x'], p[1]-W[-1]['y']) < W[-1].get('r',40)+40 and alive_after(tics)
            h = hits(res, 0)
            print(f'  {leg} p{pi} k{k} tics {len(tics)} ok {ok} hits {h} exit {res.exit_time}', flush=True)
            if ok: out.append((h, len(tics), tics, res.exit_time))
    out.sort(key=lambda c: (c[0], c[1]))
    return out
if __name__ == '__main__':
    start = sys.argv[1]; legs = sys.argv[2].split(','); n = int(sys.argv[3]); beam = int(sys.argv[4])
    prefixes = [json.load(open(D+'m6_'+s_+'.json')) for s_ in start.split('+')]
    for li, leg in enumerate(legs):
        final = (leg in ('Z', 'Zs'))
        c = expand(prefixes, leg, n, int(os.environ.get('SEED','100'))+li, final=final)
        if not c: print('FAILED at', leg); break
        for j, cc in enumerate(c[:beam]):
            json.dump(cc[2], open(D+f'm6_{TAG}{leg}_b{j}.json','w'))
        json.dump(c[0][2], open(D+f'm6_{TAG}{leg}.json','w'))
        print('LEG', leg, 'best', [(cc[0], cc[1], cc[3]) for cc in c[:beam]], flush=True)
        if final:
            sim.write_lmp(D+f'e1m6_final_{TAG}.lmp', 6, c[0][2]); print('EXIT', c[0][3])
            import subprocess, shutil, re as _re
            R='/race/opus/'
            for j, cc in enumerate(c[:beam]):
                cand = R+f'routes/e1m6_{TAG}cand{j}.lmp'
                sim.write_lmp(cand, 6, cc[2])
                out = subprocess.run(['python3', R+'check.py', cand], cwd=R, capture_output=True, text=True).stdout
                print('CHECK', out.strip(), flush=True)
                if out.startswith('PASS'):
                    secs = cc[3]
                    cur = subprocess.run(['python3', R+'check.py', R+'submit/E1M6.lmp'], cwd=R, capture_output=True, text=True).stdout if os.path.exists(R+'submit/E1M6.lmp') else ''
                    m_ = _re.search(r'PASS\s+E1M6\s+(\d+):(\d+\.\d+)', cur)
                    cur_s = int(m_.group(1))*60+float(m_.group(2)) if m_ else None
                    if cur_s is None or secs < cur_s:
                        shutil.copy(cand, R+'submit/E1M6.lmp'); shutil.copy(cand, R+'routes/e1m6_best.lmp')
                        print('SUBMITTED', secs, flush=True)
        prefixes = [cc[2] for cc in c[:beam]]
