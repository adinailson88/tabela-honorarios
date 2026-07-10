# -*- coding: utf-8 -*-
"""Gera o dashboard publico a partir dos datasets saneados."""
from __future__ import annotations

import json
import re
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ASSETS = REPO / "assets"
DATASETS = ASSETS / "datasets"
DOCS = REPO / "docs"
REFERENCIA = ASSETS / "referencia"
OUT_PATH = REPO / "index.html"

HIST_MANIFEST = DATASETS / "historico" / "manifest.json"
PRECOS = DATASETS / "precos" / "resumos.json"
QUALIDADE = DATASETS / "qualidade" / "manifest.json"
TOS = DATASETS / "tos-2022" / "manifest.json"
CENTROIDES = REFERENCIA / "municipios_bahia_ibge_centroides.csv"
CONTORNO = REFERENCIA / "bahia_estado_contorno_ibge.geojson"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline_md(text: str) -> str:
    value = esc(text)
    value = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", value)
    parts = value.split("`")
    if len(parts) % 2 == 0:
        return value
    out = []
    for idx, part in enumerate(parts):
        out.append(f"<code>{part}</code>" if idx % 2 else part)
    return "".join(out)


def render_table(rows: list[str]) -> str:
    cells = [[cell.strip() for cell in row.strip().strip("|").split("|")] for row in rows]
    header = cells[0]
    body = cells[1:]
    if body and re.match(r"^[\s:-]+$", "".join(body[0])):
        body = body[1:]
    parts = ["<table class=\"doc-table\"><thead><tr>"]
    parts.extend(f"<th>{inline_md(cell)}</th>" for cell in header)
    parts.append("</tr></thead><tbody>")
    for row in body:
        parts.append("<tr>" + "".join(f"<td>{inline_md(cell)}</td>" for cell in row) + "</tr>")
    parts.append("</tbody></table>")
    return "".join(parts)


def md_to_html(text: str) -> str:
    lines = text.splitlines()
    html: list[str] = []
    para: list[str] = []

    def flush_para() -> None:
        if para:
            html.append(f"<p>{inline_md(' '.join(para))}</p>")
            para.clear()

    idx = 0
    while idx < len(lines):
        line = lines[idx].rstrip()
        if not line.strip():
            flush_para()
            idx += 1
            continue
        if line.startswith("# "):
            flush_para()
            html.append(f"<h2>{inline_md(line[2:].strip())}</h2>")
            idx += 1
            continue
        if line.startswith("## "):
            flush_para()
            html.append(f"<h3>{inline_md(line[3:].strip())}</h3>")
            idx += 1
            continue
        if line.startswith("- "):
            flush_para()
            items = []
            while idx < len(lines) and lines[idx].startswith("- "):
                items.append(f"<li>{inline_md(lines[idx][2:].strip())}</li>")
                idx += 1
            html.append("<ul>" + "".join(items) + "</ul>")
            continue
        if re.match(r"^\d+\.\s+", line):
            flush_para()
            items = []
            while idx < len(lines) and re.match(r"^\d+\.\s+", lines[idx]):
                cleaned = re.sub(r"^\d+\.\s+", "", lines[idx]).strip()
                items.append(f"<li>{inline_md(cleaned)}</li>")
                idx += 1
            html.append("<ol>" + "".join(items) + "</ol>")
            continue
        if line.startswith("|"):
            flush_para()
            table_lines = []
            while idx < len(lines) and lines[idx].startswith("|"):
                table_lines.append(lines[idx])
                idx += 1
            html.append(render_table(table_lines))
            continue
        para.append(line.strip())
        idx += 1
    flush_para()
    return "\n".join(html)


def build_docs_html() -> str:
    docs = [
        ("Metodologia", DOCS / "metodologia.md"),
        ("Limitações", DOCS / "limitacoes.md"),
        ("Fontes", DOCS / "fontes.md"),
        ("Dicionário de dados", DOCS / "dicionario-dados.md"),
        ("Auditoria", DOCS / "auditoria.md"),
    ]
    sections = []
    for title, path in docs:
        content = md_to_html(path.read_text(encoding="utf-8")) if path.exists() else f"<p>{esc('Informação insuficiente para verificar.')}</p>"
        sections.append(f"<section class=\"doc-section\"><h2>{esc(title)}</h2>{content}</section>")
    return "\n".join(sections)


