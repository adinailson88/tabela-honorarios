# -*- coding: utf-8 -*-
"""Gera o dashboard HTML standalone (data.json embutido + coordenadas municipais).
Saida: PROPOSTA CLAUDE/dashboard/index.html  (abrir com duplo clique)."""
import json, os

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
data = json.load(open(os.path.join(BASE, 'dados', 'data.json'), encoding='utf-8'))

# Coordenadas aproximadas (centroide municipal) - dado geografico publico, fins ilustrativos
COORDS = {
"SALVADOR":[-12.971,-38.511],"FEIRA DE SANTANA":[-12.266,-38.966],"VITÓRIA DA CONQUISTA":[-14.866,-40.839],
"CAMAÇARI":[-12.697,-38.324],"BARREIRAS":[-12.153,-44.990],"LUÍS EDUARDO MAGALHÃES":[-12.092,-45.801],
"JUAZEIRO":[-9.416,-40.503],"TEIXEIRA DE FREITAS":[-17.540,-39.742],"LAURO DE FREITAS":[-12.894,-38.327],
"ILHÉUS":[-14.793,-39.039],"JEQUIÉ":[-13.858,-40.083],"GUANAMBI":[-14.223,-42.780],"PORTO SEGURO":[-16.449,-39.065],
"PAULO AFONSO":[-9.405,-38.221],"ITABUNA":[-14.785,-39.280],"SÃO DESIDÉRIO":[-12.363,-44.973],
"EUNÁPOLIS":[-16.372,-39.580],"BOM JESUS DA LAPA":[-13.255,-43.418],"IRECÊ":[-11.304,-41.856],
"ALAGOINHAS":[-12.135,-38.419],"BRUMADO":[-14.203,-41.665],"MATA DE SÃO JOÃO":[-12.531,-38.299],
"SIMÕES FILHO":[-12.784,-38.404],"CAETITÉ":[-14.069,-42.476],"SANTO ANTÔNIO DE JESUS":[-12.969,-39.261],
"CORRENTINA":[-13.343,-44.636],"FORMOSA DO RIO PRETO":[-11.048,-45.193],"JACOBINA":[-11.181,-40.517],
"RIBEIRA DO POMBAL":[-10.836,-38.535],"LIVRAMENTO DE NOSSA SENHORA":[-13.643,-41.840],"MORRO DO CHAPÉU":[-11.549,-41.156],
"VALENÇA":[-13.370,-39.073],"CANDEIAS":[-12.667,-38.551],"SENTO SÉ":[-9.745,-41.881],"XIQUE-XIQUE":[-10.823,-42.728],
"PRADO":[-17.341,-39.221],"SERRINHA":[-11.664,-39.007],"ITAPETINGA":[-15.249,-40.247],"ITABERABA":[-12.527,-40.307],
"RIACHÃO DAS NEVES":[-11.747,-44.910],"EUCLIDES DA CUNHA":[-10.508,-39.012],"JABORANDI":[-13.617,-44.421],
"CRUZ DAS ALMAS":[-12.670,-39.102],"TUCANO":[-10.962,-38.789],"CAMPO FORMOSO":[-10.508,-40.321],
"BARRA DO CHOÇA":[-14.880,-40.578],"CASA NOVA":[-9.162,-40.970],"ITAMARAJU":[-17.039,-39.531],
"JAGUAQUARA":[-13.531,-39.972],"VERA CRUZ":[-12.957,-38.622],"SANTO ESTEVÃO":[-12.430,-39.251],
"PARIPIRANGA":[-10.687,-37.862],"SANTA CRUZ CABRÁLIA":[-16.277,-39.025],"CATU":[-12.353,-38.378],
"IBOTIRAMA":[-12.185,-43.220],"JEREMOABO":[-10.072,-38.347],"SENHOR DO BONFIM":[-10.461,-40.190],
"SEABRA":[-12.417,-41.770],"ALCOBAÇA":[-17.520,-39.196],"DIAS D ÁVILA":[-12.612,-38.295],
}
# anexa coords aos municipios (quando disponivel)
for m in data['municipios']:
    c = COORDS.get(m['nome'])
    if c: m['lat'], m['lng'] = c[0], c[1]
