"""Vanilla/Boom .lmp okuyucu (Doom 1.9 = sürüm 109, longtics = 111). Tic başına: forwardmove (int8), sidemove (int8),
angleturn (vanilla: üst bayt int8; longtics: int16), buttons (uint8). Bitiş baytı 0x80; sonrasında DSDA dipnotu olabilir."""
import struct, sys

def oku(yol):
    b = open(yol, "rb").read()
    v = b[0]
    if v not in (109, 111):
        raise ValueError(f"desteklenmeyen demo sürümü {v} ({yol})")
    bas = dict(surum=v, beceri=b[1], bolum=b[2], harita=b[3], dm=b[4], respawn=b[5], fast=b[6], nomonsters=b[7], oyuncu=b[8],
               oyuncular=list(b[9:13]))
    i = 13; ticler = []; uzun = v == 111
    n = sum(1 for x in bas["oyuncular"] if x)
    while i < len(b) and b[i] != 0x80:
        f = struct.unpack("b", b[i:i + 1])[0]; s = struct.unpack("b", b[i + 1:i + 2])[0]
        if uzun:
            a = struct.unpack("<h", b[i + 2:i + 4])[0]; bt = b[i + 4]; i += 5
        else:
            a = struct.unpack("b", b[i + 2:i + 3])[0] << 8; bt = b[i + 3]; i += 4
        ticler.append((f, s, a, bt))
        i += (5 if uzun else 4) * (n - 1)  # yalnız 1. oyuncu
    dip = b[i + 1:].decode("latin-1", "replace") if i < len(b) else ""
    return bas, ticler, dip

if __name__ == "__main__":
    bas, t, dip = oku(sys.argv[1]); print(bas, len(t), "tic", dip[:200])
