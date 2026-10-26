import sys, math; sys.path.insert(0, '../tools_m45')
from follow import follow
from auto import plan
from wad import read_map
from dbg import load
import sim
m = read_map('E1M5')
def leg(wps, prefix, ul, rep=(), stop=True, mt=3000, **kw):
    return follow(5, wps, prefix=prefix, max_tics=mt, K=4, m=m, uselines=set(ul), repeat_use=set(rep), stop_at_end=stop, **kw)
def show(res, a, step=10):
    for i in range(a, len(res.pos), step): print(i, [round(v) for v in res.pos[i][:3]])
if __name__ == '__main__':
    W1 = [dict(x=x, y=y, r=40) for x, y in [(-116,196), (-92,228), (-100,380), (-436,692), (-452,748), (-548,1196), (-796,1236), (-844,1276), (-980,1276), (-996,1228), (-1156,1212), (-1564,1204), (-1620,1140), (-1620,1084), (-1324,1044)]]
    W1 += [dict(x=-1150, y=832, r=12, face=0, facer=120)]
    t1, r1 = leg(W1, (), [476, 477, 776, 811, 820, 819, 808, 189], rep=[189], verbose=True)
    print('leg1', len(t1), r1.pos[-1][:3], getattr(r1, 'dead', None))
    show(r1, 0, 20)
    sim.write_lmp('m5_l1.lmp', 5, t1)