def build_coords() -> dict[str, list[float]]:
    if not CENTROIDES.exists():
        return {}
    coords: dict[str, list[float]] = {}
    for line in CENTROIDES.read_text(encoding="utf-8").splitlines()[1:]:
        parts = line.split(",")
        if len(parts) < 5:
            continue
        try:
            coords[parts[1].strip()] = [float(parts[3]), float(parts[4])]
        except ValueError:
            continue
    return coords


def build_outline() -> list:
    if not CONTORNO.exists():
        return []
    geo = read_json(CONTORNO)
    geom = geo["features"][0]["geometry"]
    if geom["type"] == "Polygon":
        return [geom["coordinates"][0]]
    if geom["type"] == "MultiPolygon":
        return [poly[0] for poly in geom["coordinates"]]
    return []


def main() -> int:
    for path in [HIST_MANIFEST, PRECOS, QUALIDADE, TOS]:
        if not path.exists():
            raise SystemExit(f"Dataset ausente: {path}")
    docs_html = build_docs_html()
    coords = json.dumps(build_coords(), ensure_ascii=False, separators=(",", ":"))
    outline = json.dumps(build_outline(), separators=(",", ":"))
    hist_manifest = HIST_MANIFEST.read_text(encoding="utf-8")
    precos = PRECOS.read_text(encoding="utf-8")
    qualidade = QUALIDADE.read_text(encoding="utf-8")
    tos = TOS.read_text(encoding="utf-8")
    html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tabela de Honorários - Evidência Agregada de ARTs</title>
