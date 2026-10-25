import sys; sys.path.insert(0, '../tools'); sys.path.append('../tools_m23')
from optimize import leg_plan, beam_legs2
from openall import open_all
from wad import read_map
m = read_map('E1M3')
ov = open_all('E1M3')
steps = [16, 17, 18, 19, 8, 9, 10, 11, 12, 13]
ov2 = dict(ov)
for k, s in enumerate(steps):
    ov2[s] = (m.sectors[s][0] + 8 * (k + 2), None)
legs = []
def add(wps, doors, nav, stuck=70, extra_use=(), repeat=()):
    kw = dict(max_tics=5000, m=m, uselines=set(doors) | set(extra_use), repeat_use=set(repeat), nav=nav, stuck_tics=stuck)
    legs.append((wps, kw))
# 0: start -> blue key
w, d, N = leg_plan('E1M3', (-1472, -3344), (-158, -862), overrides=ov, blocked={61})
w[-1].update(r=10, hard=1)
add(w, d, N)
# 1: blue key -> across stair trigger line 967 (x=-256)
w, d, N = leg_plan('E1M3', (-158, -862), (-300, -1600), overrides=ov)
w.append(dict(x=-200, y=-1600, r=20, hard=1))
add(w, d, N)
# 2: stairs (wait for them to rise) -> exit switch line 982 (face south)
w, d, N = leg_plan('E1M3', (-200, -1600), (704, -1724), overrides=ov2, last_extra=dict(face=270, facer=120, r=8))
add(w, d, N, stuck=300, extra_use={982}, repeat={982})
for i, (w, kw) in enumerate(legs):
    print(i, len(w), [(round(p['x']), round(p['y'])) for p in w][:8], sorted(kw['uselines']))
if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    best = beam_legs2(3, legs, n=n, beam=2, jitter=14, seed=int(sys.argv[2]) if len(sys.argv) > 2 else 1, out='e1m3_beam.lmp', final_n=n)
    print('BEST', best[0] if best else None)
