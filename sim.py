import os,subprocess,struct,json,math
from wad import Wad
ROOT=os.path.dirname(os.path.abspath(__file__))
class Sim:
 def __init__(self,m):
  self.m=m;self.wad=Wad(m);self.t=[];self.trace=[];self.state={};self.prefix=ROOT+f'/work/sim{os.getpid()}'
  for ext in ['in','out']:
   p=self.prefix+'.'+ext
   if os.path.exists(p):os.unlink(p)
   os.mkfifo(p)
  open(self.prefix+'.lmp','wb').write(bytes([109,3,1,m,0,0,0,0,0,1,0,0,0])+bytes(400000)+b'\x80')
  env=os.environ.copy();env.update(RACE_IN=self.prefix+'.in',RACE_OUT=self.prefix+'.out',SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',LD_LIBRARY_PATH=ROOT+'/deps/root/usr/lib/x86_64-linux-gnu:/opt/dsda-doom/usr/lib/x86_64-linux-gnu')
  self.log=open(self.prefix+'.log','w')
  self.p=subprocess.Popen([ROOT+'/build/dsda-doom','-iwad',ROOT+'/game/DOOM1.WAD','-complevel','2','-fastdemo',self.prefix+'.lmp','-nodraw','-nosound','-nomusic','-data',ROOT+'/work'],cwd=ROOT+'/work',env=env,stdout=self.log,stderr=self.log)
  self.out=open(self.prefix+'.out');self.inp=open(self.prefix+'.in','w',buffering=1);self.read()
 def read(self):
  s=self.out.readline()
  if not s:
   log=open(self.prefix+'.log').read()
   if 'FINISHED:' in log:
    self.state['state']=1;return self.state
   raise RuntimeError('sim ended: '+log[-500:])
  self.state=json.loads(s);self.trace.append((self.state['x'],self.state['y']));return self.state
 def step(self,f=0,s=0,a=0,b=0,n=1):
  for _ in range(n):
   if self.state.get('state',0)!=0:break
   self.inp.write(f'{f} {s} {a} {b}\n');self.t.append((f,s,a,b));self.read()
  return self.state
 def close(self):
  self.p.kill();self.p.wait();self.inp.close();self.out.close()
 def save(self,path):
  open(path,'wb').write(bytes([109,3,1,self.m,0,0,0,0,0,1,0,0,0])+b''.join(struct.pack('bbBB',f,s,a%256,b) for f,s,a,b in self.t)+b'\x80')
 def draw(self):self.wad.draw(f'work/trace{self.m}.png',self.trace,False)
 def replay(self,t):
  for f,s,a,b in t:self.step(f,s,a,b)
 def goto(self,x,y,rad=20,maxn=350,fire=False,use=True,face=None,speed=22):
  start=len(self.t);stuck=0
  for k in range(maxn):
   st=self.state;px,py=st['x'],st['y'];dx,dy=x-px,y-py;dist=math.hypot(dx,dy)
   if dist<rad or st['state']!=0:break
   if st['health']<=0:break
   desired=math.atan2(dy,dx)+math.pi/4 if face is None else math.radians(face)
   if fire:
    enemies=[o for o in st['monsters'] if o[5]&4 and o[4]>0 and o[0]!=30 and math.hypot(o[1]-px,o[2]-py)<280 and ((o[1]-px)*dx+(o[2]-py)*dy)>0]
    if enemies:
     o=min(enemies,key=lambda o:math.hypot(o[1]-px,o[2]-py));desired=math.atan2(o[2]-py,o[1]-px)
   turn=round(((desired-st['angle']/2**32*math.tau+math.pi)%math.tau-math.pi)/math.tau*256)
   turn=max(-46,min(46,turn)) if len(self.t)%7==0 else 0
   ang=st['angle']/2**32*math.tau+turn/256*math.tau
   v=min(speed,dist*.3);ax=dx/dist*v-st['vx'];ay=dy/dist*v-st['vy']
   f=max(-50,min(50,round(32*(ax*math.cos(ang)+ay*math.sin(ang)))))
   s=max(-50,min(50,round(32*(ax*math.sin(ang)-ay*math.cos(ang)))))
   b=(1 if fire else 0)|(2 if use and len(self.t)%70==0 else 0)
   self.step(f,s,turn,b)
   if math.hypot(self.state['x']-px,self.state['y']-py)<.1:stuck+=1
   else:stuck=0
   if stuck>75:break
  dist=math.hypot(x-self.state['x'],y-self.state['y'])
  print('goto',x,y,'tic',len(self.t),'pos',tuple(round(self.state[v],1) for v in ['x','y']),'dist',round(dist),'hp',self.state['health'],'sector',self.state['sector'],flush=True)
  return dist<rad or self.state['state']!=0
 def face(self,deg,fire=False,use=False,n=10):
  for k in range(n):
   a=round(((math.radians(deg)-self.state['angle']/2**32*math.tau+math.pi)%math.tau-math.pi)/math.tau*256)
   a=max(-46,min(46,a)) if len(self.t)%7==0 else 0
   ang=self.state['angle']/2**32*math.tau+a/256*math.tau
   ax=-self.state['vx'];ay=-self.state['vy']
   f=max(-50,min(50,round(32*(ax*math.cos(ang)+ay*math.sin(ang)))))
   s=max(-50,min(50,round(32*(ax*math.sin(ang)-ay*math.cos(ang)))))
   self.step(f=f,s=s,a=a,b=(1 if fire else 0)|(2 if use and len(self.t)%70==0 else 0))
 def report(self):print({k:v for k,v in self.state.items() if k not in ['sectors','monsters']})
if __name__=='__main__':
 r=Sim(1);r.report();r.step(f=50,n=70);r.report();r.close()
