"""Run E1M3 sub-legs from a saved prefix: python3 e1m3_legs.py <prefix.lmp|-> <first_leg> <last_leg> <n> <seed> [fire_ahead_legs]"""
import sys; sys.path.insert(0, '..')
src = open('e1m3.py').read().split('if __name__')[0].replace("print(i, len(w)", "pass  # print(i, len(w)")
exec(src)
from lmp import oku
from optimize import beam_legs2
pre = []
if sys.argv[1] != '-':
    h, t, _ = oku(sys.argv[1]); pre = [(f, s, a >> 8, b) for f, s, a, b in t]
a, b, n, seed = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
fa = CORRIDOR if (len(sys.argv) > 6 and sys.argv[6] == 'auto') else (set(int(x) for x in sys.argv[6].split(',')) if len(sys.argv) > 6 else set())
sub = []
for i in range(a, min(b, len(legs) - 1) + 1):
    w, kw = legs[i]
    if i in fa: w = [dict(p, fire_ahead=1) if not (p.get('hard') and p.get('r', 40) <= 14) else p for p in w]
    sub.append((w, kw))
best = beam_legs2(3, sub, n=n, beam=3, jitter=14, seed=seed, out=f'e1m3_from{a}.lmp', final_n=n, prefix=pre, safe=True)
print('BEST', best[0] if best else None)
