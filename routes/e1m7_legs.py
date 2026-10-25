"""Run E1M7 legs incrementally from a saved prefix: python3 e1m7_legs.py <prefix.lmp|-> <first_leg> <last_leg> <n> <seed>"""
import sys; sys.path.insert(0, '../tools'); sys.path.insert(0, '..')
src = open('e1m7.py').read().split('n = int')[0].replace("print(i, len(w)", "pass  # print(i, len(w)")
exec(src)
from lmp import oku
from optimize import beam_legs2
pre = []
if sys.argv[1] != '-':
    h, t, _ = oku(sys.argv[1]); pre = [(f, s, a >> 8, b) for f, s, a, b in t]
a, b, n, seed = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
sub = legs[a:b + 1]
best = beam_legs2(7, sub, n=n, beam=2, jitter=14, seed=seed, out=f'e1m7_from{a}.lmp', final_n=n, prefix=pre)
print('BEST', best[0] if best else None)
