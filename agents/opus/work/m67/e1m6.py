import sys, math, time, json; sys.path.insert(0, '/race/opus/tools_m67')
from follow import follow
from auto import plan
from wad import read_map
import sim
m = read_map('E1M6')
nbr = {i:set() for i in range(len(m.sectors))}
for fs,bs in m.lsec:
    if fs>=0 and bs>=0: nbr[fs].add(bs); nbr[bs].add(fs)
def opened(sec):
    c = min(m.sectors[n][1] for n in nbr[sec] if n!=sec)
    return (None, c-4)
OV = {151:(48,None), 37:opened(37), 28:opened(28)}
BK=(-1536,-1728); YK=(1088,-608); RK=(1680,-1344)
legs = [
 ('red',   (32,-1376), [(RK[0], RK[1], dict(r=16))], set()),
 ('blue',  RK, [(BK[0], BK[1], dict(r=16))], {951}),
 ('l460',  BK, [(1250,-256, dict(r=20))], {935}),
 ('ykey',  (1250,-256), [(YK[0], YK[1], dict(r=16))], {1119, 1139}),
 ('sw822', YK, [(-64, 2330, dict(r=12, face=90, facer=80))], {890, 822}),
 ('exit',  (-64,2330), [(-1500, 1384, dict(r=24, face=0, facer=90)), (-1930, 2016, dict(r=10, face=0, facer=100))], {599, 614, 627}),
]
tics = []
t0 = time.time()
for name, st, goals, ul in legs:
    W = plan('E1M6', st, goals, overrides=OV)
    tics, res = follow(6, W, prefix=tics, max_tics=len(tics)+1500, K=4, m=m, uselines=ul, stop_at_end=(name!='exit'))
    p = res.pos[-1] if res.pos else None
    print(name, 'tics', len(tics), 'exit', res.exit_time, 'dead', getattr(res,'dead',None), 'pos', p[:3] if p else None, 'time %.0f' % (time.time()-t0), flush=True)
    if getattr(res,'dead',False) or res.exit_time: break
sim.write_lmp('/race/opus/work/m67/e1m6_try.lmp', 6, tics)
json.dump(tics, open('/race/opus/work/m67/e1m6_tics.json','w'))