com_coord = sum(1 for m in data['municipios'] if 'lat' in m)
data['_cobertura_mapa'] = com_coord

HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Painel de Evidências — Honorários de Engenharia / Bahia (ARTs 2022)</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
:root{--bg:#0f1722;--card:#17212e;--ink:#e8eef5;--mut:#9fb0c3;--ac:#2e8bdb;--ac2:#36c692;--line:#243140}
*{box-sizing:border-box}body{margin:0;font-family:system-ui,Segoe UI,Roboto,Arial,sans-serif;background:var(--bg);color:var(--ink)}
header{padding:22px 26px;border-bottom:1px solid var(--line);background:linear-gradient(135deg,#13202f,#0f1722)}
h1{margin:0 0 4px;font-size:20px}.sub{color:var(--mut);font-size:13px}
.wrap{max-width:1280px;margin:0 auto;padding:18px 22px 60px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin:16px 0}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px}
.kpi b{display:block;font-size:24px}.kpi span{color:var(--mut);font-size:12px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;margin-top:16px}
.card h2{margin:0 0 4px;font-size:15px}.card p.note{margin:0 0 12px;color:var(--mut);font-size:12px}
.full{grid-column:1/-1}#map{height:520px;border-radius:10px}
canvas{max-height:340px}
.legend{font-size:12px;color:var(--mut);margin-top:8px}
.warn{background:#2a2113;border:1px solid #5a4a1f;color:#f0d894;border-radius:10px;padding:12px 14px;font-size:13px;margin-top:16px}
.foot{color:var(--mut);font-size:12px;margin-top:24px;line-height:1.6}
a{color:var(--ac)}
@media(max-width:840px){.grid{grid-template-columns:1fr}}
</style></head>
<body>
<header>
<h1>Painel de Evidências — Honorários de Engenharia na Bahia</h1>
<div class="sub">Fonte: __FONTE__ · Gerado em __DATA__ · Apenas dados agregados (LGPD) · ART não é honorário (evidência indireta)</div>
</header>
<div class="wrap">
 <div class="kpis">
  <div class="kpi"><b id="k1"></b><span>Linhas de atividade (ART)</span></div>
  <div class="kpi"><b id="k2"></b><span>ARTs distintas</span></div>
  <div class="kpi"><b id="k3"></b><span>Valores válidos analisados</span></div>
  <div class="kpi"><b id="k4"></b><span>Mediana do valor (R$)</span></div>
  <div class="kpi"><b id="k5"></b><span>Faixa interquartil P25–P75 (R$)</span></div>
 </div>

 <div class="card full">
  <h2>📍 Localização — distribuição geográfica das ARTs na Bahia</h2>
  <p class="note">Tamanho do círculo = nº de registros; cor = mediana de valor (R$). Coordenadas aproximadas (centróide municipal), fins ilustrativos. Cobertura do mapa: __COBMAPA__ municípios (de __NMUN__ exibidos).</p>
  <div id="map"></div>
  <div class="legend">⬤ menor &nbsp;→&nbsp; ⬤ maior nº de ARTs &nbsp;|&nbsp; cor: verde = mediana menor, vermelho = mediana maior.</div>
 </div>

 <div class="grid">
  <div class="card"><h2>Top municípios por nº de ARTs</h2><p class="note">20 maiores.</p><canvas id="cMun"></canvas></div>
  <div class="card"><h2>Mediana de valor por município (R$)</h2><p class="note">Top 20 municípios; mediana robusta (n≥5).</p><canvas id="cMunMed"></canvas></div>
  <div class="card"><h2>ARTs por modalidade profissional</h2><p class="note">Rótulos padronizados/agrupados.</p><canvas id="cMod"></canvas></div>
  <div class="card"><h2>Mediana de valor por modalidade (R$)</h2><p class="note">Escala logarítmica.</p><canvas id="cModMed"></canvas></div>
  <div class="card"><h2>ARTs por unidade de medida</h2><p class="note">Confirma necessidade de m², kWp, kVA, hectare, m³…</p><canvas id="cUni"></canvas></div>
  <div class="card"><h2>Tipo de ART</h2><p class="note">Composição da base.</p><canvas id="cTipo"></canvas></div>
 </div>

 <div class="grid">
  <div class="card"><h2>📈 Evolução da mediana do valor (2015–2022)</h2>
   <p class="note">Mediana anual do valor declarado (R$). Ressalva: arquivos .xls têm teto de 65.536 linhas/semestre — contagens de 2015–2019 são mínimas e a mediana é apenas indicativa.</p>
   <canvas id="cSerie"></canvas></div>
  <div class="card"><h2>↔️ Trajetórias divergentes: mercado × CUB</h2>
   <p class="note">Medem coisas diferentes — comparação apenas de tendência, base 2017 = 100.</p>
   <canvas id="cCub"></canvas>
   <div class="legend" id="cubNote"></div></div>
 </div>

 <div class="card full"><h2>🎯 Faixas por atividade × unidade (calibração das ARTs)</h2>
  <p class="note">Barra = intervalo interquartil (P25–P75); ponto = mediana. Apenas combinações com unidade homogênea e n≥50. Base para as faixas piso–referência–teto da tabela. Total de combinações válidas (n≥5): __NCALIB__.</p>
  <canvas id="cCalib" style="max-height:560px"></canvas></div>

 <div class="card full"><h2>Faixas de valor declarado (R$) — percentis</h2>
  <p class="note">Escala logarítmica. Mostra a forte dispersão e os outliers extremos: por isso usa-se mediana/IQR, nunca média.</p>
  <canvas id="cFaixa" style="max-height:260px"></canvas></div>

 <div class="warn">⚠️ <b>Leitura metodológica:</b> o campo <i>valor_contrato</i> da ART pode refletir valor de obra,
  de contrato ou declarado — <b>não necessariamente o honorário do profissional</b>. Os valores misturam
  unidades distintas e contêm erros/outliers (máx. observado &gt; R$800 milhões). As medianas servem como
  <b>evidência indireta para calibração de faixas</b>, não como prova de preço. Células com n&lt;5 são suprimidas.</div>

 <div class="foot">
  Painel de subsídio técnico — Proposta de Nova Metodologia da Tabela de Honorários do SENGE/BA.
  Dados agregados a partir das ARTs do CREA-BA (2022). Nenhum dado pessoal, profissional ou contratante é exposto;
  não há ranking individual. CSVs de origem em <code>../dados/</code>. Requer internet para carregar mapa e bibliotecas de gráfico.
 </div>
</div>
<script>
const DATA = __JSON__;
const brl = n => n==null ? 's/ dado' : n.toLocaleString('pt-BR',{maximumFractionDigits:0});
const T = DATA.totais, F = DATA.faixas;
k1.textContent = brl(T.linhas_atividade); k2.textContent = brl(T.arts_distintas);
k3.textContent = brl(T.valores_validos); k4.textContent = 'R$ '+brl(F.mediana);
k5.textContent = brl(F.p25)+'–'+brl(F.p75);

// ---- Mapa ----
const map = L.map('map',{scrollWheelZoom:false}).setView([-13.0,-41.5],6);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:12,attribution:'© OpenStreetMap'}).addTo(map);
const meds = DATA.municipios.filter(m=>m.mediana!=null).map(m=>m.mediana).sort((a,b)=>a-b);
const lo = meds[0]||0, hi = meds[meds.length-1]||1;
function colr(v){ if(v==null) return '#7d8aa0'; const t=Math.max(0,Math.min(1,(Math.log(v+1)-Math.log(lo+1))/(Math.log(hi+1)-Math.log(lo+1))));
  const r=Math.round(54+t*(231-54)), g=Math.round(198-t*(198-76)), b=Math.round(146-t*(146-60)); return `rgb(${r},${g},${b})`; }
const maxN = Math.max(...DATA.municipios.map(m=>m.n));
DATA.municipios.forEach(m=>{ if(m.lat==null) return;
  const rad = 5 + 26*Math.sqrt(m.n/maxN);
  L.circleMarker([m.lat,m.lng],{radius:rad,color:'#0b121b',weight:1,fillColor:colr(m.mediana),fillOpacity:.78})
   .bindPopup(`<b>${m.nome}</b><br>ARTs: ${brl(m.n)}<br>Mediana: ${m.mediana==null?'s/ dado (n<5)':'R$ '+brl(m.mediana)}`)
   .addTo(map);
});

const GRID={color:'#243140'}, TICK={color:'#9fb0c3'};
const baseOpts=(log=false)=>({responsive:true,plugins:{legend:{display:false}},
  scales:{x:{grid:GRID,ticks:TICK},y:{grid:GRID,ticks:TICK,type:log?'logarithmic':'linear'}}});
const bar=(id,labels,vals,horiz,log,color)=>new Chart(document.getElementById(id),{type:'bar',
  data:{labels,datasets:[{data:vals,backgroundColor:color||'#2e8bdb'}]},
  options:Object.assign(baseOpts(log),{indexAxis:horiz?'y':'x'})});

const mun20 = DATA.municipios.slice(0,20);
bar('cMun', mun20.map(m=>m.nome), mun20.map(m=>m.n), true, false, '#2e8bdb');
const munMed = DATA.municipios.filter(m=>m.mediana!=null).slice(0,20);
bar('cMunMed', munMed.map(m=>m.nome), munMed.map(m=>m.mediana), true, false, '#36c692');
bar('cMod', DATA.modalidades.map(m=>m.nome), DATA.modalidades.map(m=>m.n), true, false, '#6f8ed6');
const modMed = DATA.modalidades.filter(m=>m.mediana!=null);
bar('cModMed', modMed.map(m=>m.nome), modMed.map(m=>m.mediana), true, true, '#36c692');
bar('cUni', DATA.unidades.map(u=>u.nome), DATA.unidades.map(u=>u.n), true, false, '#c79a3a');
new Chart(document.getElementById('cTipo'),{type:'doughnut',
  data:{labels:DATA.tipos.map(t=>t.nome),datasets:[{data:DATA.tipos.map(t=>t.n),
   backgroundColor:['#2e8bdb','#36c692','#c79a3a','#d56b6b','#9b6fd6','#5fb0c7','#888']}]},
  options:{plugins:{legend:{position:'bottom',labels:{color:'#9fb0c3',font:{size:11}}}}}});
const fk=Object.keys(F), fv=Object.values(F);
bar('cFaixa', fk, fv, false, true, '#d56b6b');

// ---- Serie temporal (mediana anual) ----
if(DATA.serie && DATA.serie.length){
  const S=DATA.serie;
  new Chart(document.getElementById('cSerie'),{type:'line',
    data:{labels:S.map(s=>s.ano),datasets:[{label:'Mediana (R$)',data:S.map(s=>s.mediana),
      borderColor:'#2e8bdb',backgroundColor:'rgba(46,139,219,.15)',fill:true,tension:.25,pointRadius:4,pointBackgroundColor:'#36c692'}]},
    options:{responsive:true,plugins:{legend:{display:false},
      tooltip:{callbacks:{label:(c)=>'Mediana R$'+brl(S[c.dataIndex].mediana)+' · n='+brl(S[c.dataIndex].n)}}},
      scales:{x:{grid:GRID,ticks:TICK},y:{grid:GRID,ticks:TICK,beginAtZero:true}}}});
}
// ---- Comparacao base 100 (2017) mercado x CUB ----
if(DATA.serie && DATA.cub){
  const base=DATA.serie.find(s=>s.ano===2017);
  const mkt=DATA.serie.filter(s=>s.ano>=2017).map(s=>({x:s.ano,y:+(s.mediana/base.mediana*100).toFixed(1)}));
  const c0=DATA.cub.pontos[0].valor;
  const cub=DATA.cub.pontos.map(p=>{const y={'Nov/2017':2017,'Nov/2023':2023,'Jun/2024':2024}[p.ref];return {x:y,y:+(p.valor/c0*100).toFixed(1)};});
  new Chart(document.getElementById('cCub'),{type:'line',
    data:{datasets:[
      {label:'Mediana observada (mercado)',data:mkt,borderColor:'#36c692',backgroundColor:'#36c692',tension:.2,pointRadius:4},
      {label:'CUB R-1 Normal (Sinduscon-BA)',data:cub,borderColor:'#d56b6b',backgroundColor:'#d56b6b',borderDash:[6,4],pointRadius:5}
    ]},
    options:{responsive:true,parsing:false,plugins:{legend:{labels:{color:'#9fb0c3',font:{size:11}}}},
      scales:{x:{type:'linear',grid:GRID,ticks:{...TICK,stepSize:1,callback:v=>v}},y:{grid:GRID,ticks:TICK,title:{display:true,text:'Índice (2017=100)',color:'#9fb0c3'}}}}});
  document.getElementById('cubNote').textContent='CUB +'+DATA.cub.var_2017_2024_pct+'% (2017→2024). Fonte: '+DATA.cub.fonte;
}
// ---- Calibracao: faixa IQR (barra flutuante) + mediana (ponto) ----
if(DATA.calibracao && DATA.calibracao.length){
  const C=DATA.calibracao;
  new Chart(document.getElementById('cCalib'),{type:'bar',
    data:{labels:C.map(c=>c.rotulo),
      datasets:[
        {label:'IQR (P25–P75)',data:C.map(c=>[c.p25,c.p75]),backgroundColor:'rgba(46,139,219,.45)',borderColor:'#2e8bdb',borderWidth:1},
        {label:'Mediana',data:C.map(c=>[c.mediana*0.985,c.mediana*1.015]),backgroundColor:'#36c692',borderColor:'#36c692',borderWidth:0}
      ]},
    options:{indexAxis:'y',responsive:true,
      plugins:{legend:{labels:{color:'#9fb0c3'}},
        tooltip:{callbacks:{label:(ctx)=>{const c=C[ctx.dataIndex];return `n=${c.n} · P25 R$${c.p25} · Mediana R$${c.mediana} · P75 R$${c.p75}`;}}}},
      scales:{x:{type:'logarithmic',grid:GRID,ticks:TICK,title:{display:true,text:'R$ (escala log)',color:'#9fb0c3'}},
              y:{stacked:true,grid:GRID,ticks:{color:'#9fb0c3',font:{size:10}}}}}});
}
</script>
</body></html>"""

html = (HTML.replace('__FONTE__', data['fonte'])
            .replace('__DATA__', data['gerado_em'])
            .replace('__COBMAPA__', str(com_coord))
            .replace('__NCALIB__', str(data.get('_calibracao_combos', 0)))
            .replace('__NMUN__', str(len(data['municipios'])))
            .replace('__JSON__', json.dumps(data, ensure_ascii=False)))
os.makedirs(os.path.join(BASE, 'dashboard'), exist_ok=True)
outp = os.path.join(BASE, 'dashboard', 'index.html')
open(outp, 'w', encoding='utf-8').write(html)
print('WROTE', outp, '| mapa cobre', com_coord, 'municipios | tamanho', round(len(html)/1024,1),'KB')

