const $=(id)=>document.getElementById(id);
const nf=(n)=>new Intl.NumberFormat('ru-RU',{maximumFractionDigits:2}).format(n||0);
let example=null;
async function request(path, options={}){
 const response=await fetch(path,{headers:{'Content-Type':'application/json'},...options});
 const data=await response.json().catch(()=>({}));
 if(!response.ok)throw new Error(typeof data.detail==='string'?data.detail:JSON.stringify(data.detail||data));
 return data;
}
async function loadDemo(){
 example=example||await request('/static/demo.json');
 $('name').value=example.name;$('level').value=example.level;
 $('editor').value=JSON.stringify(example.data,null,2);
}
function message(text,err=false){$('message').textContent=text;$('message').className=err?'error':'';}
function showRun(run){
 const r=run.result, k=r.kpis;
 $('coverage').textContent=nf(k.demand_coverage_pct)+'%';
 $('produced').textContent=nf(k.produced_tons);
 $('shortage').textContent=nf(k.shortage_tons);
 $('loss').textContent=nf(k.changeover_loss_tons);
 $('runLabel').textContent=`${run.id.slice(0,8)} · ${r.level} · ${r.engine} · НЕ оптимизировано`;
 $('resultRows').replaceChildren();
 for(const b of r.buckets){
  const tr=document.createElement('tr');
  const values=[b.bucket,Object.values(b.production_tons).reduce((a,v)=>a+v,0),Object.values(b.shortage_tons).reduce((a,v)=>a+v,0),b.unused_capacity_tons,b.changeover_loss_tons];
  for(let i=0;i<values.length;i++){const td=document.createElement('td');td.textContent=i===0?values[i]:nf(values[i]);tr.appendChild(td);}
  $('resultRows').appendChild(tr);
 }
 document.getElementById('results').scrollIntoView({behavior:'smooth',block:'start'});
}
async function refresh(){
 try{
  const items=await request('/api/scenarios');
  $('history').replaceChildren();
  if(!items.length){$('history').textContent='Сценариев пока нет. Начните с демонстрационного примера.';return;}
  for(const item of items){
   const el=document.createElement('button');el.className='history-item';
   const left=document.createElement('span');const bold=document.createElement('b');bold.textContent=item.name;
   const info=document.createElement('small');info.textContent=new Date(item.created_at).toLocaleString('ru-RU');
   left.append(bold,info);const tag=document.createElement('span');tag.className='pill';tag.textContent=item.level;
   el.append(left,tag);
   el.addEventListener('click',async()=>{
    try{const runs=await request(`/api/scenarios/${item.id}/runs`);if(runs.length)showRun(runs[0]);else message('У этого сценария ещё нет расчётов.');}
    catch(e){message(e.message,true);}
   });
   $('history').appendChild(el);
  }
 }catch(e){$('history').textContent='Ошибка подключения: '+e.message;}
}
$('demo').addEventListener('click',()=>loadDemo().catch(e=>message(e.message,true)));
$('refresh').addEventListener('click',refresh);
$('calculate').addEventListener('click',async()=>{
 const button=$('calculate');button.disabled=true;message('Сохраняю сценарий и выполняю базовый расчёт…');
 try{
  const data=JSON.parse($('editor').value);
  const scenario=await request('/api/scenarios',{method:'POST',body:JSON.stringify({name:$('name').value,level:$('level').value,data})});
  const run=await request(`/api/scenarios/${scenario.id}/runs`,{method:'POST'});
  message('Сценарий сохранён. Демо-расчёт завершён.');showRun(run);await refresh();
 }catch(e){message(e.message,true);}finally{button.disabled=false;}
});
loadDemo().then(refresh).catch(e=>message('Не удалось загрузить данные: '+e.message,true));
