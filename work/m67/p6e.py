import sys; sys.path.insert(0, '/race/opus/tools_m67')
from nav import Nav
from wad import read_map
m = read_map('E1M6')
nbr = {i:set() for i in range(len(m.sectors))}
for fs,bs in m.lsec:
    if fs>=0 and bs>=0: nbr[fs].add(bs); nbr[bs].add(fs)
def opened(sec):
    c = min(m.sectors[n][1] for n in nbr[sec] if n!=sec)
    return (None, c-4)
def closed(sec):
    return (None, m.sectors[sec][0])
YEL=[139,142,94]; RED=[174,175]; BLUE=[218,214]
S=(32,-1376)
tests = {
 'allkeys_closed': {s:closed(s) for s in YEL+RED+BLUE},
 'red_open': {s:closed(s) for s in YEL+BLUE},
 'red_blue_open': {s:closed(s) for s in YEL},
}
pts = {'red':(1680,-1344),'blue':(-1536,-1728),'yellow':(1088,-608),'north':(0,1200),'top':(-64,2300),'sw_soul':(-2080,-2368),'east_switch':(2624,-2250),'s193':(1400,-750)}
for name, ov in tests.items():
    N = Nav('E1M6', ov)
    print(name, {k: ('OK' if N.path(S, p) else 'NO') for k,p in pts.items()})
