from sim import Sim
from lmp import oku
r=Sim(5);r.replay([(f,s,a//256,b) for f,s,a,b in oku('work/route5.lmp')[1]][:288]);r.smartturn=True;r.auto_doors=True;r.avoid=True;r.weapon_policy=True
pts=[(368,352),(280,424),(416,504),(464,504),(960,472),(1128,300),(1128,200),(1296,96),(1296,48),(1088,40),(1024,0),(600,-32),(512,-32),(200,-32),(200,100),(552,160),(848,200),(900,220),(900,300),(900,220),(552,160),(200,100),(120,200),(200,420),(200,600),(360,528),(416,520),(704,640),(912,712),(1048,776),(1048,832),(968,880),(856,880),(688,800),(688,848)]
for p in pts:
 if not r.goto(*p,fire=True,rad=16):break
r.save('work/yellow5.lmp');r.draw();r.report();r.close()
