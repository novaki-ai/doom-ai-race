import sys, math; sys.path.insert(0, '../tools_m45')
from follow import follow
from auto import plan
from wad import read_map
from dbg import load
import sim
m = read_map('E1M4')
UL = {648, 649, 468, 469, 547, 548, 554}
def run_stage(wps, prefix, **kw):
    return follow(4, wps, prefix=prefix, max_tics=900, K=4, m=m, uselines=UL, repeat_use={554}, stop_at_end=True, **kw)
if __name__ == '__main__':
    # stage A: start -> door use
    W = plan('E1M4', (2032, 1120), [(-468, 1580)])
    W += [dict(x=-530, y=1790, r=40), dict(x=-540, y=1860, r=30)]
    tA, rA = run_stage(W, ())
    print('A', len(tA), rA.pos[-1][:3], getattr(rA, 'dead', None))
    sim.write_lmp('m4e_A.lmp', 4, tA)
