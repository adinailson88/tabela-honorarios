# -*- coding: utf-8 -*-
"""Gera dashboard_senge_honorarios_tos_valor_municipio.html a partir de dados_tos_valor_municipio.json.
NAO sobrescreve o dashboard anterior. Tabelas centralizadas, valores em R$ (pt-BR), filtro de natureza do valor."""
import json
from pathlib import Path
BASE = Path(__file__).resolve().parent
data = json.loads((BASE / "dados_tos_valor_municipio.json").read_text(encoding="utf-8"))
DATA_JSON = json.dumps(data, ensure_ascii=False, separators=(",", ":"))

HTML = r"""<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SENGE/BA — Honorários por Serviço (camada TOS + Natureza do Valor + Município)</title>
<style>
:root{--bg:#0f1720;--card:#16212e;--mut:#8aa0b4;--fg:#e8eef5;--ac:#2f81f7;--a:#1f9d55;--b:#b58900;--c:#c9521a;--d:#9aa3ad;--line:#26323f;
 --honor:#1f9d55;--obra:#c9521a;--simb:#b58900;--inc:#9a3b3b;--insf:#5a6b7d}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.5 system-ui,Segoe UI,Roboto,Arial}
header{padding:16px 20px;border-bottom:1px solid var(--line);background:#0b121a}
h1{font-size:18px;margin:0 0 2px}h2{font-size:15px;margin:18px 0 8px}.sub{color:var(--mut);font-size:12px}
.wrap{padding:16px 20px;max-width:1320px;margin:0 auto}
.filters{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px}
.filters label{display:block;font-size:11px;color:var(--mut);margin-bottom:4px;text-transform:uppercase;letter-spacing:.04em}
select,input{width:100%;background:#0d1722;color:var(--fg);border:1px solid var(--line);border-radius:7px;padding:6px}
select[multiple]{height:118px}
.bar{display:flex;gap:8px;align-items:center;margin:10px 0;flex-wrap:wrap}
button{background:var(--ac);color:#fff;border:0;border-radius:7px;padding:8px 12px;cursor:pointer;font-weight:600}
button.ghost{background:#22303f}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-top:12px}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px;text-align:center}
.kpi .n{font-size:22px;font-weight:700}.kpi .l{color:var(--mut);font-size:12px}
.kpi.warn{border-color:var(--c)}
.kpi.good{border-color:var(--a)}
.classbar{display:flex;height:26px;border-radius:7px;overflow:hidden;border:1px solid var(--line);margin-top:6px}
.classbar span{display:flex;align-items:center;justify-content:center;font-size:11px;color:#04121a;font-weight:700}
.legend{display:flex;gap:14px;flex-wrap:wrap;margin-top:6px;font-size:12px;color:var(--mut)}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:5px;vertical-align:middle}
/* ---- Tabelas centralizadas (Tarefa 9.1) ---- */
table{width:100%;border-collapse:collapse;margin-top:8px;font-size:13px}
table th{padding:7px 8px;border-bottom:1px solid var(--line);text-align:center;vertical-align:middle;color:var(--mut);font-weight:600;position:sticky;top:0;background:var(--card)}
table td{padding:7px 8px;border-bottom:1px solid var(--line);text-align:center;vertical-align:middle;font-variant-numeric:tabular-nums}
table td.col-texto,table td.col-descricao,table td.col-observacao{text-align:left}
.tag{font-size:10px;padding:2px 6px;border-radius:20px;border:1px solid var(--line);color:var(--mut)}
.tag.new{color:#ffd479;border-color:#5a4a16;background:#241d06}
.tag.low{color:#ff9a76;border-color:#5a2a16;background:#240e06}
.tag.obra{color:#ffb38a;border-color:#5a2a16;background:#2a160c}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px;margin-top:14px}
.warnbox{background:#2a160c;border:1px solid var(--c);color:#ffcaa8;border-radius:10px;padding:12px;margin-top:12px;display:none}
.tablewrap{max-height:520px;overflow:auto;border:1px solid var(--line);border-radius:10px}
.muted{color:var(--mut)}.small{font-size:12px}
details summary{cursor:pointer;font-weight:600}
code{background:#0d1722;padding:1px 5px;border-radius:4px}
.natbar{display:flex;height:24px;border-radius:7px;overflow:hidden;border:1px solid var(--line);margin-top:6px}
.natbar span{display:flex;align-items:center;justify-content:center;font-size:10px;color:#04121a;font-weight:700}
</style></head>
<body>
<header>
<h1>SENGE/BA — Painel de Honorários por Serviço · camada TOS + Natureza do Valor + Município</h1>
<div class="sub">Evidência <b>auxiliar, indireta e agregada</b> de ARTs. Caráter <b>orientativo</b> — não é preço obrigatório, mínimo nem tabela vinculante. <span id="meta"></span></div>
</header>
<div class="wrap">

<div class="warnbox" id="warnScope" style="display:block;background:#10202c;border-color:#2f81f7;color:#bfe0ff">
<b>Escopo desta versão:</b> camada TOS = <span id="scN"></span> ARTs com <b>Código TOS</b> oficial (subconjunto da base 2022 de 230.928 ARTs). Para o restante da base, a classificação TOS é <i>Informação insuficiente para verificar</i>. Versão de <b>validação metodológica</b>.
</div>

<div class="filters">
  <div><label>Classe de confiabilidade</label><select id="fClasse" multiple><option value="A">A — base de cálculo</option><option value="B">B — secundária</option><option value="C">C — só diagnóstico</option><option value="D">D — excluída</option></select></div>
  <div><label>Natureza do valor</label><select id="fNat" multiple></select></div>
  <div><label>Grupo de serviço (SENGE)</label><select id="fGrupo" multiple></select></div>
  <div><label>Serviço padronizado</label><select id="fServico" multiple></select></div>
  <div><label>Grupo TOS</label><select id="fGrupoTos" multiple></select></div>
  <div><label>Município</label><input id="munSearch" placeholder="filtrar lista..."><select id="fMun" multiple></select></div>
  <div><label>Ano</label><select id="fAno" multiple></select></div>
</div>
<div class="bar">
  <button onclick="clearF()" class="ghost">Limpar filtros</button>
  <span id="counter" class="small muted"></span>
  <span id="activeF" class="small muted"></span>
</div>

<div class="kpis">
  <div class="kpi"><div class="n" id="kArts">—</div><div class="l">ARTs (filtradas / total)</div></div>
  <div class="kpi"><div class="n" id="kBaseCalc">—</div><div class="l">Classe A (filtrada)</div></div>
  <div class="kpi"><div class="n" id="kHonor">—</div><div class="l">Base confiável (A + provável honorário)</div></div>
  <div class="kpi good" id="kpiMed"><div class="n" id="kMed">—</div><div class="l">Mediana confiável</div></div>
  <div class="kpi good" id="kpiIqr"><div class="n" id="kIqr">—</div><div class="l">IQR confiável (Q1–Q3)</div></div>
  <div class="kpi warn" id="kpiObra"><div class="n" id="kObra">—</div><div class="l">% provável obra/contrato</div></div>
</div>

<div class="warnbox" id="warnMon">Valor monetário <b>indisponível</b> para a seleção atual. A mediana/IQR só é exibida sobre a base <b>confiável</b> = <b>Classe A</b> + natureza <b>provável honorário técnico</b>. Classes B/C/D e valores de obra/contrato, simbólicos ou inconsistentes não formam referência de honorário.</div>

<div class="card">
  <h2 style="margin-top:0">Redução do bucket "Não mapeado" (mesmo subconjunto TOS)</h2>
  <div class="kpis" style="margin-top:6px">
    <div class="kpi warn"><div class="n" id="kNmOld">—</div><div class="l">Antes — dicionário por palavra-chave</div></div>
    <div class="kpi good"><div class="n" id="kNmTos">—</div><div class="l">Depois — por Código TOS (nível TOS)</div></div>
    <div class="kpi"><div class="n" id="kNmSenge">—</div><div class="l">Sem correspondência na tabela SENGE (candidatos a novo serviço)</div></div>
  </div>
  <div class="small muted" style="margin-top:8px">FATO: 100% das ARTs deste subconjunto têm Código TOS resolvido (grupo/subgrupo/serviço). O resíduo refere-se apenas à correspondência com os serviços da tabela atual do SENGE.</div>
</div>

<div class="card">
  <h2 style="margin-top:0">Natureza do valor declarado (seleção atual)</h2>
  <div class="natbar" id="natbar"></div>
  <div class="legend">
    <span><i class="dot" style="background:var(--honor)"></i>provável honorário técnico</span>
    <span><i class="dot" style="background:var(--obra)"></i>provável obra/contrato</span>
    <span><i class="dot" style="background:var(--simb)"></i>simbólico/taxa</span>
    <span><i class="dot" style="background:var(--inc)"></i>inconsistente/extremo</span>
    <span><i class="dot" style="background:var(--insf)"></i>informação insuficiente</span>
  </div>
  <div class="small muted" style="margin-top:8px">FATO: a maior parte do valor declarado em ART é de <b>execução/obra/contrato</b>, não de honorário técnico. Por isso a Classe A, sozinha, não basta: aplica-se também o filtro de natureza do valor.</div>
</div>

<div class="card">
  <h2 style="margin-top:0">Distribuição por classe de confiabilidade (subconjunto TOS)</h2>
  <div class="classbar" id="classbar"></div>
  <div class="legend">
    <span><i class="dot" style="background:var(--a)"></i>A — uma ART/atividade (base de cálculo)</span>
    <span><i class="dot" style="background:var(--b)"></i>B — composto homogêneo (secundária)</span>
    <span><i class="dot" style="background:var(--c)"></i>C — composto ambíguo (só diagnóstico)</span>
    <span><i class="dot" style="background:var(--d)"></i>D — inválido/sem valor (excluída)</span>
  </div>
</div>

<div class="card">
  <h2 style="margin-top:0">Serviços — referência confiável observada (Classe A + provável honorário técnico)</h2>
  <div class="small muted">Mediana, Q1, Q3 e IQR em <b>R$</b>, apenas sobre a base confiável filtrada. <span class="tag low">n&lt;5</span> = Informação insuficiente para verificar. <span class="tag new">novo</span> = lacuna da tabela atual.</div>
  <div class="tablewrap"><table id="svcTable"><thead><tr>
    <th>Serviço (SENGE)</th><th>Grupo</th><th>n (A confiável)</th><th>Mediana</th><th>Q1</th><th>Q3</th><th>IQR</th><th>Obs.</th>
  </tr></thead><tbody></tbody></table></div>
  <div class="small muted" style="margin-top:6px">Valor declarado em ART filtrado para provável honorário — <b>não</b> é honorário líquido contratado.</div>
</div>

<div class="card">
  <details open><summary>Metodologia (resumo)</summary>
  <div class="small" style="margin-top:8px">
  <p><b>Premissa central.</b> Os dados de ART são utilizados como <b>evidência auxiliar, indireta e agregada de escopo, atividade, localidade, responsabilidade técnica e valor declarado, não como prova isolada do honorário profissional efetivamente contratado.</b></p>
  <p><b>1. ART ≠ honorário.</b> O valor declarado em ART pode representar honorário técnico, valor de obra/contrato, taxa/valor simbólico ou informação insuficiente. O painel separa essas naturezas e só usa a parcela de <b>provável honorário técnico</b> para referência monetária.</p>
  <p><b>2. Classe A não basta.</b> A Classe A reduz a mistura entre atividades de uma mesma ART, mas <b>não comprova sozinha a natureza do valor</b>. Por isso aplica-se um segundo filtro (natureza do valor).</p>
  <p><b>3. TOS.</b> Quando disponível, a Tabela de Obras e Serviços (Código TOS) é usada para mapear atividade→grupo/subgrupo/serviço de forma <b>determinística</b>, melhorando o mapeamento ante o dicionário por palavra-chave.</p>
  <p><b>4. Valor só quando confiável.</b> Mediana e IQR (nunca média) aparecem apenas para base confiável (Classe A + provável honorário) e com <code>n≥5</code>; abaixo disso, "Informação insuficiente para verificar". <b>Classe C/D não forma referência monetária.</b></p>
  <p><b>5. Proteção de dados.</b> Tratamento exclusivamente <b>agregado</b>; sem dados pessoais; sem ranking de profissionais, empresas ou contratantes (LGPD).</p>
  <p><b>6. Natureza orientativa.</b> A proposta é <b>referência técnica/orientativa</b>, não tabela obrigatória, preço mínimo ou imposição de honorários. Esta é uma <b>versão de validação metodológica</b>.</p>
  </div></details>
</div>

<div class="sub" style="margin-top:18px">Fonte: <span id="fonte"></span> · Documento de subsídio técnico, caráter orientativo.</div>
</div>

<script id="DATA" type="application/json">__DATA__</script>
<script>
const D=JSON.parse(document.getElementById('DATA').textContent);
const SERV=D.servicos,GRP=D.grupo_de_servico,MUN=D.municipios,ANO=D.anos,NAT=D.naturezas,GTOS=D.grupos_tos,CC=D.classe_count;
const A=D.classeA,AGG=D.agg; // agg: [cl,svc,ano,mun,nat,gt,n,ativ]
const TOTAL=D.total_arts;
const HON=NAT.indexOf('provavel_honorario_tecnico');
const NAT_LABEL={provavel_honorario_tecnico:'provável honorário técnico',provavel_valor_obra_contrato:'provável obra/contrato',valor_simbolico_ou_taxa:'simbólico/taxa',valor_inconsistente_ou_extremo:'inconsistente/extremo',informacao_insuficiente:'informação insuficiente'};
const NAT_COLOR={provavel_honorario_tecnico:'var(--honor)',provavel_valor_obra_contrato:'var(--obra)',valor_simbolico_ou_taxa:'var(--simb)',valor_inconsistente_ou_extremo:'var(--inc)',informacao_insuficiente:'var(--insf)'};
document.getElementById('meta').textContent='Gerado em '+D.gerado_em+'.';
document.getElementById('fonte').textContent=D.fonte;
document.getElementById('scN').textContent=TOTAL.toLocaleString('pt-BR');
// Tarefa 9.2 - formatacao financeira BRL
function formatBRL(value){const n=Number(value);if(!Number.isFinite(n))return 'Informação insuficiente para verificar';
  return n.toLocaleString('pt-BR',{style:'currency',currency:'BRL',minimumFractionDigits:2,maximumFractionDigits:2});}
const fmt=n=>n==null?'—':n.toLocaleString('pt-BR');
const pct=(x,t)=>t?(100*x/t).toFixed(1)+'%':'—';

// nao-mapeado before/after
document.getElementById('kNmOld').textContent=pct(D.nao_mapeado.old_keyword,TOTAL);
document.getElementById('kNmTos').textContent=pct(D.nao_mapeado.new_tos,TOTAL);
document.getElementById('kNmSenge').textContent=pct(D.nao_mapeado.new_senge,TOTAL);

function fill(sel,items,valIsIdx){const el=document.getElementById(sel);items.forEach((t,i)=>{const o=document.createElement('option');o.value=valIsIdx?i:t;o.textContent=t;el.appendChild(o);});}
const grupos=[...new Set(GRP)].sort();fill('fGrupo',grupos,false);
{const el=document.getElementById('fNat');NAT.forEach((t,i)=>{const o=document.createElement('option');o.value=i;o.textContent=NAT_LABEL[t]||t;el.appendChild(o);});}
{const el=document.getElementById('fServico');SERV.map((s,i)=>[s,i]).sort((a,b)=>a[0].localeCompare(b[0])).forEach(([s,i])=>{const o=document.createElement('option');o.value=i;o.textContent=s;el.appendChild(o);});}
{const el=document.getElementById('fGrupoTos');GTOS.map((s,i)=>[s,i]).sort((a,b)=>a[0].localeCompare(b[0])).forEach(([s,i])=>{const o=document.createElement('option');o.value=i;o.textContent=s;el.appendChild(o);});}
{const el=document.getElementById('fMun');MUN.map((s,i)=>[s,i]).sort((a,b)=>a[0].localeCompare(b[0])).forEach(([s,i])=>{const o=document.createElement('option');o.value=i;o.textContent=s;o.dataset.k=s.toLowerCase();el.appendChild(o);});}
fill('fAno',ANO,true);
document.getElementById('munSearch').addEventListener('input',e=>{const q=e.target.value.toLowerCase();[...document.getElementById('fMun').options].forEach(o=>{o.hidden=q&&!o.dataset.k.includes(q);});});

const sel=id=>new Set([...document.getElementById(id).selectedOptions].map(o=>isNaN(o.value)?o.value:+o.value));
function getF(){return{cl:sel('fClasse'),nt:sel('fNat'),gr:sel('fGrupo'),sv:sel('fServico'),gt:sel('fGrupoTos'),mu:sel('fMun'),an:sel('fAno')};}
function svcInGrp(grSet){if(!grSet.size)return null;const s=new Set();SERV.forEach((_,i)=>{if(grSet.has(GRP[i]))s.add(i);});return s;}
function qtiles(arr){if(!arr.length)return null;const a=[...arr].sort((x,y)=>x-y);const p=q=>{const k=(a.length-1)*q,f=Math.floor(k),c=Math.min(f+1,a.length-1);return a[f]+(a[c]-a[f])*(k-f);};return{med:p(.5),q1:p(.25),q3:p(.75),n:a.length};}

function recompute(){
  const f=getF();const grSvc=svcInGrp(f.gr);
  const okSvc=i=>(!f.sv.size||f.sv.has(i))&&(!grSvc||grSvc.has(i));
  const okAno=a=>!f.an.size||f.an.has(a);
  const okMun=m=>!f.mu.size||f.mu.has(m);
  const okCl=c=>!f.cl.size||f.cl.has(['A','B','C','D'][c]);
  const okNat=n=>!f.nt.size||f.nt.has(n);
  const okGt=g=>!f.gt.size||f.gt.has(g);
  // contadores + natureza distribution via AGG
  let nArts=0,baseA=0;const natCnt={};
  for(const r of AGG){if(okCl(r[0])&&okSvc(r[1])&&okAno(r[2])&&okMun(r[3])&&okNat(r[4])&&okGt(r[5])){
    nArts+=r[6];if(r[0]===0)baseA+=r[6];natCnt[r[4]]=(natCnt[r[4]]||0)+r[6];}}
  document.getElementById('kArts').textContent=fmt(nArts)+' / '+fmt(TOTAL);
  document.getElementById('kBaseCalc').textContent=fmt(baseA);
  document.getElementById('counter').textContent='Mostrando '+fmt(nArts)+' de '+fmt(TOTAL)+' ARTs ('+pct(nArts,TOTAL)+').';
  // base confiavel = Classe A + honorario, sobre microdados cA
  const aAllowed=!f.cl.size||f.cl.has('A');
  const honAllowed=!f.nt.size||f.nt.has(HON);
  const blocked=!aAllowed||!honAllowed;
  const warn=document.getElementById('warnMon');
  const mk=document.getElementById('kpiMed'),ik=document.getElementById('kpiIqr');
  let honN=0;const byS={};const all=[];
  if(!blocked){
    for(let i=0;i<A.v.length;i++){if(A.nat[i]!==HON)continue;const s=A.s[i];
      if(/^Nao mapeado/.test(SERV[s]))continue; // candidato a novo servico nao forma referencia
      if(!okSvc(s)||!okAno(A.a[i])||!okMun(A.m[i])||(f.gt.size&&!f.gt.has(A.gt[i])))continue;
      (byS[s]=byS[s]||[]).push(A.v[i]);all.push(A.v[i]);honN++;}
  }
  document.getElementById('kHonor').textContent=blocked?'—':fmt(honN);
  if(blocked){warn.style.display='block';mk.classList.add('warn');ik.classList.add('warn');mk.classList.remove('good');ik.classList.remove('good');
    document.getElementById('kMed').textContent='—';document.getElementById('kIqr').textContent='—';renderTable(null);}
  else{warn.style.display='none';mk.classList.remove('warn');ik.classList.remove('warn');mk.classList.add('good');ik.classList.add('good');
    const q=qtiles(all);
    document.getElementById('kMed').textContent=q?formatBRL(q.med):'—';
    document.getElementById('kIqr').textContent=q?(formatBRL(q.q1)+' – '+formatBRL(q.q3)):'—';
    renderTable(byS);}
  // % obra/contrato
  const obraIdx=NAT.indexOf('provavel_valor_obra_contrato');
  document.getElementById('kObra').textContent=pct(natCnt[obraIdx]||0,nArts);
  renderNatbar(natCnt,nArts);renderClassbar();
  // filtros ativos
  const parts=[];for(const[k,lab]of[['cl','Classe'],['nt','Natureza'],['gr','Grupo'],['sv','Serviço'],['gt','Grupo TOS'],['mu','Município'],['an','Ano']]){if(f[k].size)parts.push(lab+': '+f[k].size);}
  document.getElementById('activeF').textContent=parts.length?('· Filtros ativos — '+parts.join(' · ')):'· Sem filtros (subconjunto TOS completo).';
}
function renderTable(byS){
  const tb=document.querySelector('#svcTable tbody');tb.innerHTML='';
  if(!byS){tb.innerHTML='<tr><td colspan="8" class="col-texto muted">Indisponível: a base confiável exige Classe A + natureza "provável honorário técnico".</td></tr>';return;}
  const rows=Object.keys(byS).map(s=>({s:+s,vals:byS[s]})).sort((a,b)=>b.vals.length-a.vals.length);
  if(!rows.length){tb.innerHTML='<tr><td colspan="8" class="col-texto muted">Nenhum registro confiável para o filtro.</td></tr>';return;}
  for(const r of rows){const q=qtiles(r.vals);const n=r.vals.length;const grp=GRP[r.s];const isNew=/Servi[cç]o novo/.test(grp);const low=n<5;
    const tags=(low?'<span class="tag low">n&lt;5</span> ':'')+(isNew?'<span class="tag new">novo</span>':'');
    const tr=document.createElement('tr');
    if(low){tr.innerHTML=`<td class="col-texto">${SERV[r.s]}</td><td class="col-texto muted">${grp}</td><td>${n}</td><td colspan="4" class="muted">Informação insuficiente para verificar</td><td>${tags}</td>`;}
    else{tr.innerHTML=`<td class="col-texto">${SERV[r.s]}</td><td class="col-texto muted">${grp}</td><td>${n}</td><td>${formatBRL(q.med)}</td><td>${formatBRL(q.q1)}</td><td>${formatBRL(q.q3)}</td><td>${formatBRL(q.q3-q.q1)}</td><td>${tags}</td>`;}
    tb.appendChild(tr);}
}
function renderNatbar(natCnt,tot){const el=document.getElementById('natbar');el.innerHTML='';if(!tot){el.innerHTML='<span style="background:var(--insf);width:100%">sem dados</span>';return;}
  NAT.forEach((name,i)=>{const v=natCnt[i]||0;if(!v)return;const w=100*v/tot;const s=document.createElement('span');s.style.width=w+'%';s.style.background=NAT_COLOR[name];s.textContent=w>9?(w.toFixed(0)+'%'):'';s.title=NAT_LABEL[name]+': '+fmt(v)+' ('+w.toFixed(1)+'%)';el.appendChild(s);});}
function renderClassbar(){const el=document.getElementById('classbar');const tot=CC.A+CC.B+CC.C+CC.D;const cols={A:'var(--a)',B:'var(--b)',C:'var(--c)',D:'var(--d)'};el.innerHTML='';for(const k of['A','B','C','D']){const w=100*CC[k]/tot;const s=document.createElement('span');s.style.width=w+'%';s.style.background=cols[k];s.textContent=w>7?(k+' '+w.toFixed(1)+'%'):'';el.appendChild(s);}}
function clearF(){['fClasse','fNat','fGrupo','fServico','fGrupoTos','fMun','fAno'].forEach(id=>{[...document.getElementById(id).options].forEach(o=>o.selected=false);});document.getElementById('munSearch').value='';[...document.getElementById('fMun').options].forEach(o=>o.hidden=false);recompute();}
['fClasse','fNat','fGrupo','fServico','fGrupoTos','fMun','fAno'].forEach(id=>document.getElementById(id).addEventListener('change',recompute));
recompute();
</script>
</body></html>"""

out = HTML.replace("__DATA__", DATA_JSON)
(BASE / "dashboard_senge_honorarios_tos_valor_municipio.html").write_text(out, encoding="utf-8")
print("HTML gerado:", len(out), "chars ->", "dashboard_senge_honorarios_tos_valor_municipio.html")

