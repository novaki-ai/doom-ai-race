"""E1M3 legs 20-25 from the leg-19 prefix with medikit pickups, safety-first beam."""
import sys; sys.path.insert(0, '..')
exec(open('e1m3.py').read().split('if __name__')[0].replace("print(i, len(w)", "pass  # print(i, len(w)"))
from lmp import oku
from optimize import beam_legs2
h, t, _ = oku(sys.argv[1]); pre = [(f, s, a >> 8, b) for f, s, a, b in t]
L = {i: (list(w), kw) for i, (w, kw) in enumerate(legs)}
med = lambda x, y: dict(x=x, y=y, r=14, hard=1)
L[20] = ([L[20][0][0], med(-1504, -2990)] + L[20][0][1:], L[20][1])
L[21] = ([L[21][0][0], L[21][0][1], med(-1330, -2528)] + L[21][0][2:], L[21][1])
L[24] = ([L[24][0][0], med(-448, -1612)] + L[24][0][2:], L[24][1])
sub = [L[i] for i in range(20, 26)]
best = beam_legs2(3, sub, n=int(sys.argv[2]) if len(sys.argv) > 2 else 6, beam=3, jitter=10, seed=int(sys.argv[3]) if len(sys.argv) > 3 else 1, out='e1m3_mid.lmp', final_n=6, prefix=pre, safe=True)
