import os,struct,itertools
os.sched_setaffinity(0,{4,5,6,7})
from lmp import oku
from check import check,input_problems
p=oku('work/circlereturn3.lmp')[1];q=oku('submit/E1M3.lmp')[1];h=open('work/circlereturn3.lmp','rb').read()[:13]
best=83.43
for k,j,wait in itertools.product(range(2355,2364),range(2420,2445),[0,1,3]):
 pa=28*256-sum(t[2] for t in p[k:2363]);qa=38*256+(sum(t[2] for t in q[2431:j]) if j>=2431 else -sum(t[2] for t in q[j:2431]))
 delta=(qa-pa+32768)%65536-32768
 f,s,a,b=q[j];new=p[:k]+[(0,0,0,0)]*wait+[(f,s,a+delta,b)]+q[j+1:]
 if input_problems(new):continue
 path='work/splice3candidate.lmp';open(path,'wb').write(h+b''.join(struct.pack('bbbB',f,s,a//256,b) for f,s,a,b in new)+b'\x80')
 r=check(path)
 if r['pass'] and r['seconds']<best:
  best=r['seconds'];open('work/splice3.lmp','wb').write(open(path,'rb').read());print('BEST',k,j,wait,best,flush=True)
