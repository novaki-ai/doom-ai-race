#!/usr/bin/env python3
import shutil
import subprocess
import sys

sys.path.insert(0, ".")
from lmp import oku
from race import Router, ROOT

_, tics, _ = oku(ROOT / "tools/work/E1M1/route.lmp")
r = Router(1)
r.demo.tics = list(tics[:386])
r.run()
print("prefix", len(r.demo.tics), r.last, flush=True)
steps = [
    ("go", (2944, -3520), 120),
    ("go", (2944, -3616), 80),
    ("go", (2976, -3648), 50),
    ("go", (3008, -3984), 80),
    ("use", (3008, -4016), 35),
    ("go", (3008, -4608), 90),
    ("use", (3008, -4640), 35),
    ("exit", (2912, -4736), 25),
]
for kind, target, count in steps:
    try:
        if kind == "go":
            r.go(target, maxtics=count, settle=0, buttons=1)
        elif kind == "exit":
            r.turn(target)
            r.demo.extend([(50, 0, 0, 2 if i % 4 == 0 and i < 24 else 0) for i in range(count)])
            r.run()
        else:
            r.use(target, wait=count)
    except RuntimeError as e:
        print(e, flush=True)
        break
    path = r.save("resume")
    shutil.copyfile(path, ROOT / "tools/work/E1M1/resume-latest.lmp")
path = r.save("resume")
r.demo.write(ROOT / "submit/E1M1.lmp")
print(r.run()["analysis"], flush=True)
subprocess.run([sys.executable, str(ROOT / "check.py"), str(ROOT / "submit/E1M1.lmp")])
