import sys; sys.path.insert(0, '../tools')
from optimize import leg_plan, beam_legs2
from wad import read_map
m = read_map('E1M7')
KEYED = {79, 89, 39, 41, 164, 2, 96, 95}
RED, BLUE, YEL = {79}, {89}, {39, 41, 164, 2, 96, 95}
legs = []
def add(wps, doors, nav, stuck=70, extra_use=(), repeat=()):
    kw = dict(max_tics=6000, m=m, uselines=set(doors) | set(extra_use), repeat_use=set(repeat), nav=nav, stuck_tics=stuck)
    legs.append((wps, kw))
# 0: start -> sector 22 (crossing L396 triggers the east lift)
w, d, N = leg_plan('E1M7', (96, 528), (192, 0), blocked=KEYED)
w[-1].update(r=12, hard=1)
w2, d2, N2 = leg_plan('E1M7', (192, 0), (-608, -96), blocked=KEYED)
w2[-1].update(r=12, hard=1)
w3, d3, N3 = leg_plan('E1M7', (-608, -96), (1330, -690), blocked=KEYED)
add(w + w2 + w3, d | d2 | d3, N3)
# 1: onto the lift, ride up, yellow key
w, d, N = leg_plan('E1M7', (1440, -704), (1344, -192), overrides={23: (144, None)}, blocked=RED | BLUE)
w[0]['aim'] = (1440, -352); w[1].setdefault('aim', (1440, -352))
add([dict(x=1440, y=-704, r=14, hard=1, aim=(1296, -752))] + w, d, N, stuck=260)
# 2: yellow key -> sector 67 east of the west lift (crossing L248 triggers it)
w, d, N = leg_plan('E1M7', (1344, -192), (-1236, -70), overrides={70: (48, None)}, blocked=RED | BLUE)
add(w, d, N)
# 3: onto the west lift, ride up, red key
w, d, N = leg_plan('E1M7', (-1376, -64), (-1424, 380), overrides={70: (152, None)}, blocked=RED | BLUE)
add([dict(x=-1376, y=-64, r=14, hard=1)] + w, d, N, stuck=260)
# 4: back onto the lift (crossing L644 lowers it), ride down, step off east
add([dict(x=-1500, y=120, r=30), dict(x=-1376, y=-60, r=14, hard=1), dict(x=-1236, y=-70, r=20, hard=1)], set(), None, stuck=260)
# 5: -> blue key pickup spot (through yellow doors and the red door)
w, d, N = leg_plan('E1M7', (-1236, -70), (-995, 262), overrides={70: (48, None)}, blocked=BLUE, r=40)
w[-1].update(r=10, hard=1)
add(w, d, N)
# 6: -> exit switch (line 810 at x=1952, face east)
w, d, N = leg_plan('E1M7', (-995, 262), (1915, -2304), last_extra=dict(face=0, facer=120, r=8))
add(w, d, N, extra_use={810}, repeat={810})
for i, (w, kw) in enumerate(legs):
    print(i, len(w), [(round(p['x']), round(p['y'])) for p in w][:12], sorted(kw['uselines']))
n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
best = beam_legs2(7, legs, n=n, beam=2, jitter=14, seed=int(sys.argv[2]) if len(sys.argv) > 2 else 1, out='e1m7_beam.lmp', final_n=n)
print('BEST', best[0] if best else None)
