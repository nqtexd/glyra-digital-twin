export function kernel(m){return m>=0&&m<=360?(m/48)*Math.exp(1-m/48):0;}
export function features(person,cursor){
 const {profile:p,readings,meals}=person;const t=readings[cursor].minute;const hist=readings.slice(cursor-12,cursor+1).map(r=>r.glucose);const mean=a=>a.reduce((s,v)=>s+v,0)/a.length;
 const av=mean(hist);const logged=meals.filter(m=>m.minute<=t);
 return [hist.at(-1),mean(hist.slice(-7)),hist.at(-1)-hist.at(-7),Math.sqrt(mean(hist.map(v=>(v-av)**2))),p.fasting,p.a1c,p.sleep,p.activity,Math.sin(t/1440*2*Math.PI),Math.cos(t/1440*2*Math.PI),...[0,30,60,90,120].map(h=>logged.reduce((s,m)=>s+m.carbs*kernel(t+h-m.minute),0)),p.age];
}
export function predict(model,f){const z=[1,...f.map((v,i)=>(v-model.mean[i])/model.std[i])];return model.horizons.map((h,j)=>({horizon:h,value:z.reduce((s,v,i)=>s+v*model.weights[i][j],0),halfWidth:model.quantiles[j]}));}
export function quality(person,cursor,now=person.readings[cursor]?.minute){
 const rows=person.readings.slice(Math.max(0,cursor-12),cursor+1);const reasons=[];
 if(rows.length<13)reasons.push('At least 13 readings over 60 minutes are required.');
 if(rows.some(r=>!Number.isFinite(r.glucose)||r.glucose<40||r.glucose>400||!Number.isFinite(r.minute)))reasons.push('A reading is outside this model’s supported range.');
 if(rows.some((r,i)=>i>0&&(r.minute<=rows[i-1].minute||r.minute-rows[i-1].minute>7)))reasons.push('Readings must be ordered and spaced about five minutes apart.');
 if(!Number.isFinite(now)||now-rows.at(-1)?.minute>10||now<rows.at(-1)?.minute)reasons.push('The latest reading is stale or dated in the future.');
 const p=person.profile;
 if(![p.fasting,p.a1c,p.sleep,p.activity,p.age].every(Number.isFinite)||p.fasting<95||p.fasting>170||p.a1c<6||p.a1c>10||p.sleep<4||p.sleep>9||p.activity<0||p.activity>1||p.age<25||p.age>80)reasons.push('Health record falls outside the synthetic model’s supported range.');
 return {ok:reasons.length===0,reasons,count:rows.length,age:Number.isFinite(now)?now-rows.at(-1)?.minute:null};
}
export function forecast(model,person,cursor,now){const q=quality(person,cursor,now);return {quality:q,points:q.ok?predict(model,features(person,cursor)):[]};}
export function parseCSV(text){
 const lines=text.trim().split(/\r?\n/);if(lines[0].trim()!=='minute,glucose')throw new Error('Use the exact header minute,glucose.');
 if(lines.length>5001)throw new Error('Limit imports to 5,000 rows.');
 const rows=lines.slice(1).map((line,i)=>{const parts=line.split(',');if(parts.length!==2||parts.some(p=>p.trim()===''))throw new Error(`Row ${i+2} needs two numbers.`);const [minute,glucose]=parts.map(Number);if(!Number.isFinite(minute)||!Number.isFinite(glucose)||minute<0||glucose<40||glucose>400)throw new Error(`Row ${i+2} is out of range.`);return {minute,glucose};});
 if(rows.length<13)throw new Error('Import at least 13 readings.');
 if(rows.some((r,i)=>i>0&&(r.minute<=rows[i-1].minute||Math.abs(r.minute-rows[i-1].minute-5)>.01)))throw new Error('Use increasing five-minute intervals, with no duplicates or gaps.');
 return rows;
}
