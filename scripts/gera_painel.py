# -*- coding: utf-8 -*-
"""Gera o painel principal (estilo CREA-BA) em dashboard/index.html.
Embute flat_counts.json (contagens cruzaveis por ano/municipio/modalidade/unidade/tipo) e
data.json (paineis analiticos de valor: faixas, calibracao, serie, CUB).
Choropleth via malha municipal do IBGE (UF 29), juntando por nome de municipio."""
import json, os
BASE=os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
flat=json.load(open(os.path.join(BASE,'dados','flat_counts.json'),encoding='utf-8'))
data=json.load(open(os.path.join(BASE,'dados','data.json'),encoding='utf-8'))

HTML=r'''<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Painel de Honorários e ARTs — SENGE/CREA-BA</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
:root{--b950:#061b3a;--b900:#082b58;--b800:#063f7a;--b700:#07579f;--b600:#0b68b5;--b500:#0f7ccf;
--green:#0f8a5f;--orange:#d96c2c;--red:#b5543e;--g100:#f1f5f9;--g200:#e2e8f0;--g300:#cbd5e1;--g600:#475569;--g700:#334155;--g800:#1e293b;
--card:#fff;--radius:16px;--shadow:0 10px 24px rgba(15,23,42,.10);--soft:0 4px 14px rgba(15,23,42,.08)}
*{box-sizing:border-box}body{margin:0;font-family:Inter,Arial,Helvetica,sans-serif;color:var(--g800);background:var(--g100)}
#app{min-height:100vh;background:radial-gradient(circle at 20% 10%,rgba(15,124,207,.15),transparent 30%),linear-gradient(135deg,#f8fafc,#eef4fb 45%,#f8fafc)}
.shell{display:grid;grid-template-columns:288px minmax(0,1fr);min-height:100vh}
.sidebar{background:linear-gradient(180deg,var(--b950),var(--b900) 48%,#073d72);color:#fff;padding:18px;position:sticky;top:0;height:100vh;overflow-y:auto;box-shadow:8px 0 22px rgba(2,6,23,.18);z-index:10}
.brand{display:flex;gap:12px;align-items:center;padding:10px 8px 18px;border-bottom:1px solid rgba(255,255,255,.14);margin-bottom:16px}
.logo{width:54px;height:54px;border-radius:14px;display:grid;place-items:center;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.25);font-weight:900;font-size:18px}
.brand h1{margin:0;font-size:21px;letter-spacing:-.6px}.brand p{margin:5px 0 0;font-size:11px;opacity:.84;line-height:1.2}
.ftitle{font-size:13px;font-weight:800;letter-spacing:.3px;margin:12px 4px 14px;text-transform:uppercase}
.fcard{background:rgba(255,255,255,.97);color:var(--b950);border-radius:12px;padding:10px 12px;margin-bottom:10px;box-shadow:var(--soft)}
.fcard label{display:block;margin-bottom:7px;font-size:12.5px;font-weight:800}
.fcard select{width:100%;border:1px solid var(--g200);border-radius:10px;background:#fff;color:var(--g800);padding:9px;font-size:13px;outline:none}
.fcard select:focus{border-color:var(--b500);box-shadow:0 0 0 3px rgba(15,124,207,.16)}
.btn{width:100%;margin-top:4px;background:rgba(255,255,255,.12);color:#fff;border:1px solid rgba(255,255,255,.25);border-radius:10px;padding:9px;font-size:13px;font-weight:700;cursor:pointer}
.btn:hover{background:rgba(255,255,255,.2)}
.note{margin-top:16px;border-radius:14px;padding:13px;background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.13);font-size:11.5px;line-height:1.45;color:rgba(255,255,255,.88)}
.note strong{display:block;margin-bottom:6px;color:#fff;font-size:12.5px}
.main{min-width:0;padding:20px 22px 26px}
.head{border-radius:22px;padding:20px 22px;background:linear-gradient(135deg,var(--b950),var(--b800) 58%,#0f5895);color:#fff;display:flex;justify-content:space-between;gap:20px;align-items:flex-start;box-shadow:var(--shadow);margin-bottom:14px}
.head h2{margin:0;font-size:clamp(22px,2.2vw,34px);letter-spacing:-1px;line-height:1.05}.head p{margin:8px 0 0;opacity:.86;font-size:13.5px}
.hmeta{min-width:180px;text-align:right;font-size:12px;opacity:.94;line-height:1.45}.hmeta strong{display:block;font-size:13px;color:#fff}
.status{margin:0 0 14px;padding:10px 14px;border:1px solid var(--g200);background:rgba(255,255,255,.82);color:var(--g700);border-radius:12px;font-size:12.5px;box-shadow:var(--soft)}
.status.warn{border-color:#f59e0b;background:#fffbeb;color:#92400e}
.kpis{display:grid;grid-template-columns:repeat(6,minmax(140px,1fr));gap:12px;margin-bottom:12px}
.kpi{background:var(--card);border:1px solid rgba(148,163,184,.26);border-radius:var(--radius);padding:13px;min-height:104px;box-shadow:var(--soft);display:grid;grid-template-columns:40px 1fr;gap:10px;align-items:center}
.kicon{width:40px;height:40px;border-radius:50%;display:grid;place-items:center;background:linear-gradient(135deg,var(--b900),var(--b600));color:#fff;font-size:16px;font-weight:900;box-shadow:0 6px 14px rgba(7,87,159,.24)}
.ktitle{margin:0 0 6px;font-size:11.5px;color:var(--g700);font-weight:700}.kval{margin:0;font-size:clamp(20px,2vw,28px);color:var(--b950);font-weight:900;letter-spacing:-.8px;line-height:1}
.ksub{margin:5px 0 0;color:var(--g600);font-size:11px}.kpi.green .kval{color:var(--green)}.kpi.red .kval{color:var(--red)}
.grid{display:grid;grid-template-columns:repeat(12,1fr);gap:12px}
.card{background:rgba(255,255,255,.96);border:1px solid rgba(148,163,184,.26);border-radius:var(--radius);box-shadow:var(--soft);padding:14px 16px;min-width:0;position:relative}
.card h3{margin:0 0 4px;color:var(--b950);font-size:14.5px;letter-spacing:-.2px}.card .sub{margin:0 0 10px;color:var(--g600);font-size:11.5px}
.s3{grid-column:span 3}.s4{grid-column:span 4}.s5{grid-column:span 5}.s6{grid-column:span 6}.s7{grid-column:span 7}.s8{grid-column:span 8}.s12{grid-column:span 12}
.cbox{position:relative;width:100%;height:300px}.cbox.short{height:240px}.cbox.tall{height:360px}.cbox.xtall{height:520px}
#mapa{width:100%;height:380px;border-radius:14px;overflow:hidden;background:#eaf2fb;border:1px solid var(--g200)}
.legend{position:absolute;left:26px;bottom:22px;padding:9px 11px;border-radius:12px;background:rgba(255,255,255,.92);box-shadow:var(--soft);font-size:11px;line-height:1.25;z-index:499;border:1px solid rgba(148,163,184,.22)}
.lline{display:flex;align-items:center;gap:7px;margin-top:5px;white-space:nowrap}.lc{width:18px;height:10px;border-radius:3px;border:1px solid rgba(15,23,42,.12)}
.gauge-wrap{height:240px;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:6px}
.gauge{--deg:0deg;width:240px;height:120px;border-radius:240px 240px 0 0;background:conic-gradient(from 180deg at 50% 100%,var(--b600) 0deg var(--deg),#e5e7eb var(--deg) 180deg,transparent 180deg);position:relative;overflow:hidden}
.gauge::after{content:"";position:absolute;left:40px;right:40px;bottom:0;height:80px;background:#fff;border-radius:170px 170px 0 0;box-shadow:inset 0 3px 8px rgba(15,23,42,.06)}
.gval{margin-top:-70px;z-index:1;font-size:30px;font-weight:900;color:var(--b900);letter-spacing:-1px}.gsub{color:var(--g600);font-size:11.5px;text-align:center;max-width:260px}
.foot{margin-top:12px;border-radius:12px;background:#eaf2fb;border:1px solid #d8e7f7;color:var(--g700);padding:10px 12px;font-size:11.5px;line-height:1.4}
@media(max-width:1280px){.kpis{grid-template-columns:repeat(3,minmax(150px,1fr))}.s3,.s4,.s5,.s6,.s7,.s8{grid-column:span 6}}
@media(max-width:920px){.shell{grid-template-columns:1fr}.sidebar{position:relative;height:auto}.main{padding:14px}.kpis{grid-template-columns:repeat(2,1fr)}.s3,.s4,.s5,.s6,.s7,.s8,.s12{grid-column:span 12}.head{flex-direction:column}.hmeta{text-align:left}}
</style></head><body><div id="app"><div class="shell">
<aside class="sidebar">
 <div class="brand"><div class="logo">BA</div><div><h1>SENGE · CREA-BA</h1><p>Honorários de Engenharia — evidência por ARTs</p></div></div>
 <div class="ftitle">Filtros</div>
 <div class="fcard"><label for="fAno">Ano</label><select id="fAno"></select></div>
 <div class="fcard"><label for="fMun">Município</label><select id="fMun"></select></div>
 <div class="fcard"><label for="fMod">Modalidade</label><select id="fMod"></select></div>
 <div class="fcard"><label for="fUni">Unidade de medida</label><select id="fUni"></select></div>
 <div class="fcard"><label for="fTipo">Tipo de ART</label><select id="fTipo"></select></div>
 <button class="btn" id="btnLimpar">Limpar filtros</button>
 <div class="note"><strong>Sobre os dados</strong>
  Contagens de atividades de ART (CREA-BA), 2015–2022, apenas BA. Os painéis de <b>valor</b> (faixas, calibração, mercado×CUB)
  usam mediana/IQR — a ART <b>não é honorário</b> (evidência indireta) e são referenciados à base 2022. Sem dados pessoais (LGPD).
 </div>
</aside>
<main class="main">
 <header class="head">
  <div><h2>Painel de Honorários &amp; ARTs — Bahia</h2><p>Subsídio técnico para a nova metodologia da Tabela de Honorários do SENGE/BA.</p></div>
  <div class="hmeta">Gerado em<strong id="ger"></strong><span>Fonte: ARTs CREA-BA</span></div>
 </header>
 <div id="status" class="status">Carregando malha municipal do IBGE…</div>
 <section class="kpis">
  <div class="kpi"><div class="kicon">A</div><div><p class="ktitle">Atividades de ART</p><p class="kval" id="kAtiv">0</p><p class="ksub" id="kAtivSub">no filtro</p></div></div>
  <div class="kpi"><div class="kicon">M</div><div><p class="ktitle">Municípios</p><p class="kval" id="kMun">0</p><p class="ksub">com registros</p></div></div>
  <div class="kpi"><div class="kicon">E</div><div><p class="ktitle">Modalidades</p><p class="kval" id="kMod">0</p><p class="ksub">no filtro</p></div></div>
  <div class="kpi green"><div class="kicon">R$</div><div><p class="ktitle">Mediana do valor</p><p class="kval" id="kMed">0</p><p class="ksub" id="kMedSub">base 2022</p></div></div>
  <div class="kpi"><div class="kicon">IQR</div><div><p class="ktitle">Faixa P25–P75</p><p class="kval" id="kIqr" style="font-size:19px">—</p><p class="ksub">base 2022</p></div></div>
  <div class="kpi red"><div class="kicon">U</div><div><p class="ktitle">Unidades de medida</p><p class="kval" id="kUni">0</p><p class="ksub">distintas no filtro</p></div></div>
 </section>
 <section class="grid">
  <div class="card s5"><h3>Mapa da Bahia — atividades por município</h3><p class="sub">Choropleth (malha IBGE). Cor = nº de atividades de ART no filtro.</p>
   <div id="mapa"></div>
   <div class="legend"><strong>Atividades</strong>
    <div class="lline"><span class="lc" style="background:#dbeafe"></span>1–100</div>
    <div class="lline"><span class="lc" style="background:#93c5fd"></span>101–500</div>
    <div class="lline"><span class="lc" style="background:#3b82f6"></span>501–2.000</div>
    <div class="lline"><span class="lc" style="background:#1d4ed8"></span>2.001–10.000</div>
    <div class="lline"><span class="lc" style="background:#082f7a"></span>10.001+</div></div></div>
  <div class="card s4"><h3>Top 10 municípios</h3><p class="sub">Por nº de atividades (filtro).</p><div class="cbox tall"><canvas id="cMun"></canvas></div></div>
  <div class="card s3"><h3>Tipo de ART</h3><p class="sub">Composição (filtro).</p><div class="cbox tall"><canvas id="cTipo"></canvas></div></div>

  <div class="card s5"><h3>Atividades por modalidade</h3><p class="sub">Filtro.</p><div class="cbox"><canvas id="cMod"></canvas></div></div>
  <div class="card s4"><h3>Atividades por unidade de medida</h3><p class="sub">Confirma kVA, kWp, ha, m³ além do m².</p><div class="cbox"><canvas id="cUni"></canvas></div></div>
  <div class="card s3"><h3>% precificável</h3><p class="sub">Com valor e unidade (base total).</p><div class="gauge-wrap"><div id="gauge" class="gauge"></div><div id="gval" class="gval">0%</div><div class="gsub" id="gsub"></div></div></div>

  <div class="card s6"><h3>Evolução das atividades por ano</h3><p class="sub">Respeita os demais filtros (exceto Ano).</p><div class="cbox"><canvas id="cEvol"></canvas></div></div>
  <div class="card s6"><h3>Mercado × CUB (tendência, base 2017 = 100)</h3><p class="sub">Grandezas distintas; comparação só de tendência.</p><div class="cbox"><canvas id="cCub"></canvas></div><div class="sub" id="cubNote" style="margin-top:8px"></div></div>

  <div class="card s12"><h3>Precificação por atividade (conforme tabela TOS)</h3>
   <p class="sub">Escolha a atividade para ver a faixa por unidade (piso–referência–teto, com poda de __TRIM__% nas pontas). Atividades sem unidade não são precificáveis.</p>
   <select id="fAtiv" style="width:100%;max-width:520px;border:1px solid var(--g200);border-radius:10px;padding:9px;font-size:13px;margin-bottom:10px"></select>
   <div id="pricingBox"></div></div>

  <div class="card s8"><h3>Faixas por atividade × unidade — top combinações (base 2022)</h3>
   <p class="sub">Barra = faixa P__TRIM__–P__TRIMH__ (poda de outliers); marcador verde = mediana. n≥50. Independe dos filtros de contagem.</p>
   <div class="cbox xtall"><canvas id="cCalib"></canvas></div></div>
  <div class="card s4"><h3>Precificabilidade por tipo de ART</h3>
   <p class="sub">Verde = com valor e unidade; cinza = sem (não precificável).</p>
   <div class="cbox tall"><canvas id="cPrecif"></canvas></div>
   <div class="sub" id="precifNote" style="margin-top:8px"></div></div>

  <div class="foot s12">Atividades de ART ≠ honorários: o valor declarado pode ser de obra/contrato. Use mediana/IQR como evidência indireta.
   Arquivos .xls (2015–2019) têm teto de 65.536 linhas/semestre — contagens desses anos são mínimas. Mapa requer internet (IBGE + OSM).</div>
 </section>
</main></div></div>
<script>
const FLAT=__FLAT__, DATA=__DATA__;
const $=id=>document.getElementById(id);
const fInt=new Intl.NumberFormat('pt-BR',{maximumFractionDigits:0});
const charts={}; let MAP=null,GEO=null,NAME2VAL={},code2name={};
$('ger').textContent=DATA.gerado_em||'';
const norm=s=>String(s||'').normalize('NFD').replace(/[̀-ͯ]/g,'').toUpperCase().replace(/[^A-Z0-9]/g,'');

// ----- filtros -----
const SEL={Ano:'fAno',Mun:'fMun',Mod:'fMod',Uni:'fUni',Tipo:'fTipo'};
function opts(id,arr,todos){ $(id).innerHTML=`<option value="">${todos}</option>`+arr.map((v,i)=>`<option value="${i}">${v}</option>`).join(''); }
opts('fAno',FLAT.anos,'Todos'); opts('fMun',FLAT.municipios,'Todos'); opts('fMod',FLAT.modalidades,'Todas');
opts('fUni',FLAT.unidades,'Todas'); opts('fTipo',FLAT.tipos,'Todos');
Object.values(SEL).forEach(id=>$(id).addEventListener('change',render));
$('btnLimpar').addEventListener('click',()=>{Object.values(SEL).forEach(id=>$(id).value='');render();});

function selIdx(id){const v=$(id).value;return v===''?-1:+v;}
function filtered(skip){ // skip: dimensao a ignorar (ex 'Ano' para evolucao)
  const a=selIdx('fAno'),m=selIdx('fMun'),mo=selIdx('fMod'),u=selIdx('fUni'),t=selIdx('fTipo');
  return FLAT.recs.filter(r=>(skip==='Ano'||a<0||r[0]===a)&&(m<0||r[1]===m)&&(mo<0||r[2]===mo)&&(u<0||r[3]===u)&&(t<0||r[4]===t));
}
function sumBy(recs,dimIdx,labels){const c=new Map();recs.forEach(r=>c.set(r[dimIdx],(c.get(r[dimIdx])||0)+r[5]));
  return [...c.entries()].map(([i,v])=>({label:labels[i],value:v})).sort((a,b)=>b.value-a.value);}

const baseOpts=(h=false)=>({responsive:true,maintainAspectRatio:false,indexAxis:h?'y':'x',
 plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>`${fInt.format(c.raw)}`}}},
 scales:{x:{beginAtZero:true,grid:{color:'rgba(148,163,184,.2)'},ticks:{color:'#475569',font:{size:10}}},
 y:{beginAtZero:true,grid:{color:'rgba(148,163,184,.15)'},ticks:{color:'#334155',font:{size:10}}}}});
function mk(id,type,data,opt){if(charts[id])charts[id].destroy();const e=$(id);if(e&&window.Chart)charts[id]=new Chart(e,{type,data,options:opt});}

function render(){
  const recs=filtered();
  const total=recs.reduce((s,r)=>s+r[5],0);
  const munA=sumBy(recs,1,FLAT.municipios).filter(x=>x.label!=='Outros municípios');
  const modA=sumBy(recs,2,FLAT.modalidades);
  const uniA=sumBy(recs,3,FLAT.unidades);
  const tipoA=sumBy(recs,4,FLAT.tipos);
  $('kAtiv').textContent=fInt.format(total);
  $('kAtivSub').textContent=fInt.format(recs.length)+' grupos';
  $('kMun').textContent=fInt.format(new Set(recs.map(r=>r[1])).size);
  $('kMod').textContent=fInt.format(modA.filter(x=>x.value>0).length);
  $('kUni').textContent=fInt.format(uniA.filter(x=>x.value>0).length);
  // mediana: usa breakdown da data.json quando 1 modalidade ou 1 unidade selecionada
  const moi=selIdx('fMod'),ui=selIdx('fUni');
  const lastw=s=>{const p=norm(s);return p;};const tail=s=>{const w=String(s||'').normalize('NFD').replace(/[̀-ͯ]/g,'').toUpperCase().match(/[A-Z]+/g)||[];return w[w.length-1]||'';};
  let med=DATA.faixas.mediana, sub='base 2022 (geral)';
  if(moi>=0){const t=tail(FLAT.modalidades[moi]);const f=(DATA.modalidades||[]).find(x=>tail(x.nome)===t&&x.mediana);if(f){med=f.mediana;sub='base 2022 · '+FLAT.modalidades[moi];}}
  else if(ui>=0){const nu=norm(FLAT.unidades[ui]);const f=(DATA.unidades||[]).find(x=>norm(x.nome).includes(nu)||nu.includes(norm(x.nome)));if(f&&f.mediana){med=f.mediana;sub='base 2022 · '+FLAT.unidades[ui];}}
  $('kMed').textContent='R$ '+fInt.format(med); $('kMedSub').textContent=sub;
  $('kIqr').textContent='R$ '+fInt.format(DATA.faixas.p25)+'–'+fInt.format(DATA.faixas.p75);

  mk('cMun','bar',{labels:munA.slice(0,10).map(x=>x.label),datasets:[{data:munA.slice(0,10).map(x=>x.value),backgroundColor:'#07579f',borderRadius:6}]},baseOpts(true));
  mk('cMod','bar',{labels:modA.map(x=>x.label),datasets:[{data:modA.map(x=>x.value),backgroundColor:'#0b68b5',borderRadius:6}]},baseOpts(true));
  mk('cUni','bar',{labels:uniA.slice(0,12).map(x=>x.label),datasets:[{data:uniA.slice(0,12).map(x=>x.value),backgroundColor:'#0f7ccf',borderRadius:6}]},baseOpts(true));
  mk('cTipo','doughnut',{labels:tipoA.map(x=>x.label),datasets:[{data:tipoA.map(x=>x.value),backgroundColor:['#07579f','#0b68b5','#0f7ccf','#d96c2c','#0f8a5f','#b5543e','#94a3b8'],borderWidth:0}]},
    {responsive:true,maintainAspectRatio:false,cutout:'62%',plugins:{legend:{position:'bottom',labels:{boxWidth:10,font:{size:10}}},tooltip:{callbacks:{label:c=>`${c.label}: ${fInt.format(c.raw)}`}}}});
  // evolucao (ignora filtro Ano)
  const ev=sumBy(filtered('Ano'),0,FLAT.anos).sort((a,b)=>String(a.label).localeCompare(String(b.label)));
  mk('cEvol','line',{labels:ev.map(x=>x.label),datasets:[{label:'Atividades',data:ev.map(x=>x.value),borderColor:'#07579f',backgroundColor:'rgba(7,87,159,.12)',fill:true,tension:.3,pointRadius:4,pointBackgroundColor:'#0f8a5f'}]},baseOpts(false));
  // mapa
  NAME2VAL={}; munA.forEach(x=>{NAME2VAL[norm(x.label)]=x.value;}); paintMap();
}

// ----- paineis analiticos (estaticos) -----
function staticPanels(){
  if(DATA.cub&&DATA.serie){
    const base=DATA.serie.find(s=>s.ano===2017)||DATA.serie[0];
    const mkt=DATA.serie.filter(s=>s.ano>=2017).map(s=>({x:s.ano,y:+(s.mediana/base.mediana*100).toFixed(1)}));
    const c0=DATA.cub.pontos[0].valor, yr={'Nov/2017':2017,'Nov/2023':2023,'Jun/2024':2024};
    const cub=DATA.cub.pontos.map(p=>({x:yr[p.ref],y:+(p.valor/c0*100).toFixed(1)}));
    mk('cCub','line',{datasets:[
      {label:'Mediana observada (mercado)',data:mkt,borderColor:'#0f8a5f',backgroundColor:'#0f8a5f',tension:.2,pointRadius:4},
      {label:'CUB R-1 Normal (Sinduscon-BA)',data:cub,borderColor:'#b5543e',backgroundColor:'#b5543e',borderDash:[6,4],pointRadius:5}]},
     {responsive:true,maintainAspectRatio:false,parsing:false,plugins:{legend:{labels:{font:{size:10}}}},
      scales:{x:{type:'linear',ticks:{stepSize:1,callback:v=>v,color:'#475569'},grid:{color:'rgba(148,163,184,.2)'}},
      y:{title:{display:true,text:'Índice (2017=100)'},grid:{color:'rgba(148,163,184,.2)'},ticks:{color:'#475569'}}}});
    $('cubNote').textContent='CUB +'+DATA.cub.var_2017_2024_pct+'% (2017→2024). '+DATA.cub.fonte;
  }
  drawCalib(DATA.calibracao||[]);
  // gauge % precificavel (base total)
  if(DATA.precificabilidade){const tot=DATA.precificabilidade.reduce((s,p)=>s+p.total,0),pre=DATA.precificabilidade.reduce((s,p)=>s+p.precif,0);
    const pg=tot>0?pre/tot:0; $('gauge').style.setProperty('--deg',(pg*180)+'deg'); $('gval').textContent=(pg*100).toFixed(0)+'%';
    $('gsub').textContent=fInt.format(tot-pre)+' de '+fInt.format(tot)+' registros SEM valor/unidade (não precificáveis).';
    // chart precificabilidade por tipo
    const P=DATA.precificabilidade;
    mk('cPrecif','bar',{labels:P.map(p=>p.tipo.length>18?p.tipo.slice(0,18)+'…':p.tipo),datasets:[
      {label:'Precificável',data:P.map(p=>p.precif),backgroundColor:'#0f8a5f',borderRadius:5,stack:'s'},
      {label:'Sem valor/unidade',data:P.map(p=>p.naoprecif),backgroundColor:'#cbd5e1',borderRadius:5,stack:'s'}]},
     {indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{font:{size:10}}},tooltip:{callbacks:{label:c=>`${c.dataset.label}: ${fInt.format(c.raw)}`}}},
      scales:{x:{stacked:true,grid:{color:'rgba(148,163,184,.2)'},ticks:{color:'#475569',font:{size:10}}},y:{stacked:true,ticks:{color:'#334155',font:{size:10}}}}});
    $('precifNote').textContent=`${(pg*100).toFixed(1)}% das atividades de ART têm valor e unidade. As demais (cargo-função, registros sem medida) não são precificáveis por unidade.`;
  }
  // seletor de atividade (TOS)
  if(DATA.calibracao_full){
    const ativs=[...new Set(DATA.calibracao_full.map(c=>c.atividade))].sort((a,b)=>a.localeCompare(b,'pt-BR'));
    $('fAtiv').innerHTML='<option value="">— escolha uma atividade —</option>'+ativs.map(a=>`<option>${a}</option>`).join('');
    $('fAtiv').addEventListener('change',renderPricing);
    renderPricing();
  }
}

function corConf(c){return /Baixa/.test(c)?'#b5543e':(/Média|Media/.test(c)?'#d96c2c':'#0f8a5f');}
function drawCalib(C){
  if(!C||!C.length)return;
  mk('cCalib','bar',{labels:C.map(c=>c.rotulo||(c.atividade+' ('+c.unidade+')')),datasets:[
    {label:'Faixa (com poda)',data:C.map(c=>[c.piso,c.teto]),backgroundColor:'rgba(7,87,159,.4)',borderColor:'#07579f',borderWidth:1},
    {label:'Mediana',data:C.map(c=>[c.mediana*.985,c.mediana*1.015]),backgroundColor:'#0f8a5f',borderWidth:0}]},
   {indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{font:{size:10}}},
    tooltip:{callbacks:{label:c=>{const x=C[c.dataIndex];return `n=${x.n} · piso R$${x.piso} · ref R$${x.mediana} · teto R$${x.teto} · ${x.conf||''}`;}}}},
    scales:{x:{type:'logarithmic',title:{display:true,text:'R$ (escala log)'},grid:{color:'rgba(148,163,184,.2)'},ticks:{color:'#475569'}},
    y:{stacked:true,ticks:{font:{size:9},color:'#334155'},grid:{color:'rgba(148,163,184,.12)'}}}});
}
function renderPricing(){
  const a=$('fAtiv').value, box=$('pricingBox');
  if(!a){box.innerHTML='<div style="color:#475569;font-size:13px;padding:8px">Selecione uma atividade para ver as faixas por unidade.</div>';return;}
  const its=DATA.calibracao_full.filter(c=>c.atividade===a).sort((x,y)=>y.n-x.n);
  let h='<table style="width:100%;border-collapse:collapse;font-size:13px"><thead><tr style="text-align:left;color:#334155">'
    +'<th style="padding:6px 8px">Unidade</th><th style="padding:6px 8px">n</th><th style="padding:6px 8px">Piso (R$)</th>'
    +'<th style="padding:6px 8px">Referência (R$)</th><th style="padding:6px 8px">Teto (R$)</th><th style="padding:6px 8px">Confiabilidade</th></tr></thead><tbody>';
  its.forEach(c=>{h+=`<tr style="border-top:1px solid #e2e8f0"><td style="padding:6px 8px"><b>${c.unidade}</b></td>`
    +`<td style="padding:6px 8px">${fInt.format(c.n)}</td><td style="padding:6px 8px">${fInt.format(c.piso)}</td>`
    +`<td style="padding:6px 8px;font-weight:800;color:#07579f">${fInt.format(c.mediana)}</td><td style="padding:6px 8px">${fInt.format(c.teto)}</td>`
    +`<td style="padding:6px 8px;color:${corConf(c.conf)};font-weight:700">${c.conf||''}</td></tr>`;});
  h+='</tbody></table>';
  box.innerHTML=h;
  drawCalib(its.slice(0,20).map(c=>({...c,rotulo:c.unidade})));
}

// ----- mapa IBGE -----
function corMapa(v){if(v<=0)return '#eef2f7';if(v<=100)return '#dbeafe';if(v<=500)return '#93c5fd';if(v<=2000)return '#3b82f6';if(v<=10000)return '#1d4ed8';return '#082f7a';}
function paintMap(){if(!GEO)return;GEO.eachLayer(l=>{const c=l._cod;const nm=code2name[c]||'';const v=NAME2VAL[norm(nm)]||0;
  l.setStyle({fillColor:corMapa(v),fillOpacity:v>0?.9:.45});l.bindTooltip(`${nm}<br>${fInt.format(v)} atividades`,{sticky:true});});}
async function initMap(){
  if(!window.L){$('mapa').innerHTML='<div style="padding:20px">Leaflet não carregou.</div>';return;}
  MAP=L.map('mapa',{scrollWheelZoom:false,attributionControl:false}).setView([-12.6,-41.7],6);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:10}).addTo(MAP);
  try{
    const mun=await (await fetch('https://servicodados.ibge.gov.br/api/v1/localidades/estados/29/municipios',{cache:'force-cache'})).json();
    mun.forEach(m=>code2name[String(m.id)]=m.nome);
    const gj=await (await fetch('https://servicodados.ibge.gov.br/api/v3/malhas/estados/29?formato=application/vnd.geo+json&qualidade=minima&intrarregiao=municipio',{cache:'force-cache'})).json();
    GEO=L.geoJSON(gj,{style:{color:'#fff',weight:.6,fillColor:'#eef2f7',fillOpacity:.5},
      onEachFeature:(f,l)=>{const p=f.properties||{};l._cod=String(p.codarea||p.CD_MUN||p.id||'').trim();}}).addTo(MAP);
    MAP.fitBounds(GEO.getBounds(),{padding:[6,6]});
    $('status').textContent='Dados carregados: '+fInt.format(FLAT.recs.reduce((s,r)=>s+r[5],0))+' atividades (2015–2022, BA). Use os filtros à esquerda.';
    $('status').className='status'; paintMap();
  }catch(e){console.warn(e);$('mapa').innerHTML='<div style="padding:20px;color:#475569">Não foi possível carregar a malha do IBGE (sem internet?). Os demais gráficos funcionam.</div>';
    $('status').textContent='Mapa indisponível (IBGE/internet). Demais indicadores ativos.';$('status').className='status warn';}
}
staticPanels(); render(); initMap();
</script></body></html>'''

trim=data.get('trim_pct',20)
html=(HTML.replace('__FLAT__',json.dumps(flat,ensure_ascii=False,separators=(',',':')))
          .replace('__DATA__',json.dumps(data,ensure_ascii=False,separators=(',',':')))
          .replace('__TRIMH__',str(100-trim)).replace('__TRIM__',str(trim)))
outp=os.path.join(BASE,'dashboard','index.html')
open(outp,'w',encoding='utf-8').write(html)
print('WROTE',outp,'| %.0f KB'%(len(html)/1024))

