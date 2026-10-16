"""Seeded synthetic benchmark. Requires numpy. No patient data or clinical claims."""
from pathlib import Path
import json, math, numpy as np

ROOT=Path(__file__).parent
OUT=ROOT/'dist'/'data'
OUT.mkdir(parents=True,exist_ok=True)
NAMES=['current','mean30','trend30','variability60','fasting','a1c','sleep','activity','clockSin','clockCos','mealNow','meal30','meal60','meal90','meal120','age']
HORIZONS=[30,60,90,120]

def kernel(minutes):
    return (minutes/48)*math.exp(1-minutes/48) if 0<=minutes<=360 else 0

def make_person(pid):
    r=np.random.default_rng(4100+pid)
    fasting=float(r.uniform(102,157)); a1c=float(r.uniform(6.3,9.2)); sleep=float(r.uniform(4.5,8.5))
    age=int(r.integers(28,74)); activity=float(r.uniform(0,0.9)); gain=float(0.65+(a1c-6)*0.24+r.uniform(-.08,.08))
    profile=dict(id=f'SYN-{pid:03}',name=f'Synthetic person {pid:03}',age=age,fasting=round(fasting,1),a1c=round(a1c,1),sleep=round(sleep,1),activity=round(activity,2),condition='Type 2 diabetes · synthetic')
    meals=[]
    for day in range(4):
        for minute in [480,780,1200]:
            meals.append(dict(minute=int(day*1440+minute+r.integers(-35,36)),carbs=int(r.uniform(35,100)),label=['Breakfast','Lunch','Dinner'][[480,780,1200].index(minute)]))
    rows=[]; drift=0
    for t in range(4*288):
        minute=t*5
        drift=drift*.93+float(r.normal(0,1.1))
        meal=sum(m['carbs']*gain*kernel(minute-m['minute']) for m in meals)
        circ=5*math.sin(minute/1440*2*math.pi)+3*math.cos(minute/720*2*math.pi)
        glucose=fasting+meal+circ+(7-sleep)*2-activity*6+drift+float(r.normal(0,2))
        rows.append(dict(minute=minute,glucose=round(glucose,2)))
    return dict(profile=profile,readings=rows,meals=meals)

def features(p,i):
    rows=p['readings']; profile=p['profile']; t=rows[i]['minute']; history=[v['glucose'] for v in rows[i-12:i+1]]
    logged=[m for m in p['meals'] if m['minute']<=t]
    meal=[sum(m['carbs']*kernel(t+h-m['minute']) for m in logged) for h in [0,30,60,90,120]]
    return [history[-1],np.mean(history[-7:]),history[-1]-history[-7],np.std(history),profile['fasting'],profile['a1c'],profile['sleep'],profile['activity'],math.sin(t/1440*2*math.pi),math.cos(t/1440*2*math.pi),*meal,profile['age']]

def dataset(ids):
    x=[]; y=[]; now=[]; who=[]
    for pid in ids:
        p=make_person(pid)
        for i in range(24,len(p['readings'])-24,6):
            x.append(features(p,i)); y.append([p['readings'][i+h//5]['glucose'] for h in HORIZONS]); now.append(p['readings'][i]['glucose']);who.append(pid)
    return np.array(x),np.array(y),np.array(now),np.array(who)

def train():
    x,y,_,_=dataset(range(1,101)); cx,cy,_,_=dataset(range(101,126));tx,ty,tn,tw=dataset(range(126,151))
    mean=x.mean(axis=0);std=x.std(axis=0);std[std<1e-8]=1
    transform=lambda z:np.column_stack([np.ones(len(z)),(z-mean)/std])
    a=transform(x);pen=np.eye(a.shape[1])*8;pen[0,0]=0
    weights=np.linalg.solve(a.T@a+pen,a.T@y)
    cp=transform(cx)@weights;pred=transform(tx)@weights
    quantiles=[float(np.sort(np.abs(cy[:,j]-cp[:,j]))[min(len(cy)-1,math.ceil((len(cy)+1)*.9)-1)]) for j in range(4)]
    metrics=[]
    for j,h in enumerate(HORIZONS):
        err=pred[:,j]-ty[:,j];b=tn-ty[:,j]
        per_person=[np.mean(np.abs(err[tw==pid])) for pid in range(126,151)]
        metrics.append(dict(horizon=h,mae=round(float(np.mean(np.abs(err))),2),rmse=round(float(np.sqrt(np.mean(err**2))),2),persistenceMAE=round(float(np.mean(np.abs(b))),2),coverage=round(float(np.mean(np.abs(err)<=quantiles[j]))*100,1),halfWidth=round(quantiles[j],2),patientMAEmin=round(float(min(per_person)),2),patientMAEmax=round(float(max(per_person)),2)))
    model=dict(version='glyra-ridge-synthetic-v1',featureNames=NAMES,horizons=HORIZONS,mean=mean.tolist(),std=std.tolist(),weights=weights.tolist(),quantiles=quantiles,source='Synthetic generator train.py; not a validated physiological simulator')
    report=dict(seed='4100 + person id',population=150,trainPeople=list(range(1,101)),calibrationPeople=list(range(101,126)),testPeople=list(range(126,151)),trainWindows=len(y),calibrationWindows=len(cy),testWindows=len(ty),metrics=metrics,limits=['All results are synthetic-only.','Intervals are pointwise marginal calibration over synthetic windows; within-person dependence limits interpretation.','No guaranteed coverage for real patients, entire trajectories or edited scenarios.','Unannounced future meals remain unpredictable.','No medication or insulin recommendation.'])
    (OUT/'model.json').write_text(json.dumps(model,indent=2))
    (OUT/'benchmark.json').write_text(json.dumps(report,indent=2))
    fixtures=[]
    for n,pid in enumerate([126,133,141]):
        p=make_person(pid);p['profile']['name']=['Ananya · demo','Ravi · demo','Meera · demo'][n];p['cursor']=384+[0,20,44][n];fixtures.append(p)
    (OUT/'fixtures.json').write_text(json.dumps(fixtures))
    case=fixtures[0];i=case['cursor'];f=features(case,i);expected=np.r_[1,(np.array(f)-mean)/std]@weights
    (OUT/'parity.json').write_text(json.dumps(dict(features=f,expected=expected.tolist(),id=case['profile']['id'],cursor=i)))
    print(json.dumps(dict(metrics=metrics,windows=[len(y),len(cy),len(ty)]),indent=2))

if __name__=='__main__':train()
