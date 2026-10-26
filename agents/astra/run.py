import struct,subprocess,os,math,json
ROOT=os.path.dirname(os.path.abspath(__file__))
class Run:
 def __init__(self,m,name='try'):
  self.m=m;self.name=name;self.t=[];self.frames=[];self.pos=next((x,y,ang*2**32/360) for x,y,ang,k,f in __import__('wad').Wad(m).th if k==1)
 def save(self,path):
  open(path,'wb').write(bytes([109,3,1,self.m,0,0,0,0,0,1,0,0,0])+b''.join(struct.pack('bbBB',f,s,a%256,b) for f,s,a,b in self.t)+b'\x80')
 def replay(self):
  self.save(f'work/{self.name}.lmp')
  p=subprocess.run(['dsda-doom','-iwad',ROOT+'/game/DOOM1.WAD','-complevel','2','-fastdemo',self.name+'.lmp','-export_ghost',self.name,'-levelstat','-analysis','-nodraw','-nosound','-nomusic','-data',ROOT+'/work'],cwd=ROOT+'/work',capture_output=True)
  b=open(f'work/{self.name}.gst','rb').read();self.frames=[struct.unpack_from('<iiiIiiiii',b,i) for i in range(8,len(b)-35,36)];q=self.frames[-1];self.pos=(q[0]/65536,q[1]/65536,q[3]);return self.pos
 def step(self,n=1,f=0,s=0,a=0,b=0):
  self.t += [(f,s,a,b)]*n;return self.replay()
 def goto(self,x,y,rad=28,maxn=400,fire=False,use=True):
  start=len(self.t);stuck=0;last=None
  while len(self.t)-start<maxn:
   px,py,ang=self.pos;dist=math.hypot(x-px,y-py)
   if dist<rad:break
   desired=math.atan2(y-py,x-px)+math.pi/4
   turn=round(((desired-ang/2**32*math.tau+math.pi)%math.tau-math.pi)/math.tau*256)
   turn=max(-46,min(46,turn))
   # one correction per 7 tics; at most five direction reversals/sec
   n=7 if dist>80 else 3
   if len(self.t)%7: turn=0
   for j in range(n):
    tic=len(self.t);self.t.append((50,50,turn if j==0 else 0,(1 if fire else 0)|(2 if use and tic%7==0 else 0)))
   self.replay()
   if last and math.hypot(self.pos[0]-last[0],self.pos[1]-last[1])<1:stuck+=n
   else:stuck=0
   last=self.pos
   if stuck>70:break
  print('goto',x,y,'tic',len(self.t),'pos',tuple(round(v,2) for v in self.pos[:2]),'dist',round(math.hypot(x-self.pos[0],y-self.pos[1]),1),flush=True)
  return math.hypot(x-self.pos[0],y-self.pos[1])<rad
 def draw(self): __import__('wad').Wad(self.m).draw(f'work/trace{self.m}.png',[(f[0]/65536,f[1]/65536) for f in self.frames],False)
if __name__=='__main__':
 r=Run(1)
 for p in [(1250,-3000),(1290,-2530),(1480,-2490),(1660,-2490),(2240,-2660),(2400,-2650),(2800,-2800),(2930,-2940),(2930,-3550),(3000,-3800),(3000,-4110),(3000,-4580),(3000,-4750)]:
  if not r.goto(*p):break
 r.draw()
