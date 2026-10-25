"""Demo writer + engine runner. A tic is (forward, side, turn_byte, buttons); turn_byte is the vanilla
high byte of angleturn (-46..46 allowed by the rules). Positions come from DSDA's ghost export."""
import os, struct, subprocess, tempfile, re, math

GAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'game', 'DOOM1.WAD')
WORK = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'work')

def lmp_bytes(mapnum, tics):
    out = bytearray([109, 3, 1, mapnum, 0, 0, 0, 0, 0, 1, 0, 0, 0])
    for f, s, t, b in tics:
        out += struct.pack('bbbB', f, s, t, b)
    out.append(0x80)
    return bytes(out)

def write_lmp(path, mapnum, tics):
    open(path, 'wb').write(lmp_bytes(mapnum, tics))

class Result:
    pass

def run(mapnum, tics, keep=None, _retry=2):
    r = _run(mapnum, tics, keep)
    while _retry and tics and len(tics) > 2 and not r.pos and r.exit_time is None:
        _retry -= 1
        r = _run(mapnum, tics, keep)
    return r

def _run(mapnum, tics, keep=None):
    """Replay; returns Result with .pos list (after each tic: x,y,z,angle(deg),sprite,frame), .exit_time (seconds or None)."""
    os.makedirs(WORK, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=WORK) as d:
        write_lmp(os.path.join(d, 'r.lmp'), mapnum, tics)
        subprocess.run(['dsda-doom', '-iwad', GAME, '-complevel', '2', '-fastdemo', 'r.lmp', '-nodraw', '-nosound', '-nomusic',
                        '-levelstat', '-analysis', '-export_ghost', 'g'], cwd=d, capture_output=True, timeout=120)
        r = Result()
        b = open(os.path.join(d, 'g.gst'), 'rb').read() if os.path.exists(os.path.join(d, 'g.gst')) else b''
        r.pos = []
        for i in range(8, len(b) - 35, 36):
            x, y, z, a, sp, fr, ep, mp, tic = struct.unpack('<iiiIiiiii', b[i:i + 36])
            r.pos.append((x / 65536, y / 65536, z / 65536, a * 360 / 2**32, sp, fr, mp))
        ls = open(os.path.join(d, 'levelstat.txt')).read() if os.path.exists(os.path.join(d, 'levelstat.txt')) else ''
        an = open(os.path.join(d, 'analysis.txt')).read() if os.path.exists(os.path.join(d, 'analysis.txt')) else ''
        r.levelstat = ls
        hit = re.search(rf'^E1M{mapnum} - (\d+):(\d+\.\d+)', ls, re.M)
        r.exit_time = int(hit.group(1)) * 60 + float(hit.group(2)) if hit else None
        r.reborn = 'reborn 1' in an
        if keep:
            write_lmp(keep, mapnum, tics)
        return r
