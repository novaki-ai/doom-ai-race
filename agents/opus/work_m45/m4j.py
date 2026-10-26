import sys, math; sys.path.insert(0, '../tools_m45')
from dbg import load
import sim
tB = load(sys.argv[1]); cut = int(sys.argv[2]) if len(sys.argv) > 2 else len(tB)
tB = tB[:cut]
side = -50
good = []
for d in range(0, 3):
    for f0 in range(5, 51, 3):
        run = [(0, 0, 0, 0)] * d + [(f0, -f0, 0, 0)] + [(50, -50, 0, 0)] * 75
        res = sim.run(4, tB + run)
        P = res.pos
        ok = None
        for i in range(len(tB), len(P)):
            if P[i][0] < -1225:
                ok = P[i][2]; break
        mx = min(p[0] for p in P[len(tB):]) if len(P) > len(tB) else None
        dead = P and (P[-1][5] & 0x7fff) >= 7
        print(d, f0, 'landing z', ok, 'minx', round(mx), 'dead', dead, flush=True)
        if ok is not None and ok >= 190: good.append((d, f0))
print('GOOD', good)
