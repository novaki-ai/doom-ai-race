import sys; sys.path.insert(0, '../tools_m45')
import sim, struct
def load(path):
    b = open(path,'rb').read()
    tics=[]
    i=13
    while b[i]!=0x80:
        f,s,t,bt = struct.unpack('bbbB', b[i:i+4]); tics.append((f,s,t,bt)); i+=4
    return tics
if __name__ == '__main__':
    tics = load(sys.argv[1]); mp = int(sys.argv[2]); a=int(sys.argv[3]); b=int(sys.argv[4])
    res = sim.run(mp, tics)
    for i in range(a, min(b, len(tics))):
        p = res.pos[i] if i < len(res.pos) else None
        print(i, tics[i], [round(v,1) for v in p[:4]] if p else None, p[4:6] if p else None)