<style>
:root{--navy:#08294a;--blue:#0f5e9c;--sky:#dcecf8;--paper:#f6f8fb;--ink:#16212b;--muted:#5a6b7b;--line:#d7e1eb;--card:#ffffff;--shadow:0 14px 34px rgba(8,41,74,.10);--radius:18px}
*{box-sizing:border-box}body{margin:0;font-family:"Segoe UI",Tahoma,sans-serif;background:linear-gradient(180deg,#eef4f9 0%,#f7f8fb 100%);color:var(--ink)}
.shell{display:grid;grid-template-columns:320px minmax(0,1fr);min-height:100vh}.sidebar{background:linear-gradient(180deg,#06213b 0%,#0a3f6b 100%);color:#fff;padding:22px 18px;position:sticky;top:0;height:100vh;overflow:auto}
.brand{padding:8px 10px 18px;border-bottom:1px solid rgba(255,255,255,.18);margin-bottom:18px}.brand h1{margin:0;font-size:24px;line-height:1.05}.brand p{margin:8px 0 0;font-size:12px;line-height:1.45;color:rgba(255,255,255,.84)}
.group{margin-bottom:14px;background:rgba(255,255,255,.10);padding:12px;border-radius:14px}.group label{display:block;font-size:12px;font-weight:700;margin-bottom:6px}.group select,.group input{width:100%;padding:10px;border-radius:10px;border:1px solid rgba(255,255,255,.18);background:#fff;color:var(--ink)}.group select[multiple]{min-height:108px}
.button{display:inline-flex;align-items:center;justify-content:center;width:100%;padding:10px 12px;border:none;border-radius:10px;background:#fff;color:var(--navy);font-weight:800;cursor:pointer}
.main{padding:22px}.hero{background:linear-gradient(135deg,#ffffff 0%,#e9f2f8 100%);border:1px solid var(--line);border-radius:24px;padding:22px;box-shadow:var(--shadow);margin-bottom:16px}
.hero h2{margin:0;font-size:32px;line-height:1.02}.hero p{margin:10px 0 0;color:var(--muted);max-width:920px;line-height:1.5}.status{margin-top:12px;padding:12px 14px;border-radius:14px;background:#fff7df;border:1px solid #f1d48e;color:#7b5512;font-size:13px}
.filters{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0 18px}.chip{background:#eaf4fb;border:1px solid #cfe1f0;border-radius:999px;padding:7px 10px;font-size:12px;color:#23455f}
.tabs{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}.tabs button{border:1px solid var(--line);background:#fff;border-radius:999px;padding:9px 14px;font-weight:800;color:var(--navy);cursor:pointer}.tabs button.active{background:var(--navy);color:#fff;border-color:var(--navy)}
.view{display:none}.view.active{display:block}.grid{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:14px}.card{grid-column:span 12;background:var(--card);border:1px solid var(--line);border-radius:var(--radius);box-shadow:0 8px 24px rgba(8,41,74,.06);padding:16px}
.card h3{margin:0 0 8px;font-size:18px}.sub{margin:0 0 12px;color:var(--muted);font-size:13px;line-height:1.45}.kpi-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px}
.kpi{background:#fbfdff;border:1px solid var(--line);border-radius:16px;padding:14px}.kpi strong{display:block;font-size:13px;color:var(--muted)}.kpi span{display:block;margin-top:6px;font-size:28px;font-weight:800;color:var(--navy)}
.list{display:grid;gap:8px}.row{display:grid;grid-template-columns:minmax(160px,1fr) 1fr 78px;gap:10px;align-items:center}.bar{height:16px;border-radius:999px;background:#ebf1f6;overflow:hidden;border:1px solid var(--line)}.fill{height:100%;background:linear-gradient(90deg,#0f5e9c,#6ab0d7)}.row .label{font-size:13px;color:var(--ink);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.row .value{text-align:right;font-size:12px;color:var(--muted)}
.table-wrap{overflow:auto;border:1px solid var(--line);border-radius:16px}table{width:100%;border-collapse:collapse;font-size:13px}th,td{padding:10px;border-bottom:1px solid var(--line);vertical-align:top}th{background:#f7fafc;text-align:left}
.note{padding:12px 14px;border-radius:14px;background:#eef6ec;border:1px solid #c8dfc2;color:#2b5f31;font-size:13px;line-height:1.45}.warn{padding:12px 14px;border-radius:14px;background:#fff6e8;border:1px solid #f3d2a1;color:#85561a;font-size:13px;line-height:1.45}
.territory{display:grid;grid-template-columns:1.2fr .8fr;gap:14px}.map{min-height:420px;border:1px solid var(--line);border-radius:16px;background:#f8fbfd;padding:8px}.doc-section{margin-bottom:22px}.doc-section h2{font-size:20px;margin:0 0 8px;color:var(--navy)}.doc-section h3{font-size:16px;margin:14px 0 6px}.doc-section p,.doc-section li{font-size:14px;line-height:1.6;color:#273745}.doc-section ul,.doc-section ol{padding-left:24px}.doc-table{width:100%;border-collapse:collapse;font-size:13px;margin:8px 0 14px}.doc-table th,.doc-table td{border:1px solid var(--line);padding:8px}.muted{color:var(--muted)}
@media(max-width:1080px){.shell{grid-template-columns:1fr}.sidebar{position:relative;height:auto}.territory{grid-template-columns:1fr}.main{padding:14px}}
</style>
</head>
<body>
<div class="shell">
  <aside class="sidebar">
    <div class="brand"><h1>Tabela de Honorários</h1><p>Painel público redesenhado para evidência agregada, com privacidade reforçada e separação entre histórico, evidência monetária e disponibilidade TOS.</p></div>
    <div class="group"><label for="ano">Ano</label><select id="ano"></select></div>
    <div class="group"><label for="classe">Classe de confiabilidade</label><select id="classe" multiple></select></div>
    <div class="group"><label for="natureza">Natureza do valor</label><select id="natureza" multiple></select></div>
    <div class="group"><label for="grupo">Grupo de serviço</label><select id="grupo" multiple></select></div>
    <div class="group"><label for="servico">Serviço</label><select id="servico" multiple></select></div>
    <div class="group"><label for="municipioBusca">Buscar município</label><input id="municipioBusca" type="text"></div>
    <div class="group"><label for="municipio">Município</label><select id="municipio" multiple></select></div>
    <button class="button" id="limpar">Limpar filtros</button>
  </aside>
  <main class="main">
    <section class="hero">
      <h2>Evidência agregada de ARTs para leitura institucional</h2>
      <p>O painel separa panorama histórico, demanda por serviço, evidência monetária agregada elegível, leitura territorial e documentação metodológica. A camada TOS permanece desabilitada até que a fonte necessária volte a estar disponível de forma verificável.</p>
      <div id="status" class="status" role="status" aria-live="polite"></div>
      <div id="chips" class="filters" aria-live="polite"></div>
    </section>
    <div class="tabs"><button data-view="geral" class="active">Visão geral</button><button data-view="demanda">Demanda e serviços</button><button data-view="monetaria">Evidência monetária</button><button data-view="territorial">Territorial</button><button data-view="metodologia">Metodologia e auditoria</button></div>
    <section id="geral" class="view active"><div class="card"><h3>Resumo do recorte ativo</h3><p class="sub">A composição abaixo reage aos filtros. Quando um indicador não puder ser verificado com o recorte atual, o painel mostra a formulação padrão exigida.</p><div id="kpis" class="kpi-grid"></div></div><div class="card"><h3>Composição A/B/C/D</h3><p class="sub">A distribuição de classes é recalculada conforme os filtros ativos.</p><div id="classeBars" class="list"></div></div></section>
    <section id="demanda" class="view"><div class="grid"><div class="card" style="grid-column:span 7"><h3>ARTs por serviço</h3><p class="sub">Volume agregado de ARTs no recorte ativo. Não há atribuição de serviço “verdadeiro” para ART composta; a ambiguidade permanece nas classes não monetárias.</p><div id="servicoBars" class="list"></div></div><div class="card" style="grid-column:span 5"><h3>Atividades por serviço</h3><p class="sub">Quando disponível, a contagem vem do campo agregado de atividades do dataset histórico.</p><div id="atividadeBars" class="list"></div></div><div class="card"><h3>Serviços no recorte</h3><div class="table-wrap"><table id="servicosTabela"><thead><tr><th>Serviço</th><th>Grupo</th><th>ARTs</th><th>Atividades</th><th>Observação</th></tr></thead><tbody></tbody></table></div></div></div></section>
    <section id="monetaria" class="view"><div class="card"><h3>Evidência monetária observada elegível</h3><p class="sub">Somente `precos_resumo` alimenta esta visão. Classe A não prova que o valor seja honorário; ela apenas delimita o recorte elegível já agregado.</p><div id="monetariaAviso" class="warn"></div></div><div class="card"><div class="table-wrap"><table id="monetariaTabela"><thead><tr><th>Ano</th><th>Serviço</th><th>Grupo</th><th>Unidade</th><th>n</th><th>Mediana</th><th>Q1</th><th>Q3</th><th>IQR</th><th>Confiança</th></tr></thead><tbody></tbody></table></div></div><div class="card"><h3>Faixa interquartil</h3><p class="sub">Representação semântica correta da faixa Q1-Q3 dos agregados publicados.</p><div id="iqrBars" class="list"></div></div></section>
    <section id="territorial" class="view"><div class="card"><h3>Correspondência territorial</h3><p class="sub">O mapa só posiciona nomes com correspondência oficial exata. Os demais registros continuam visíveis na lista.</p><div id="territorialResumo" class="note"></div></div><div class="territory"><div class="card"><h3>Municípios do recorte</h3><div class="table-wrap"><table id="territorioTabela"><thead><tr><th>Município</th><th>ARTs</th><th>Status territorial</th></tr></thead><tbody></tbody></table></div></div><div class="card"><h3>Mapa da Bahia</h3><div id="mapa" class="map"></div><p id="mapaLegenda" class="sub"></p></div></div></section>
    <section id="metodologia" class="view"><div class="card"><h3>Manifesto de qualidade</h3><div id="qualidadeResumo" class="note"></div></div><div class="card">__DOCS_HTML__</div></section>
  </main>
</div>
<script>
const HIST_MANIFEST=__HIST_MANIFEST__,PRECOS=__PRECOS__,QUALIDADE=__QUALIDADE__,TOS=__TOS__,MUNICIPIO_COORDS=__COORDS__,BAHIA_OUTLINE=__OUTLINE__,INSUF='Informação insuficiente para verificar.';const cache=new Map();let dataset=null;
function $(id){return document.getElementById(id)}function fmtInt(v){return new Intl.NumberFormat('pt-BR').format(v||0)}function fmtPct(v){return new Intl.NumberFormat('pt-BR',{minimumFractionDigits:1,maximumFractionDigits:1}).format(v||0)+'%'}function fmtMoney(v){return typeof v==='number'?new Intl.NumberFormat('pt-BR',{style:'currency',currency:'BRL'}).format(v):INSUF}function selectedValues(id){return [...$(id).selectedOptions].map(o=>o.value)}function sortAlpha(values){return [...values].sort((a,b)=>String(a).localeCompare(String(b),'pt-BR'))}
async function loadDataset(file){if(cache.has(file))return cache.get(file);const resp=await fetch(file,{cache:'no-store'});if(!resp.ok)throw new Error('Falha ao carregar '+file);const data=await resp.json();cache.set(file,data);return data}
function populateSelect(id,values){const select=$(id);select.innerHTML='';values.forEach(value=>{const opt=document.createElement('option');opt.value=String(value);opt.textContent=String(value);select.appendChild(opt)})}
function bindSidebar(){populateSelect('ano',HIST_MANIFEST.anos.map(item=>item.ano));['classe','natureza','grupo','servico','municipio'].forEach(id=>$(id).addEventListener('change',applyFilters));$('ano').addEventListener('change',loadCurrentDataset);$('municipioBusca').addEventListener('input',()=>{const q=$('municipioBusca').value.toLowerCase();[...$('municipio').options].forEach(opt=>{opt.hidden=q&&!opt.textContent.toLowerCase().includes(q)})});$('limpar').addEventListener('click',()=>{['classe','natureza','grupo','servico','municipio'].forEach(id=>[...$(id).options].forEach(o=>o.selected=false));$('municipioBusca').value='';[...$('municipio').options].forEach(o=>o.hidden=false);applyFilters()});document.querySelectorAll('.tabs button').forEach(btn=>btn.addEventListener('click',()=>{document.querySelectorAll('.tabs button').forEach(x=>x.classList.remove('active'));document.querySelectorAll('.view').forEach(x=>x.classList.remove('active'));btn.classList.add('active');$(btn.dataset.view).classList.add('active')}))}
async function loadCurrentDataset(){const ano=$('ano').value||HIST_MANIFEST.anos[HIST_MANIFEST.anos.length-1].ano;const meta=HIST_MANIFEST.anos.find(item=>item.ano===ano);dataset=await loadDataset(meta.arquivo);populateSelect('classe',dataset.dimensions.classes);populateSelect('natureza',dataset.dimensions.naturezas);populateSelect('grupo',sortAlpha(new Set(dataset.dimensions.grupos_servico)));populateSelect('servico',sortAlpha(dataset.dimensions.servicos));populateSelect('municipio',sortAlpha(dataset.dimensions.municipios));applyFilters()}
function activeFilterState(){return{classes:new Set(selectedValues('classe')),naturezas:new Set(selectedValues('natureza')),grupos:new Set(selectedValues('grupo')),servicos:new Set(selectedValues('servico')),municipios:new Set(selectedValues('municipio'))}}
function rowMatches(row,state){const dims=dataset.dimensions,classe=dims.classes[row[0]],servico=dims.servicos[row[1]],grupo=dims.grupos_servico[row[1]],municipio=dims.municipios[row[4]],natureza=dims.naturezas[row[5]];return(!state.classes.size||state.classes.has(classe))&&(!state.servicos.size||state.servicos.has(servico))&&(!state.grupos.size||state.grupos.has(grupo))&&(!state.municipios.size||state.municipios.has(municipio))&&(!state.naturezas.size||state.naturezas.has(natureza))}
function collectMetrics(state){const dims=dataset.dimensions,byService=new Map(),byMunicipio=new Map(),byClasse=new Map();let arts=0,atividades=0,mapped=0,official=0;dataset.agg.forEach(row=>{if(!rowMatches(row,state))return;const count=row[7],acts=row[8],classe=dims.classes[row[0]],servico=dims.servicos[row[1]],grupo=dims.grupos_servico[row[1]],municipio=dims.municipios[row[4]];arts+=count;atividades+=acts;if(!/^Nao mapeado/.test(servico))mapped+=count;if(MUNICIPIO_COORDS[municipio])official+=count;byClasse.set(classe,(byClasse.get(classe)||0)+count);const svc=byService.get(servico)||{servico,grupo,arts:0,atividades:0};svc.arts+=count;svc.atividades+=acts;byService.set(servico,svc);byMunicipio.set(municipio,(byMunicipio.get(municipio)||0)+count)});return{arts,atividades,mapped,official,byService,byMunicipio,byClasse}}
function renderChips(state){const chips=['Ano: '+$('ano').value];if(state.classes.size)chips.push('Classes: '+[...state.classes].join(', '));if(state.naturezas.size)chips.push('Naturezas: '+[...state.naturezas].join(', '));if(state.grupos.size)chips.push('Grupos: '+[...state.grupos].join(', '));if(state.servicos.size)chips.push('Serviços: '+[...state.servicos].slice(0,3).join(', ')+(state.servicos.size>3?'…':''));if(state.municipios.size)chips.push('Municípios: '+[...state.municipios].slice(0,2).join(', ')+(state.municipios.size>2?'…':''));$('chips').innerHTML=chips.map(text=>'<span class="chip">'+text+'</span>').join('')}
function renderStatus(metrics){$('status').textContent='Última base disponível: 2022. Ano carregado: '+$('ano').value+'. TOS: '+TOS.mensagem+' Arquivo necessário para regeneração: '+TOS.arquivo_necessario_para_regeneracao+'. ARTs no recorte: '+fmtInt(metrics.arts)+'.'}
function renderKpis(metrics){const classeA=metrics.byClasse.get('A')||0,totalBase=dataset.resumos.total_arts||0,kpis=[['Período',dataset.periodo.rotulo],['ARTs no recorte',fmtInt(metrics.arts)],['Atividades agregadas',metrics.atividades?fmtInt(metrics.atividades):INSUF],['Classe A no recorte',fmtInt(classeA)],['Classe A (% do recorte)',metrics.arts?fmtPct(100*classeA/metrics.arts):INSUF],['Serviços mapeados (% do recorte)',metrics.arts?fmtPct(100*metrics.mapped/metrics.arts):INSUF],['Correspondência territorial oficial',metrics.arts?fmtPct(100*metrics.official/metrics.arts):INSUF],['Base publicada do ano',fmtInt(totalBase)]];$('kpis').innerHTML=kpis.map(([label,value])=>'<div class="kpi"><strong>'+label+'</strong><span>'+value+'</span></div>').join('')}
function renderBars(containerId,items){const max=Math.max(...items.map(item=>item.value),1);$(containerId).innerHTML=items.length?items.map(item=>{const width=Math.max(2,100*item.value/max);return '<div class="row"><div class="label" title="'+item.label+'">'+item.label+'</div><div class="bar"><div class="fill" style="width:'+width+'%"></div></div><div class="value">'+item.display+'</div></div>'}).join(''):'<p class="muted">'+INSUF+'</p>'}
function renderClasses(metrics){renderBars('classeBars',dataset.dimensions.classes.map(classe=>({label:classe,value:metrics.byClasse.get(classe)||0,display:fmtInt(metrics.byClasse.get(classe)||0)})))}
function renderDemand(metrics){const services=[...metrics.byService.values()].sort((a,b)=>b.arts-a.arts).slice(0,15);renderBars('servicoBars',services.map(item=>({label:item.servico,value:item.arts,display:fmtInt(item.arts)})));renderBars('atividadeBars',services.map(item=>({label:item.servico,value:item.atividades,display:fmtInt(item.atividades)})));$('servicosTabela').querySelector('tbody').innerHTML=services.map(item=>'<tr><td>'+item.servico+'</td><td>'+item.grupo+'</td><td>'+fmtInt(item.arts)+'</td><td>'+fmtInt(item.atividades)+'</td><td>'+(/^Nao mapeado/.test(item.servico)?'Ambiguidade ou lacuna de mapeamento mantida.':'Serviço agregado sem desambiguar ART composta como “verdade única”.')+'</td></tr>').join('')}
function monetaryRows(state){if(state.municipios.size)return{rows:[],message:INSUF+' Não existe agregado monetário público pré-calculado por município nesta publicação.'};const ano=$('ano').value,rows=PRECOS.rows.filter(row=>row.ano===ano&&(!state.servicos.size||state.servicos.has(row.servico))&&(!state.grupos.size||state.grupos.has(row.grupo)));return{rows,message:rows.length?'Leitura monetária restrita a agregados pré-calculados com n >= 5 e unidade preservada.':INSUF}}
function renderMonetary(state){const result=monetaryRows(state);$('monetariaAviso').textContent=result.message;const tbody=$('monetariaTabela').querySelector('tbody');if(!result.rows.length){tbody.innerHTML='<tr><td colspan="10">'+INSUF+'</td></tr>';$('iqrBars').innerHTML='<p class="muted">'+INSUF+'</p>';return}tbody.innerHTML=result.rows.map(row=>'<tr><td>'+row.ano+'</td><td>'+row.servico+'</td><td>'+row.grupo+'</td><td>'+row.unidade+'</td><td>'+fmtInt(row.n)+'</td><td>'+fmtMoney(row.mediana)+'</td><td>'+fmtMoney(row.q1)+'</td><td>'+fmtMoney(row.q3)+'</td><td>'+fmtMoney(row.iqr)+'</td><td>'+row.nivel_confianca+'</td></tr>').join('');renderBars('iqrBars',result.rows.slice(0,12).map(row=>({label:row.servico+' / '+row.unidade,value:row.iqr,display:fmtMoney(row.iqr)})))}
function projectOutline(){if(!BAHIA_OUTLINE.length)return'';const pts=[];BAHIA_OUTLINE.forEach(ring=>ring.forEach(([lon,lat])=>pts.push({lon,lat})));const lonMin=Math.min(...pts.map(p=>p.lon)),lonMax=Math.max(...pts.map(p=>p.lon)),latMin=Math.min(...pts.map(p=>p.lat)),latMax=Math.max(...pts.map(p=>p.lat)),scaleX=320/(lonMax-lonMin||1),scaleY=380/(latMax-latMin||1),project=(lat,lon)=>[(lon-lonMin)*scaleX+10,390-(lat-latMin)*scaleY];return{path:BAHIA_OUTLINE.map(ring=>'M'+ring.map(([lon,lat])=>project(lat,lon).map(v=>v.toFixed(1)).join(',')).join('L')+'Z').join(' '),project}}
function renderTerritory(metrics){const items=[...metrics.byMunicipio.entries()].sort((a,b)=>b[1]-a[1]);$('territorialResumo').textContent='ARTs com correspondência territorial oficial no recorte: '+fmtPct(metrics.arts?100*metrics.official/metrics.arts:0)+'. Registros sem correspondência oficial permanecem listados e não são excluídos.';$('territorioTabela').querySelector('tbody').innerHTML=items.map(([nome,count])=>'<tr><td>'+nome+'</td><td>'+fmtInt(count)+'</td><td>'+(MUNICIPIO_COORDS[nome]?'Correspondência oficial':'Sem correspondência oficial verificável')+'</td></tr>').join('');if(!items.length||!BAHIA_OUTLINE.length){$('mapa').innerHTML='<p class="muted">'+INSUF+'</p>';return}const outline=projectOutline(),positioned=items.filter(([nome])=>MUNICIPIO_COORDS[nome]),max=Math.max(...positioned.map(([,count])=>count),1);let svg='<svg viewBox="0 0 340 400" width="100%" height="400"><path d="'+outline.path+'" fill="#edf5fb" stroke="#8eb4cf" stroke-width="1.4"></path>';positioned.forEach(([nome,count])=>{const [lat,lon]=MUNICIPIO_COORDS[nome],[x,y]=outline.project(lat,lon),r=2.5+8*Math.sqrt(count/max);svg+='<circle cx="'+x.toFixed(1)+'" cy="'+y.toFixed(1)+'" r="'+r.toFixed(1)+'" fill="rgba(15,94,156,.55)" stroke="#0f5e9c" stroke-width="1.2"><title>'+nome+': '+count+' ARTs</title></circle>'});svg+='</svg>';$('mapa').innerHTML=svg;$('mapaLegenda').textContent='Tamanho e cor das bolhas representam volume de ARTs no recorte. Apenas nomes com correspondência oficial entram no mapa.'}
function renderQuality(){$('qualidadeResumo').textContent='Privacidade: '+QUALIDADE.regra_privacidade+' Checks: publicação sem microdados = '+QUALIDADE.checks.publicacao_sem_microdados+', build determinístico = '+QUALIDADE.checks.build_deterministico+'.'}
function applyFilters(){if(!dataset)return;const state=activeFilterState(),metrics=collectMetrics(state);renderChips(state);renderStatus(metrics);renderKpis(metrics);renderClasses(metrics);renderDemand(metrics);renderMonetary(state);renderTerritory(metrics);renderQuality()}
bindSidebar();loadCurrentDataset().catch(err=>{$('status').textContent='Falha ao carregar o painel. '+err.message})
</script>
</body>
</html>"""
    final_html = (
        html.replace("__DOCS_HTML__", docs_html)
        .replace("__HIST_MANIFEST__", hist_manifest)
        .replace("__PRECOS__", precos)
        .replace("__QUALIDADE__", qualidade)
        .replace("__TOS__", tos)
        .replace("__COORDS__", coords)
        .replace("__OUTLINE__", outline)
    )
    OUT_PATH.write_text(final_html, encoding="utf-8")
    print(f"HTML gerado em {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
