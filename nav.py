import struct,math,heapq
from PIL import Image,ImageDraw
from wad import Wad
class Nav:
 def __init__(self,w,step=16,radius=18):
  self.w=w;self.step=step;self.radius=radius
  self.nodes=list(struct.iter_unpack('<hhhhhhhhhhhhHH',w.data['NODES']))
  self.ss=list(struct.iter_unpack('<HH',w.data['SSECTORS']));self.segs=list(struct.iter_unpack('<HHHHHH',w.data['SEGS']))
  self.sssec=[w.s[w.l[self.segs[start][3]][5+self.segs[start][4]]][-1] for count,start in self.ss]
  xs,ys=zip(*w.v);self.ox=min(xs)-64;self.oy=min(ys)-64;self.nx=(max(xs)-self.ox+64)//step+1;self.ny=(max(ys)-self.oy+64)//step+1
  self.mask=Image.new('L',(self.nx,self.ny));d=ImageDraw.Draw(self.mask)
  for a,b,fl,sp,tag,r,l in w.l:
   if l==65535 or fl&1:
    p=self.grid(w.v[a]);q=self.grid(w.v[b]);width=math.ceil(radius*2/step)
    d.line([p,q],fill=255,width=width)
    for x,y in (p,q):d.ellipse((x-radius/step,y-radius/step,x+radius/step,y+radius/step),fill=255)
  self.pix=self.mask.load();self.sectorcache={}
 def grid(self,p):return ((p[0]-self.ox)/self.step,(p[1]-self.oy)/self.step)
 def world(self,p):return (p[0]*self.step+self.ox,p[1]*self.step+self.oy)
 def sector(self,x,y):
  n=len(self.nodes)-1
  while not n&32768:
   v=self.nodes[n];side=int((y-v[1])*v[2]>=(x-v[0])*v[3]);n=v[12+side]
  return self.sssec[n&32767]
 def sec(self,p):
  if p not in self.sectorcache:self.sectorcache[p]=self.sector(*self.world(p))
  return self.sectorcache[p]
 def path(self,start,end,sectors=None,allow_lifts=True):
  if sectors is None:sectors=[s[:2] for s in self.w.sec]
  def nearest(p):
   a,b=map(round,self.grid(p));cand=[(x,y) for x in range(a-4,a+5) for y in range(b-4,b+5) if 0<=x<self.nx and 0<=y<self.ny and not self.pix[x,y]]
   return min(cand,key=lambda q:math.dist(self.world(q),p))
  start=nearest(start);goal=nearest(end)
  # sectors of closed doors have a floor but their ceiling will open on use.
  doors=set()
  lifts=set()
  for a,b,fl,sp,tag,r,l in self.w.l:
   if l!=65535 and sp in [1,26,27,28,31,32,33,34,117,118]:doors.add(self.w.s[l][-1])
   if tag and sp in [62,88,10,21,53,87]:lifts|={i for i,s in enumerate(self.w.sec) if s[-1]==tag}
  def height(p):
   sec=self.sec(p);f,c=sectors[sec];return (f,c,sec)
  q=[(0,0,start)];cost={start:0};prev={};dirs=[(a,b) for a in [-1,0,1] for b in [-1,0,1] if a or b]
  while q:
   _,g,p=heapq.heappop(q)
   if cost[p]!=g:continue
   if p==goal:break
   pf,pc,ps=height(p)
   for dx,dy in dirs:
    t=(p[0]+dx,p[1]+dy)
    if not(0<=t[0]<self.nx and 0<=t[1]<self.ny) or self.pix[t]:continue
    if dx and dy and (self.pix[p[0]+dx,p[1]] or self.pix[p[0],p[1]+dy]):continue
    f,c,sec=height(t)
    if sec not in doors and c-f<56:continue
    if f-pf>24 and not(allow_lifts and (sec in lifts or ps in lifts)):continue
    ng=g+math.hypot(dx,dy)+(3 if sec in lifts and f-pf>24 else 0)
    if ng<cost.get(t,1e9):cost[t]=ng;prev[t]=p;heapq.heappush(q,(ng+math.dist(t,goal),ng,t))
  if goal not in cost:raise RuntimeError('no path')
  path=[goal]
  while path[-1]!=start:path.append(prev[path[-1]])
  path=path[::-1]
  # simplify only when the straight line stays in free grid and respects rising floors
  def clear(a,b):
   n=max(abs(b[0]-a[0]),abs(b[1]-a[1]))*2;last=a
   for k in range(1,n+1):
    t=(round(a[0]+(b[0]-a[0])*k/n),round(a[1]+(b[1]-a[1])*k/n))
    if self.pix[t]:return False
    f,c,sec=height(t);pf,pc,ps=height(last)
    if sec not in doors and c-f<56:return False
    if f-pf>24 and not(allow_lifts and(sec in lifts or ps in lifts)):return False
    last=t
   return True
  simple=[path[0]];i=0
  while i<len(path)-1:
   j=i+1
   while j+1<len(path) and clear(path[i],path[j+1]):j+=1
   simple.append(path[j]);i=j
  return [self.world(p) for p in simple]
if __name__=='__main__':
 import sys
 m=int(sys.argv[1]);w=Wad(m);nav=Nav(w);start=next((x,y) for x,y,a,t,f in w.th if t==1);end=tuple(map(int,sys.argv[2:4]));p=nav.path(start,end);print(p);w.draw(f'work/nav{m}.png',p)
