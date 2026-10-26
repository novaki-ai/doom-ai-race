"""Promote only immutable snapshots which pass the official checker and improve time."""
import os,json,hashlib,datetime
os.sched_setaffinity(0,{4,5,6,7})
from check import check
candidates={1:['angleprune1'],2:['angleprune2','fineend2','shotend2'],3:['angleprune3','splice3'],4:['angleprune4','closejump4','tunejump4','tunejumpb4'],5:['angleprune5','starfastend5','splice5'],6:['angleprune6','nosoulpink6','rushnosoul6'],7:['angleprune7','directhealth7'],8:['angleprune8','skipmed8']}
results=[]
for m,names in candidates.items():
 target=f'submit/E1M{m}.lmp';best=check(target)
 assert best['pass'],best
 for name in names:
  src=f'work/{name}.lmp'
  if not os.path.exists(src):continue
  data=open(src,'rb').read();snap=f'work/promote-E1M{m}.lmp';open(snap,'wb').write(data)
  r=check(snap)
  if r['pass'] and r['map']==f'E1M{m}' and r['seconds']<best['seconds']:
   open(target,'wb').write(data);best=check(target);assert best['pass'];print('PROMOTED',name,best['time'],flush=True)
 best=check(target);best['sha256']=hashlib.sha256(open(target,'rb').read()).hexdigest();results.append(best)
report={'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'valid_maps':sum(r['pass'] for r in results),'total_seconds':round(sum(r['seconds'] for r in results),2),'results':results}
json.dump(report,open('RESULTS.json','w'),indent=2)
for r in results:print('PASS',r['map'],r['time'],flush=True)
print('TOTAL',report['total_seconds'],flush=True)
