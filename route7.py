from sim import Sim
r=Sim(7);r.smartturn=True;r.auto_doors=True;r.weapon_policy=True;r.avoid=True
for p in [(192,400),(192,320),(192,0),(-64,192),(32,-96),(376,-128),(840,-184),(1376,-672),(1416,-672),(1440,-640),(1408,-392),(1328,-352),(1264,-352),(1248,-320),(1248,-248),(1344,-192),(1232,-144)]:
 if not r.goto(*p,fire=True,rad=14,maxn=450,stucklimit=350):break
r.save('work/route7.lmp');r.draw();r.report();r.close()
