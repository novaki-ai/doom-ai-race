import sys, os, pickle
sys.path.insert(0, '/race/opus/tools_m23')
from wad import read_map
from follow import follow
from auto import plan
from seg import pain_count
import sim
m = read_map('E1M2')
OV = {49: (-232, None), 137: (0, None), 129: (None, 60), 124: (None, 60)}
prefix, used0, cur, _ = pickle.load(open('e1m2_seg4.pkl', 'rb'))
goals = eval(sys.argv[1])
K = int(sys.argv[2]) if len(sys.argv) > 2 else 4
wps = plan('E1M2', cur, goals, overrides=OV)
print([(round(w['x']), round(w['y'])) for w in wps])
tics, res = follow(2, wps, prefix=prefix, max_tics=len(prefix) + 900, K=K, m=m, uselines={325, 291, 326, 527, 777, 854, 873}, repeat_use={873}, done_stop=True, used0=used0)
print('exit', res.exit_time, 'dead', res.dead, 'pain', pain_count(res.pos, len(prefix)))
for i in range(len(prefix) + 60, len(res.pos), 3): print(i, [round(v) for v in res.pos[i][:4]], res.pos[i][4:6], tics[i] if i < len(tics) else None)
if res.exit_time: sim.write_lmp('e1m2_dbg5.lmp', 2, tics)
