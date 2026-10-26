import os,sys,random,struct,time,json
os.sched_setaffinity(0,{4,5,6,7})
from check import check,input_problems
from lmp import oku
m=int(sys.argv[1]);random.seed(m+12)
src=f'submit/E1M{m}.lmp';raw=open(src,'rb').read();header=raw[:13];t=oku(src)[1];best=check(src)['seconds'];start=time.time();attempt=0
path=f'work/prune{m}.lmp';candidate=f'work/candidate{m}.lmp'
while time.time()-start<600:
 attempt+=1
 size=random.choice([1,1,1,2,2,3,4,5,8,12,16,24,35,50,70,100])
 i=random.randrange(1,len(t)-size)
 cut=t[i:i+size]
 # Retain heading. Removed movements or pauses may be redundant.
 if sum(x[2] for x in cut)!=0:continue
 new=t[:i]+t[i+size:]
 if input_problems(new):continue
 open(candidate,'wb').write(header+b''.join(struct.pack('bbbB',f,s,a//256,b) for f,s,a,b in new)+b'\x80')
 r=check(candidate)
 if r['pass'] and r['seconds']<best:
  best=r['seconds'];t=new;open(path,'wb').write(open(candidate,'rb').read());print('BEST',m,best,'removed',i,size,'attempt',attempt,flush=True)
print('DONE',m,best,attempt,flush=True)
