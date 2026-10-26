import os,struct,itertools
os.sched_setaffinity(0,{4,5,6,7})
from lmp import oku
from check import check,input_problems
p=oku('work/starkey5.lmp')[1];q=oku('work/fastexit5.lmp')[1];h=open('work/starkey5.lmp','rb').read()[:13]
best=108.69
for k,j,wait in itertools.product(range(3175,3184),range(3390,3405),[0,1,3]):
 pa=252*256-sum(t[2] for t in p[k:3183]);qa=241*256+(sum(t[2] for t in q[3395:j]) if j>=3395 else -sum(t[2] for t in q[j:3395]))
 delta=(qa-pa+32768)%65536-32768
 f,s,a,b=q[j];new=p[:k]+[(0,0,0,0)]*wait+[(f,s,a+delta,b)]+q[j+1:]
 if input_problems(new):continue
 path='work/splice5candidate.lmp';open(path,'wb').write(h+b''.join(struct.pack('bbbB',f,s,a//256,b) for f,s,a,b in new)+b'\x80')
 r=check(path)
 if r['pass'] and r['seconds']<best:
  best=r['seconds'];open('work/splice5.lmp','wb').write(open(path,'rb').read());print('BEST',k,j,wait,best,flush=True)
