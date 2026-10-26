import struct,math,json
from PIL import Image,ImageDraw,ImageFont
class Wad:
 def __init__(self,m):
  b=open('game/DOOM1.WAD','rb').read(); n,o=struct.unpack_from('<ii',b,4); lumps=[struct.unpack_from('<ii8s',b,o+i*16) for i in range(n)]; k=next(i for i,l in enumerate(lumps) if l[2].rstrip(b'\0')==f'E1M{m}'.encode()); self.data={name.rstrip(b'\0').decode():b[p:p+s] for p,s,name in lumps[k+1:k+11]}
  def unpack(name,fmt): return list(struct.iter_unpack('<'+fmt,self.data[name]))
  self.v=unpack('VERTEXES','hh');self.l=unpack('LINEDEFS','HHHHHHH');self.s=unpack('SIDEDEFS','hh8s8s8sH');self.sec=unpack('SECTORS','hh8s8shhh');self.th=unpack('THINGS','hhhhh');self.m=m
 def draw(self,path=None,route=None,labels=True):
  xs,ys=zip(*self.v); scale=min(1800/(max(xs)-min(xs)),1600/(max(ys)-min(ys))); margin=50
  def xy(p):return (margin+(p[0]-min(xs))*scale,margin+(max(ys)-p[1])*scale)
  im=Image.new('RGB',(int((max(xs)-min(xs))*scale+100),int((max(ys)-min(ys))*scale+100)),(20,22,27));d=ImageDraw.Draw(im)
  for i,(a,b,fl,sp,tag,r,l) in enumerate(self.l):
   col=(180,180,190) if l==65535 else (58,62,70)
   if sp: col=(255,160,40)
   d.line([xy(self.v[a]),xy(self.v[b])],fill=col,width=2 if l==65535 or sp else 1)
   if sp and labels:
    p=tuple((x+y)/2 for x,y in zip(self.v[a],self.v[b]));d.text(xy(p),f'{i}:{sp}/{tag}',fill=(255,200,70))
  colors={1:'white',5:'blue',6:'yellow',13:'red',2001:'cyan',2002:'cyan',2003:'cyan',2004:'cyan',2018:'green',2019:'green',2022:'magenta',2023:'magenta'}
  for x,y,a,t,f in self.th:
   if not(f&4) and t!=1:continue
   p=xy((x,y)); col=colors.get(t,'#c05050' if t in [3001,3002,3003,3004,9,58] else '#666677');r=4 if t in colors else 2
   d.ellipse((p[0]-r,p[1]-r,p[0]+r,p[1]+r),fill=col)
   if t in colors: d.text((p[0]+4,p[1]),f'{t} ({x},{y})',fill=col)
  if route:
   ps=[xy(p) for p in route];d.line(ps,fill='#00ff88',width=2)
   for i,p in enumerate(ps): d.text(p,str(i),fill='white')
  # coordinate grid
  for x in range(math.ceil(min(xs)/256)*256,max(xs)+1,256):
   p=xy((x,max(ys)));d.text((p[0],20),str(x),fill='#aaaaaa')
  for y in range(math.ceil(min(ys)/256)*256,max(ys)+1,256):
   p=xy((min(xs),y));d.text((0,p[1]),str(y),fill='#aaaaaa')
  im.save(path or f'work/map{self.m}.png')
 def info(self):
  print('Things',[(x,y,a,t) for x,y,a,t,f in self.th if t in [1,5,6,13,2001,2002,2003,2022,2023]])
  for i,(a,b,fl,sp,tag,r,l) in enumerate(self.l):
   if sp:print(i,self.v[a],self.v[b],'special',sp,'tag',tag,'sectors',self.s[r][-1],self.s[l][-1] if l!=65535 else None)
if __name__=='__main__':
 import sys
 w=Wad(int(sys.argv[1]));w.draw();w.info()
