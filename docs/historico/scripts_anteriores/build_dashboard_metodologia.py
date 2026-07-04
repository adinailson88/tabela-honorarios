# -*- coding: utf-8 -*-
"""Gera dashboard_senge_honorarios_metodologia_servicos.html a partir do JSON da pipeline."""
import json
from pathlib import Path
BASE = Path(__file__).resolve().parent
data = json.loads((BASE / "dados_metodologia_servicos.json").read_text(encoding="utf-8"))
DATA_JSON = json.dumps(data, ensure_ascii=False, separators=(",", ":"))

HTML = r"""<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SENGE/BA — Honorários por Serviço e Classe de Confiabilidade</title>
<style>
:root{--bg:#0f1720;--card:#16212e;--mut:#8aa0b4;--fg:#e8eef5;--ac:#2f81f7;--a:#1f9d55;--b:#b58900;--c:#c9521a;--d:#9aa3ad;--line:#26323f}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.5 system-ui,Segoe UI,Roboto,Arial}
header{padding:16px 20px;border-bottom:1px solid var(--line);background:#0b121a}
h1{font-size:18px;margin:0 0 2px}h2{font-size:15px;margin:18px 0 8px}.sub{color:var(--mut);font-size:12px}
.wrap{padding:16px 20px;max-width:1280px;margin:0 auto}
.filters{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:10px;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px}
.filters label{display:block;font-size:11px;color:var(--mut);margin-bottom:4px;text-transform:uppercase;letter-spacing:.04em}
select,input{width:100%;background:#0d1722;color:var(--fg);border:1px solid var(--line);border-radius:7px;padding:6px}
select[multiple]{height:120px}
.bar{display:flex;gap:8px;align-items:center;margin:10px 0;flex-wrap:wrap}
button{background:var(--ac);color:#fff;border:0;border-radius:7px;padding:8px 12px;cursor:pointer;font-weight:600}
button.ghost{background:#22303f}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-top:12px}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px}
.kpi .n{font-size:22px;font-weight:700}.kpi .l{color:var(--mut);font-size:12px}
.kpi.warn{border-color:var(--c)}
.classbar{display:flex;height:26px;border-radius:7px;overflow:hidden;border:1px solid var(--line);margin-top:6px}
.classbar span{display:flex;align-items:center;justify-content:center;font-size:11px;color:#04121a;font-weight:700}
.legend{display:flex;gap:14px;flex-wrap:wrap;margin-top:6px;font-size:12px;color:var(--mut)}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:5px;vertical-align:middle}
table{width:100%;border-collapse:collapse;margin-top:8px;font-size:13px}
th,td{padding:7px 8px;border-bottom:1px solid var(--line);text-align:left}
th{color:var(--mut);font-weight:600;position:sticky;top:0;background:var(--card)}
td.num{text-align:right;font-variant-numeric:tabular-nums}
.tag{font-size:10px;padding:2px 6px;border-radius:20px;border:1px solid var(--line);color:var(--mut)}
.tag.new{color:#ffd479;border-color:#5a4a16;background:#241d06}
.tag.low{color:#ff9a76;border-color:#5a2a16;background:#240e06}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px;margin-top:14px}
.warnbox{background:#2a160c;border:1px solid var(--c);color:#ffcaa8;border-radius:10px;padding:12px;margin-top:12px;display:none}
.tablewrap{max-height:520px;overflow:auto;border:1px solid var(--line);border-radius:10px}
.muted{color:var(--mut)}.small{font-size:12px}
details summary{cursor:pointer;font-weight:600}
code{background:#0d1722;padding:1px 5px;border-radius:4px}
</style></head>
<body>
<header>
<h1>SENGE/BA — Painel de Honorários por Serviço e Classe de Confiabilidade</h1>
<div class="sub">Evidência auxiliar, indireta e agregada de ARTs (base 2022). Caráter <b>orientativo</b> — não é preço obrigatório nem tabela vinculante. <span id="meta"></span></div>
</header>
<div class="wrap">

<div class="filters">
  <div><label>Classe de confiabilidade</label><select id="fClasse" multiple><option value="A">A — base de cálculo</option><option value="B">B — secundária</option><option value="C">C — só diagnóstico</option><option value="D">D — excluída</option></select></div>
  <div><label>Grupo de serviço</label><select id="fGrupo" multiple></select></div>
  <div><label>Serviço padronizado</label><select id="fServico" multiple></select></div>
  <div><label>Município (filtro)</label><input id="munSearch" placeholder="filtrar lista..."><select id="fMun" multiple></select></div>
  <div><label>Ano</label><select id="fAno" multiple></select></div>
</div>
<div class="bar">
  <button onclick="clearF()" class="ghost">Limpar filtros</button>
  <span id="activeF" class="small muted"></span>
</div>

<div class="kpis">
  <div class="kpi"><div class="n" id="kArts">—</div><div class="l">ARTs (filtradas)</div></div>
  <div class="kpi"><div class="n" id="kAtiv">—</div><div class="l">Atividades distintas (por ART)</div></div>
  <div class="kpi"><div class="n" id="kServ">—</div><div class="l">Serviços distintos</div></div>
  <div class="kpi"><div class="n" id="kBaseCalc">—</div><div class="l">Base de cálculo (Classe A)</div></div>
  <div class="kpi" id="kpiMed"><div class="n" id="kMed">—</div><div class="l">Mediana do valor (Classe A) — R$</div></div>
  <div class="kpi" id="kpiIqr"><div class="n" id="kIqr">—</div><div class="l">IQR (Q1–Q3) — Classe A</div></div>
</div>

<div class="warnbox" id="warnMon">Os filtros selecionados não incluem a <b>Classe A</b>. Valores monetários (mediana/IQR/tabela) ficam <b>indisponíveis</b>: apenas a Classe A fundamenta cálculo de honorário. As classes B, C e D servem para frequência, demanda e diagnóstico.</div>

<div class="card">
  <h2 style="margin-top:0">Distribuição por classe de confiabilidade (base total)</h2>
  <div class="classbar" id="classbar"></div>
  <div class="legend">
    <span><i class="dot" style="background:var(--a)"></i>A — uma ART/atividade, valor associável (base de cálculo)</span>
    <span><i class="dot" style="background:var(--b)"></i>B — composto homogêneo (secundária)</span>
    <span><i class="dot" style="background:var(--c)"></i>C — composto ambíguo (só diagnóstico)</span>
    <span><i class="dot" style="background:var(--d)"></i>D — inválido/sem valor (excluída)</span>
  </div>
  <div class="small muted" style="margin-top:8px">FATO: o valor da ART é replicado nas linhas (não somar). Só a Classe A entra no cálculo monetário. Mediana e IQR (nunca média simples).</div>
</div>

<div class="card">
  <h2 style="margin-top:0">Serviços — referência observada (Classe A)</h2>
  <div class="small muted">Faixas observadas (mediana, Q1, Q3, IQR) por serviço, sobre a base de cálculo filtrada. <span class="tag low">n&lt;5</span> = sem base estatística (Informação insuficiente para verificar). <span class="tag new">novo</span> = serviço/lacuna não previsto na tabela atual.</div>
  <div class="tablewrap"><table id="svcTable"><thead><tr>
    <th>Serviço</th><th>Grupo</th><th class="num">n (ARTs A)</th><th class="num">Mediana R$</th><th class="num">Q1</th><th class="num">Q3</th><th class="num">IQR</th><th></th>
  </tr></thead><tbody></tbody></table></div>
</div>

<div class="card">
  <details open><summary>Metodologia (resumo)</summary>
  <div class="small" style="margin-top:8px">
  <p><b>Objetivo.</b> Subsidiar uma referência técnica e <b>orientativa</b> de honorários por serviço, usando ARTs como <b>evidência auxiliar, indireta e agregada de escopo, atividade, localidade, responsabilidade técnica e valor declarado — não como prova isolada do honorário profissional efetivamente contratado.</b></p>
  <p><b>Base.</b> ARTs CREA-BA de 2022. Período disponível: somente 2022 (campo de emissão). Tratamento exclusivamente <b>agregado</b>; sem dados pessoais; sem ranking de profissionais, empresas ou contratantes (LGPD).</p>
  <p><b>Classes.</b> A (uma ART/atividade, valor associável — base de cálculo); B (composto homogêneo — secundária); C (composto ambíguo, valor único não decomponível — só frequência/diagnóstico); D (inválido/sem valor — excluída).</p>
  <p><b>Valor.</b> O valor é da ART inteira e aparece <b>replicado</b> em todas as linhas — por isso não se somam linhas. Só a Classe A calcula valor, com <b>mediana e IQR</b> (nunca média). Serviços com <code>n&lt;5</code> recebem "Informação insuficiente para verificar".</p>
  <p><b>Mapeamento serviço.</b> Atividade→serviço é uma <b>inferência por palavra-chave</b> (aproximada); atividades sem correspondência ficam como "Não mapeado / Informação insuficiente para verificar".</p>
  <p><b>Mapa.</b> A visão geográfica permanece no painel anterior (<code>dashboard_senge_honorarios_corrigido_codex.html</code>), preservado.</p>
  </div></details>
</div>

<div class="sub" style="margin-top:18px">Fonte: <span id="fonte"></span> · Documento de subsídio técnico, caráter orientativo.</div>
</div>

<script id="DATA" type="application/json">__DATA__</script>
<script>
const D=JSON.parse(document.getElementById('DATA').textContent);
const SERV=D.servicos, GRP=D.grupo_de_servico, MUN=D.municipios, ANO=D.anos, CC=D.classe_count;
const A=D.classeA, AGG=D.agg; // agg row: [classeIdx,svcIdx,anoIdx,munIdx,nArts,nAtiv]
const CLIDX={A:0,B:1,C:2,D:3};
document.getElementById('meta').textContent='Gerado em '+D.gerado_em+'.';
document.getElementById('fonte').textContent=D.fonte;
const fmt=n=>n==null?'—':n.toLocaleString('pt-BR');
const money=n=>n==null?'—':n.toLocaleString('pt-BR',{maximumFractionDigits:2});

// preencher selects
function fill(sel,items,valIsIdx){const el=document.getElementById(sel);items.forEach((t,i)=>{const o=document.createElement('option');o.value=valIsIdx?i:t;o.textContent=t;el.appendChild(o);});}
const grupos=[...new Set(GRP)].sort();
fill('fGrupo',grupos,false);
// servicos com indice
{const el=document.getElementById('fServico');SERV.map((s,i)=>[s,i]).sort((a,b)=>a[0].localeCompare(b[0])).forEach(([s,i])=>{const o=document.createElement('option');o.value=i;o.textContent=s;el.appendChild(o);});}
{const el=document.getElementById('fMun');MUN.map((s,i)=>[s,i]).sort((a,b)=>a[0].localeCompare(b[0])).forEach(([s,i])=>{const o=document.createElement('option');o.value=i;o.textContent=s;o.dataset.k=s.toLowerCase();el.appendChild(o);});}
fill('fAno',ANO,true);

document.getElementById('munSearch').addEventListener('input',e=>{const q=e.target.value.toLowerCase();[...document.getElementById('fMun').options].forEach(o=>{o.hidden=q&&!o.dataset.k.includes(q);});});

const sel=id=>new Set([...document.getElementById(id).selectedOptions].map(o=>isNaN(o.value)?o.value:+o.value));
function getF(){return{cl:sel('fClasse'),gr:sel('fGrupo'),sv:sel('fServico'),mu:sel('fMun'),an:sel('fAno')};}
function svcInGrp(grSet){if(!grSet.size)return null;const s=new Set();SERV.forEach((_,i)=>{if(grSet.has(GRP[i]))s.add(i);});return s;}

function recompute(){
  const f=getF();
  const grSvc=svcInGrp(f.gr);
  const okSvc=i=>(!f.sv.size||f.sv.has(i))&&(!grSvc||grSvc.has(i));
  const okAno=a=>!f.an.size||f.an.has(a);
  const okMun=m=>!f.mu.size||f.mu.has(m);
  const okCl=c=>!f.cl.size||f.cl.has(['A','B','C','D'][c]);
  // contadores via AGG
  let nArts=0,nAtiv=0,baseA=0;const svcSet=new Set();
  for(const r of AGG){if(okCl(r[0])&&okSvc(r[1])&&okAno(r[2])&&okMun(r[3])){nArts+=r[4];nAtiv+=r[5];svcSet.add(r[1]);if(r[0]===0)baseA+=r[4];}}
  document.getElementById('kArts').textContent=fmt(nArts);
  document.getElementById('kAtiv').textContent=fmt(nAtiv);
  document.getElementById('kServ').textContent=fmt(svcSet.size);
  document.getElementById('kBaseCalc').textContent=fmt(baseA);
  // monetario: so se classe A incluida
  const aAllowed=!f.cl.size||f.cl.has('A');
  const warn=document.getElementById('warnMon');
  const mk=document.getElementById('kpiMed'),ik=document.getElementById('kpiIqr');
  if(!aAllowed){warn.style.display='block';mk.classList.add('warn');ik.classList.add('warn');
    document.getElementById('kMed').textContent='—';document.getElementById('kIqr').textContent='—';
    renderTable(null);}
  else{warn.style.display='none';mk.classList.remove('warn');ik.classList.remove('warn');
    // filtrar microdados Classe A
    const byS={};const all=[];
    for(let i=0;i<A.v.length;i++){const s=A.s[i];if(!okSvc(s))continue;if(!okAno(A.a[i]))continue;if(!okMun(A.m[i]))continue;
      (byS[s]=byS[s]||[]).push(A.v[i]);all.push(A.v[i]);}
    const q=qtiles(all);
    document.getElementById('kMed').textContent=q?money(q.med):'—';
    document.getElementById('kIqr').textContent=q?(money(q.q1)+' – '+money(q.q3)):'—';
    renderTable(byS);}
  // barra de classes (base total, global)
  renderClassbar();
  // filtros ativos
  const parts=[];for(const[k,lab]of[['cl','Classe'],['gr','Grupo'],['sv','Serviço'],['mu','Município'],['an','Ano']]){if(f[k].size)parts.push(lab+': '+f[k].size);}
  document.getElementById('activeF').textContent=parts.length?('Filtros ativos — '+parts.join(' · ')):'Sem filtros (base completa).';
}
function qtiles(arr){if(!arr.length)return null;const a=[...arr].sort((x,y)=>x-y);const p=q=>{const k=(a.length-1)*q,f=Math.floor(k),c=Math.min(f+1,a.length-1);return a[f]+(a[c]-a[f])*(k-f);};return{med:p(.5),q1:p(.25),q3:p(.75),n:a.length};}
function renderTable(byS){
  const tb=document.querySelector('#svcTable tbody');tb.innerHTML='';
  if(!byS){tb.innerHTML='<tr><td colspan="8" class="muted">Indisponível para as classes selecionadas (apenas Classe A calcula valor).</td></tr>';return;}
  const rows=Object.keys(byS).map(s=>({s:+s,vals:byS[s]})).sort((a,b)=>b.vals.length-a.vals.length);
  if(!rows.length){tb.innerHTML='<tr><td colspan="8" class="muted">Nenhum registro Classe A para o filtro.</td></tr>';return;}
  for(const r of rows){const q=qtiles(r.vals);const n=r.vals.length;const grp=GRP[r.s];const isNew=grp.indexOf('Servico novo')===0||grp.indexOf('Serviço novo')===0;const low=n<5;
    const tags=(low?'<span class="tag low">n&lt;5</span> ':'')+(isNew?'<span class="tag new">novo</span>':'');
    const tr=document.createElement('tr');
    if(low){tr.innerHTML=`<td>${SERV[r.s]}</td><td class="muted">${grp}</td><td class="num">${n}</td><td colspan="4" class="muted">Informação insuficiente para verificar</td><td>${tags}</td>`;}
    else{tr.innerHTML=`<td>${SERV[r.s]}</td><td class="muted">${grp}</td><td class="num">${n}</td><td class="num">${money(q.med)}</td><td class="num">${money(q.q1)}</td><td class="num">${money(q.q3)}</td><td class="num">${money(q.q3-q.q1)}</td><td>${tags}</td>`;}
    tb.appendChild(tr);}
}
function renderClassbar(){const el=document.getElementById('classbar');const tot=CC.A+CC.B+CC.C+CC.D;const cols={A:'var(--a)',B:'var(--b)',C:'var(--c)',D:'var(--d)'};el.innerHTML='';for(const k of['A','B','C','D']){const w=100*CC[k]/tot;const s=document.createElement('span');s.style.width=w+'%';s.style.background=cols[k];s.textContent=w>7?(k+' '+w.toFixed(1)+'%'):'';el.appendChild(s);}}
function clearF(){['fClasse','fGrupo','fServico','fMun','fAno'].forEach(id=>{[...document.getElementById(id).options].forEach(o=>o.selected=false);});document.getElementById('munSearch').value='';[...document.getElementById('fMun').options].forEach(o=>o.hidden=false);recompute();}
['fClasse','fGrupo','fServico','fMun','fAno'].forEach(id=>document.getElementById(id).addEventListener('change',recompute));
recompute();
</script>
</body></html>"""

out = HTML.replace("__DATA__", DATA_JSON)
(BASE / "dashboard_senge_honorarios_metodologia_servicos.html").write_text(out, encoding="utf-8")
print("HTML gerado:", len(out), "chars")

