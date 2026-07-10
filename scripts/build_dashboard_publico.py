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

INSUF = "Informacao insuficiente para verificar."


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
    out: list[str] = []
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
        ("Limitacoes", DOCS / "limitacoes.md"),
        ("Fontes", DOCS / "fontes.md"),
        ("Dicionario de dados", DOCS / "dicionario-dados.md"),
        ("Auditoria", DOCS / "auditoria.md"),
    ]
    sections = []
    for title, path in docs:
        if path.exists():
            content = md_to_html(path.read_text(encoding="utf-8"))
        else:
            content = f"<p>{esc(INSUF)}</p>"
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
<title>Tabela de Honorarios - Evidencia agregada de ARTs</title>
<style>
:root{
  --navy:#09243a;
  --teal:#146c74;
  --sand:#f5ecd9;
  --paper:#f6f7f4;
  --ink:#182128;
  --muted:#5f6a72;
  --line:#d7ddd8;
  --card:#ffffff;
  --accent:#c96f2d;
  --ok:#215a2f;
  --warn:#8c5a16;
  --soft:#e6f0ef;
  --shadow:0 16px 38px rgba(9,36,58,.08);
  --radius:20px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0;
  font-family:Georgia,"Times New Roman",serif;
  background:
    radial-gradient(circle at top right, rgba(201,111,45,.10), transparent 22%),
    linear-gradient(180deg,#eef1ec 0%,#f8f8f4 100%);
  color:var(--ink);
}
a{color:inherit}
.sr-only{
  position:absolute;
  width:1px;
  height:1px;
  padding:0;
  margin:-1px;
  overflow:hidden;
  clip:rect(0,0,0,0);
  white-space:nowrap;
  border:0;
}
.skip-link{
  position:absolute;
  left:12px;
  top:-48px;
  background:#fff;
  color:var(--navy);
  padding:10px 14px;
  border-radius:999px;
  border:1px solid var(--line);
  z-index:50;
}
.skip-link:focus{top:12px}
:focus-visible{
  outline:3px solid var(--accent);
  outline-offset:2px;
}
.shell{
  display:grid;
  grid-template-columns:320px minmax(0,1fr);
  min-height:100vh;
}
.sidebar{
  background:
    linear-gradient(180deg, rgba(9,36,58,.98) 0%, rgba(17,79,84,.98) 100%);
  color:#fff;
  padding:24px 18px;
  position:sticky;
  top:0;
  height:100vh;
  overflow:auto;
}
.brand{
  padding:10px 10px 18px;
  border-bottom:1px solid rgba(255,255,255,.18);
  margin-bottom:18px;
}
.eyebrow{
  display:inline-block;
  font-size:11px;
  letter-spacing:.16em;
  text-transform:uppercase;
  color:#a8d6cf;
  margin-bottom:8px;
}
.brand h1{
  margin:0;
  font-size:28px;
  line-height:1;
}
.brand p{
  margin:10px 0 0;
  font-size:13px;
  line-height:1.55;
  color:rgba(255,255,255,.86);
}
.group{
  margin-bottom:14px;
  background:rgba(255,255,255,.10);
  padding:12px;
  border-radius:16px;
}
.group label{
  display:block;
  font-size:12px;
  font-weight:700;
  margin-bottom:6px;
}
.group small{
  display:block;
  color:rgba(255,255,255,.78);
  line-height:1.4;
  margin-top:5px;
  font-size:11px;
}
.group select,
.group input{
  width:100%;
  padding:10px;
  border-radius:12px;
  border:1px solid rgba(255,255,255,.18);
  background:#fff;
  color:var(--ink);
  font:inherit;
}
.group select[multiple]{min-height:112px}
.button{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  width:100%;
  padding:12px 14px;
  border:none;
  border-radius:12px;
  background:#fff;
  color:var(--navy);
  font-weight:700;
  cursor:pointer;
  font:inherit;
}
.sidebar-note{
  margin-top:14px;
  padding:12px;
  border:1px solid rgba(255,255,255,.18);
  border-radius:16px;
  font-size:12px;
  line-height:1.5;
  color:rgba(255,255,255,.82);
}
.main{padding:24px}
.hero{
  background:
    linear-gradient(135deg, rgba(255,255,255,.96) 0%, rgba(230,240,239,.95) 55%, rgba(245,236,217,.96) 100%);
  border:1px solid var(--line);
  border-radius:28px;
  padding:24px;
  box-shadow:var(--shadow);
  margin-bottom:18px;
  position:relative;
  overflow:hidden;
}
.hero::after{
  content:"";
  position:absolute;
  inset:auto -40px -50px auto;
  width:220px;
  height:220px;
  border-radius:50%;
  background:radial-gradient(circle, rgba(20,108,116,.12), transparent 70%);
}
.hero h2{
  margin:0;
  font-size:34px;
  line-height:1.04;
  max-width:900px;
}
.hero p{
  margin:12px 0 0;
  color:var(--muted);
  max-width:900px;
  line-height:1.65;
  font-size:15px;
}
.hero-meta{
  display:flex;
  gap:8px;
  flex-wrap:wrap;
  margin-top:14px;
}
.pill,.scope,.chip{
  display:inline-flex;
  align-items:center;
  gap:6px;
  border-radius:999px;
  padding:8px 12px;
  font-size:12px;
  line-height:1.2;
}
.pill{
  background:#fff;
  border:1px solid var(--line);
  color:var(--navy);
}
.scope{
  background:rgba(20,108,116,.10);
  border:1px solid rgba(20,108,116,.24);
  color:var(--teal);
  font-weight:700;
}
.status{
  margin-top:14px;
  padding:13px 15px;
  border-radius:16px;
  background:#fffdf2;
  border:1px solid #efd8a6;
  color:var(--warn);
  font-size:13px;
  line-height:1.5;
}
.filters{
  display:flex;
  gap:8px;
  flex-wrap:wrap;
  margin:14px 0 0;
}
.chip{
  background:#eef4f1;
  border:1px solid #cddad7;
  color:#27444a;
}
.tabs{
  display:flex;
  gap:8px;
  flex-wrap:wrap;
  margin-bottom:14px;
}
.tabs button{
  border:1px solid var(--line);
  background:#fff;
  border-radius:999px;
  padding:10px 14px;
  font-weight:700;
  color:var(--navy);
  cursor:pointer;
  font:inherit;
}
.tabs button.active{
  background:var(--navy);
  color:#fff;
  border-color:var(--navy);
}
.view{display:none}
.view.active{display:block}
.grid{
  display:grid;
  grid-template-columns:repeat(12,minmax(0,1fr));
  gap:14px;
}
.card{
  grid-column:span 12;
  background:var(--card);
  border:1px solid var(--line);
  border-radius:var(--radius);
  box-shadow:0 10px 26px rgba(9,36,58,.05);
  padding:18px;
}
.card-head{
  display:flex;
  align-items:flex-start;
  justify-content:space-between;
  gap:12px;
  margin-bottom:10px;
}
.card h3{
  margin:0;
  font-size:19px;
}
.sub{
  margin:0;
  color:var(--muted);
  font-size:13px;
  line-height:1.55;
}
.badge-wrap{
  display:flex;
  gap:6px;
  flex-wrap:wrap;
}
.flag{
  display:inline-flex;
  align-items:center;
  border-radius:999px;
  padding:6px 10px;
  font-size:11px;
  font-weight:700;
}
.flag.global{
  background:#eef5fb;
  color:#275b7a;
  border:1px solid #c8dced;
}
.flag.filter{
  background:#eef6ec;
  color:#2c5e32;
  border:1px solid #cfe1c8;
}
.flag.caution{
  background:#fff4e5;
  color:#8d5a16;
  border:1px solid #f0d2a3;
}
.kpi-grid{
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(180px,1fr));
  gap:12px;
}
.kpi{
  background:#fcfcfa;
  border:1px solid var(--line);
  border-radius:16px;
  padding:14px;
}
.kpi strong{
  display:block;
  font-size:12px;
  color:var(--muted);
  text-transform:uppercase;
  letter-spacing:.05em;
}
.kpi span{
  display:block;
  margin-top:8px;
  font-size:28px;
  line-height:1.1;
  font-weight:700;
  color:var(--navy);
}
.kpi small{
  display:block;
  margin-top:8px;
  color:var(--muted);
  font-size:12px;
  line-height:1.45;
}
.list{
  display:grid;
  gap:8px;
}
.row{
  display:grid;
  grid-template-columns:minmax(150px,1fr) minmax(110px,1.5fr) 92px;
  gap:10px;
  align-items:center;
}
.label{
  font-size:13px;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}
.bar{
  height:16px;
  border-radius:999px;
  background:#edf1ef;
  overflow:hidden;
  border:1px solid var(--line);
}
.fill{
  height:100%;
  background:linear-gradient(90deg,var(--teal),#77b8bb);
}
.value{
  text-align:right;
  font-size:12px;
  color:var(--muted);
}
.note,.warn{
  padding:13px 15px;
  border-radius:16px;
  font-size:13px;
  line-height:1.6;
}
.note{
  background:#eef7ef;
  border:1px solid #cadecb;
  color:var(--ok);
}
.warn{
  background:#fff7ea;
  border:1px solid #f0d5a8;
  color:var(--warn);
}
.split{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:14px;
}
.territory{
  display:grid;
  grid-template-columns:1.15fr .85fr;
  gap:14px;
}
.table-wrap{
  overflow:auto;
  border:1px solid var(--line);
  border-radius:16px;
}
table{
  width:100%;
  border-collapse:collapse;
  font-size:13px;
}
th,td{
  padding:10px;
  border-bottom:1px solid var(--line);
  vertical-align:top;
}
th{
  background:#f7f8f5;
  text-align:left;
}
.doc-section{margin-bottom:22px}
.doc-section h2{
  font-size:20px;
  margin:0 0 8px;
  color:var(--navy);
}
.doc-section h3{
  font-size:16px;
  margin:14px 0 6px;
}
.doc-section p,
.doc-section li{
  font-size:14px;
  line-height:1.65;
  color:#273745;
}
.doc-section ul,
.doc-section ol{padding-left:24px}
.doc-table{
  width:100%;
  border-collapse:collapse;
  font-size:13px;
  margin:8px 0 14px;
}
.doc-table th,.doc-table td{
  border:1px solid var(--line);
  padding:8px;
}
.muted{color:var(--muted)}
.map{
  min-height:420px;
  border:1px solid var(--line);
  border-radius:16px;
  background:#fbfcfa;
  padding:8px;
}
.stack{display:grid;gap:12px}
@media(max-width:1080px){
  .shell{grid-template-columns:1fr}
  .sidebar{position:relative;height:auto}
  .territory,.split{grid-template-columns:1fr}
  .main{padding:14px}
  .hero h2{font-size:28px}
}
@media(max-width:720px){
  .row{grid-template-columns:1fr}
  .value{text-align:left}
  .tabs{overflow:auto;flex-wrap:nowrap;padding-bottom:2px}
  .tabs button{white-space:nowrap}
  .hero-meta,.filters{gap:6px}
}
</style>
</head>
<body>
<a class="skip-link" href="#conteudo">Ir para o conteudo principal</a>
<div class="shell">
  <aside class="sidebar" aria-label="Filtros e navegacao lateral">
    <div class="brand">
      <span class="eyebrow">Publicacao institucional</span>
      <h1>Tabela de Honorarios</h1>
      <p>Painel publico para leitura agregada de ARTs, com separacao entre panorama historico, evidencia monetaria elegivel, cobertura territorial e documentacao metodologica.</p>
    </div>
    <div class="group">
      <label for="ano">Ano publicado</label>
      <select id="ano" aria-label="Selecionar ano publicado"></select>
      <small>O painel destaca visualmente que a ultima base disponivel e 2022.</small>
    </div>
    <div class="group">
      <label for="classe">Classe de confiabilidade</label>
      <select id="classe" multiple aria-label="Filtrar por classe de confiabilidade"></select>
      <small>Afeta a leitura historica, de demanda e territorial.</small>
    </div>
    <div class="group">
      <label for="natureza">Natureza do valor</label>
      <select id="natureza" multiple aria-label="Filtrar por natureza do valor"></select>
      <small>Na visao monetaria, filtros fora do recorte elegivel retornam a mensagem padrao.</small>
    </div>
    <div class="group">
      <label for="grupo">Grupo de servico</label>
      <select id="grupo" multiple aria-label="Filtrar por grupo de servico"></select>
    </div>
    <div class="group">
      <label for="servico">Servico</label>
      <select id="servico" multiple aria-label="Filtrar por servico"></select>
    </div>
    <div class="group">
      <label for="municipioBusca">Buscar municipio na lista</label>
      <input id="municipioBusca" type="text" aria-label="Buscar municipio na lista">
    </div>
    <div class="group">
      <label for="municipio">Municipio</label>
      <select id="municipio" multiple aria-label="Filtrar por municipio"></select>
      <small>A visao monetaria nao tem agregado publico por municipio nesta publicacao.</small>
    </div>
    <button class="button" id="limpar" type="button">Limpar filtros</button>
    <div class="sidebar-note">
      Componentes marcados como <strong>Global</strong> nao reagem aos filtros. Componentes marcados como <strong>Recorte ativo</strong> recalculam o conteudo a partir do filtro atual.
    </div>
  </aside>
  <main id="conteudo" class="main" tabindex="-1">
    <section class="hero">
      <span class="eyebrow">Fase 3 - leitura por finalidade</span>
      <h2>Evidencia agregada para leitura tecnica, sem publicar ART individual nem presumir honorario como fato.</h2>
      <p>O painel organiza a leitura em cinco visoes: contexto geral da base, demanda por servicos, evidencia monetaria observada elegivel, cobertura territorial e documentacao metodologica com manifesto de qualidade. A camada TOS permanece desabilitada ate a volta da fonte local verificavel necessaria para regeneracao.</p>
      <div class="hero-meta">
        <span class="pill">Ultima base disponivel: <strong>2022</strong></span>
        <span class="scope">Camada TOS: desabilitada</span>
        <span class="scope">Regra monetaria minima: n >= 5</span>
      </div>
      <div id="status" class="status" role="status" aria-live="polite"></div>
      <div id="chips" class="filters" aria-live="polite"></div>
    </section>

    <div class="tabs" role="tablist" aria-label="Navegacao entre visoes do painel">
      <button id="tab-geral" class="active" role="tab" aria-selected="true" aria-controls="geral" data-view="geral" type="button">Visao geral</button>
      <button id="tab-demanda" role="tab" aria-selected="false" aria-controls="demanda" data-view="demanda" type="button">Demanda e servicos</button>
      <button id="tab-monetaria" role="tab" aria-selected="false" aria-controls="monetaria" data-view="monetaria" type="button">Evidencia monetaria</button>
      <button id="tab-territorial" role="tab" aria-selected="false" aria-controls="territorial" data-view="territorial" type="button">Territorial</button>
      <button id="tab-metodologia" role="tab" aria-selected="false" aria-controls="metodologia" data-view="metodologia" type="button">Metodologia e auditoria</button>
    </div>

    <section id="geral" class="view active" role="tabpanel" aria-labelledby="tab-geral">
      <div class="stack">
        <div class="card">
          <div class="card-head">
            <div>
              <h3>Resumo do recorte ativo</h3>
              <p class="sub">Indicadores recalculados com os filtros ativos, sem esconder as limitacoes do contrato publico atual.</p>
            </div>
            <div class="badge-wrap"><span class="flag filter">Recorte ativo</span></div>
          </div>
          <div id="kpis" class="kpi-grid"></div>
        </div>
        <div class="split">
          <div class="card">
            <div class="card-head">
              <div>
                <h3>Composicao A/B/C/D</h3>
                <p class="sub">Distribuicao por classe recalculada conforme o recorte ativo.</p>
              </div>
              <div class="badge-wrap"><span class="flag filter">Recorte ativo</span></div>
            </div>
            <p id="classeDesc" class="sr-only"></p>
            <div id="classeBars" class="list" aria-describedby="classeDesc"></div>
          </div>
          <div class="card">
            <div class="card-head">
              <div>
                <h3>Alertas e contexto</h3>
                <p class="sub">Avisos metodologicos e operacionais que independem de inferencia local pelo usuario.</p>
              </div>
              <div class="badge-wrap"><span class="flag global">Global</span></div>
            </div>
            <div id="alertasGerais" class="stack"></div>
          </div>
        </div>
      </div>
    </section>

    <section id="demanda" class="view" role="tabpanel" aria-labelledby="tab-demanda">
      <div class="grid">
        <div class="card" style="grid-column:span 5">
          <div class="card-head">
            <div>
              <h3>Demanda agregada por servico</h3>
              <p class="sub">Leitura por ARTs agregadas. Quando ha ambiguidade, o painel nao fabrica um servico unico verdadeiro para a ART composta.</p>
            </div>
            <div class="badge-wrap"><span class="flag filter">Recorte ativo</span></div>
          </div>
          <p id="servicoDesc" class="sr-only"></p>
          <div id="servicoBars" class="list" aria-describedby="servicoDesc"></div>
        </div>
        <div class="card" style="grid-column:span 7">
          <div class="card-head">
            <div>
              <h3>Cobertura de mapeamento e lacunas</h3>
              <p class="sub">Separacao entre volume mapeado, lacuna metodologica e casos que permanecem como diagnostico de demanda.</p>
            </div>
            <div class="badge-wrap"><span class="flag filter">Recorte ativo</span></div>
          </div>
          <div id="demandaResumo" class="note"></div>
          <div class="table-wrap" style="margin-top:12px">
            <table id="servicosTabela" aria-label="Tabela de servicos no recorte ativo">
              <thead>
                <tr><th>Servico</th><th>Grupo</th><th>ARTs</th><th>Atividades</th><th>Leitura metodologica</th></tr>
              </thead>
              <tbody></tbody>
            </table>
          </div>
        </div>
      </div>
    </section>

    <section id="monetaria" class="view" role="tabpanel" aria-labelledby="tab-monetaria">
      <div class="stack">
        <div class="card">
          <div class="card-head">
            <div>
              <h3>Evidencia monetaria observada elegivel</h3>
              <p class="sub">Usa somente `precos_resumo`. Filtros monetarios so podem alterar o resultado quando existe agregado publico pre-calculado correspondente.</p>
            </div>
            <div class="badge-wrap">
              <span class="flag global">Ano + servico + grupo</span>
              <span class="flag caution">Sem agregado por municipio</span>
            </div>
          </div>
          <div id="monetariaAviso" class="warn" role="alert"></div>
        </div>
        <div class="split">
          <div class="card">
            <div class="card-head">
              <div>
                <h3>Tabela monetaria</h3>
                <p class="sub">Cada linha ja respeita Classe A, natureza provavel honorario tecnico e n minimo publicado.</p>
              </div>
              <div class="badge-wrap"><span class="flag global">Global</span></div>
            </div>
            <div class="table-wrap">
              <table id="monetariaTabela" aria-label="Tabela de evidencia monetaria agregada">
                <thead>
                  <tr><th>Ano</th><th>Servico</th><th>Grupo</th><th>Unidade</th><th>n</th><th>Mediana</th><th>Q1</th><th>Q3</th><th>IQR</th><th>Confianca</th></tr>
                </thead>
                <tbody></tbody>
              </table>
            </div>
          </div>
          <div class="card">
            <div class="card-head">
              <div>
                <h3>Faixa interquartil</h3>
                <p class="sub">Leitura visual da dispersao entre Q1 e Q3, sem chamar a visualizacao de boxplot quando ela nao implementa a semantica completa.</p>
              </div>
              <div class="badge-wrap"><span class="flag global">Global</span></div>
            </div>
            <p id="iqrDesc" class="sr-only"></p>
            <div id="iqrBars" class="list" aria-describedby="iqrDesc"></div>
          </div>
        </div>
      </div>
    </section>

    <section id="territorial" class="view" role="tabpanel" aria-labelledby="tab-territorial">
      <div class="stack">
        <div class="card">
          <div class="card-head">
            <div>
              <h3>Cobertura territorial do recorte</h3>
              <p class="sub">Nomes com correspondencia oficial exata entram no mapa. Os demais continuam visiveis na listagem e nao sao tratados como inexistentes.</p>
            </div>
            <div class="badge-wrap"><span class="flag filter">Recorte ativo</span></div>
          </div>
          <div id="territorialResumo" class="note"></div>
        </div>
        <div class="territory">
          <div class="card">
            <div class="card-head">
              <div>
                <h3>Municipios no recorte</h3>
                <p class="sub">Lista completa do recorte ativo, incluindo registros nao posicionaveis no mapa.</p>
              </div>
              <div class="badge-wrap"><span class="flag filter">Recorte ativo</span></div>
            </div>
            <div class="table-wrap">
              <table id="territorioTabela" aria-label="Tabela territorial por municipio">
                <thead>
                  <tr><th>Municipio</th><th>ARTs</th><th>Status territorial</th></tr>
                </thead>
                <tbody></tbody>
              </table>
            </div>
          </div>
          <div class="card">
            <div class="card-head">
              <div>
                <h3>Mapa da Bahia</h3>
                <p class="sub">Somente nomes com correspondencia oficial entram no posicionamento cartografico.</p>
              </div>
              <div class="badge-wrap"><span class="flag filter">Recorte ativo</span></div>
            </div>
            <div id="mapa" class="map" role="img" aria-label="Mapa da Bahia com bolhas proporcionais ao volume de ARTs em municipios com correspondencia oficial"></div>
            <p id="mapaLegenda" class="sub"></p>
          </div>
        </div>
      </div>
    </section>

    <section id="metodologia" class="view" role="tabpanel" aria-labelledby="tab-metodologia">
      <div class="stack">
        <div class="split">
          <div class="card">
            <div class="card-head">
              <div>
                <h3>Manifesto de qualidade e contrato publico</h3>
                <p class="sub">Resumo das regras de privacidade, checks do build e fontes locais ainda indisponiveis.</p>
              </div>
              <div class="badge-wrap"><span class="flag global">Global</span></div>
            </div>
            <div id="qualidadeResumo" class="note"></div>
          </div>
          <div class="card">
            <div class="card-head">
              <div>
                <h3>Metadados da publicacao</h3>
                <p class="sub">Versoes de esquema, cobertura por ano, status da camada TOS e data de atualizacao da publicacao.</p>
              </div>
              <div class="badge-wrap"><span class="flag global">Global</span></div>
            </div>
            <div id="metaPublicacao" class="kpi-grid"></div>
          </div>
        </div>
        <div class="card">
          <div class="card-head">
            <div>
              <h3>Cobertura por ano publicado</h3>
              <p class="sub">Tabela global de cobertura anual da publicacao, com o alerta de que a ultima base disponivel e 2022.</p>
            </div>
            <div class="badge-wrap"><span class="flag global">Global</span></div>
          </div>
          <div class="table-wrap">
            <table id="anosTabela" aria-label="Tabela de cobertura por ano publicado">
              <thead>
                <tr><th>Ano</th><th>Dataset</th><th>ARTs publicadas</th><th>TOS disponivel</th></tr>
              </thead>
              <tbody></tbody>
            </table>
          </div>
        </div>
        <div class="card">__DOCS_HTML__</div>
      </div>
    </section>
  </main>
</div>
<script>
const HIST_MANIFEST = __HIST_MANIFEST__;
const PRECOS = __PRECOS__;
const QUALIDADE = __QUALIDADE__;
const TOS = __TOS__;
const MUNICIPIO_COORDS = __COORDS__;
const BAHIA_OUTLINE = __OUTLINE__;
const INSUF = 'Informacao insuficiente para verificar.';
const cache = new Map();
let dataset = null;

function $(id){ return document.getElementById(id); }
function fmtInt(v){ return new Intl.NumberFormat('pt-BR').format(v || 0); }
function fmtPct(v){ return typeof v === 'number' ? new Intl.NumberFormat('pt-BR',{minimumFractionDigits:1,maximumFractionDigits:1}).format(v) + '%' : INSUF; }
function fmtMoney(v){ return typeof v === 'number' ? new Intl.NumberFormat('pt-BR',{style:'currency',currency:'BRL'}).format(v) : INSUF; }
function fmtDate(v){
  if(!v){ return INSUF; }
  const d = new Date(v);
  return Number.isNaN(d.getTime()) ? v : d.toLocaleString('pt-BR');
}
function selectedValues(id){ return [...$(id).selectedOptions].map((o) => o.value); }
function uniqueSorted(values){ return [...new Set(values)].sort((a,b) => String(a).localeCompare(String(b),'pt-BR')); }
function sanitizeText(value){ return String(value || '').trim(); }

async function loadDataset(file){
  if(cache.has(file)){ return cache.get(file); }
  const resp = await fetch(file, { cache: 'no-store' });
  if(!resp.ok){ throw new Error('Falha ao carregar ' + file); }
  const data = await resp.json();
  cache.set(file, data);
  return data;
}

function populateSelect(id, values){
  const select = $(id);
  select.innerHTML = '';
  values.forEach((value) => {
    const opt = document.createElement('option');
    opt.value = String(value);
    opt.textContent = String(value);
    select.appendChild(opt);
  });
}

function currentYearMeta(){
  const selected = $('ano').value || HIST_MANIFEST.anos[HIST_MANIFEST.anos.length - 1].ano;
  return HIST_MANIFEST.anos.find((item) => item.ano === selected) || HIST_MANIFEST.anos[HIST_MANIFEST.anos.length - 1];
}

function bindTabs(){
  const tabs = [...document.querySelectorAll('.tabs button')];
  function activate(btn){
    tabs.forEach((tab) => {
      const active = tab === btn;
      tab.classList.toggle('active', active);
      tab.setAttribute('aria-selected', active ? 'true' : 'false');
      $(tab.dataset.view).classList.toggle('active', active);
    });
  }
  tabs.forEach((btn, index) => {
    btn.addEventListener('click', () => activate(btn));
    btn.addEventListener('keydown', (event) => {
      if(event.key !== 'ArrowRight' && event.key !== 'ArrowLeft'){ return; }
      event.preventDefault();
      const next = event.key === 'ArrowRight'
        ? tabs[(index + 1) % tabs.length]
        : tabs[(index - 1 + tabs.length) % tabs.length];
      next.focus();
      activate(next);
    });
  });
}

function bindSidebar(){
  populateSelect('ano', HIST_MANIFEST.anos.map((item) => item.ano));
  ['classe','natureza','grupo','servico','municipio'].forEach((id) => $(id).addEventListener('change', applyFilters));
  $('ano').addEventListener('change', loadCurrentDataset);
  $('municipioBusca').addEventListener('input', () => {
    const q = $('municipioBusca').value.toLowerCase();
    [...$('municipio').options].forEach((opt) => {
      opt.hidden = q && !opt.textContent.toLowerCase().includes(q);
    });
  });
  $('limpar').addEventListener('click', () => {
    ['classe','natureza','grupo','servico','municipio'].forEach((id) => {
      [...$(id).options].forEach((opt) => { opt.selected = false; });
    });
    $('municipioBusca').value = '';
    [...$('municipio').options].forEach((opt) => { opt.hidden = false; });
    applyFilters();
  });
}

async function loadCurrentDataset(){
  const meta = currentYearMeta();
  dataset = await loadDataset(meta.arquivo);
  populateSelect('classe', dataset.dimensions.classes || []);
  populateSelect('natureza', dataset.dimensions.naturezas || []);
  populateSelect('grupo', uniqueSorted(dataset.dimensions.grupos_servico || []));
  populateSelect('servico', uniqueSorted(dataset.dimensions.servicos || []));
  populateSelect('municipio', uniqueSorted(dataset.dimensions.municipios || []));
  applyFilters();
}

function activeFilterState(){
  return {
    classes: new Set(selectedValues('classe')),
    naturezas: new Set(selectedValues('natureza')),
    grupos: new Set(selectedValues('grupo')),
    servicos: new Set(selectedValues('servico')),
    municipios: new Set(selectedValues('municipio')),
  };
}

function rowMatches(row, state){
  const dims = dataset.dimensions;
  const classe = dims.classes[row[0]];
  const servico = dims.servicos[row[1]];
  const grupo = dims.grupos_servico[row[1]];
  const municipio = dims.municipios[row[4]];
  const natureza = dims.naturezas[row[5]];
  return (!state.classes.size || state.classes.has(classe))
    && (!state.servicos.size || state.servicos.has(servico))
    && (!state.grupos.size || state.grupos.has(grupo))
    && (!state.municipios.size || state.municipios.has(municipio))
    && (!state.naturezas.size || state.naturezas.has(natureza));
}

function collectMetrics(state){
  const dims = dataset.dimensions;
  const byService = new Map();
  const byMunicipio = new Map();
  const byClasse = new Map();
  let arts = 0;
  let atividades = 0;
  let mapped = 0;
  let official = 0;

  dataset.agg.forEach((row) => {
    if(!rowMatches(row, state)){ return; }
    const count = row[7];
    const acts = row[8];
    const classe = dims.classes[row[0]];
    const servico = dims.servicos[row[1]];
    const grupo = dims.grupos_servico[row[1]];
    const municipio = dims.municipios[row[4]];

    arts += count;
    atividades += acts;
    if(!/^Nao mapeado/.test(servico)){ mapped += count; }
    if(MUNICIPIO_COORDS[municipio]){ official += count; }
    byClasse.set(classe, (byClasse.get(classe) || 0) + count);

    const svc = byService.get(servico) || { servico, grupo, arts: 0, atividades: 0 };
    svc.arts += count;
    svc.atividades += acts;
    byService.set(servico, svc);

    byMunicipio.set(municipio, (byMunicipio.get(municipio) || 0) + count);
  });

  return { arts, atividades, mapped, official, byService, byMunicipio, byClasse };
}

function renderChips(state){
  const chips = ['Ano: ' + currentYearMeta().ano];
  if(state.classes.size){ chips.push('Classes: ' + [...state.classes].join(', ')); }
  if(state.naturezas.size){ chips.push('Naturezas: ' + [...state.naturezas].join(', ')); }
  if(state.grupos.size){ chips.push('Grupos: ' + [...state.grupos].join(', ')); }
  if(state.servicos.size){
    const label = [...state.servicos].slice(0,3).join(', ') + (state.servicos.size > 3 ? '...' : '');
    chips.push('Servicos: ' + label);
  }
  if(state.municipios.size){
    const label = [...state.municipios].slice(0,2).join(', ') + (state.municipios.size > 2 ? '...' : '');
    chips.push('Municipios: ' + label);
  }
  $('chips').innerHTML = chips.map((text) => '<span class="chip">' + text + '</span>').join('');
}

function hasTruncationAlert(){
  return (dataset.limitacoes || []).some((item) => String(item).toLowerCase().includes('trunc'));
}

function renderStatus(metrics){
  const meta = currentYearMeta();
  $('status').textContent =
    'Ultima base disponivel: 2022. Ano carregado: ' + meta.ano +
    '. TOS: ' + sanitizeText(TOS.mensagem || INSUF) +
    '. Arquivo necessario para regeneracao da camada TOS: ' + sanitizeText(TOS.arquivo_necessario_para_regeneracao || INSUF) +
    '. ARTs no recorte ativo: ' + fmtInt(metrics.arts) + '.';
}

function renderKpis(metrics){
  const classeA = metrics.byClasse.get('A') || 0;
  const meta = currentYearMeta();
  const totalBase = meta.total_arts || dataset.resumos.total_arts || 0;
  const cards = [
    ['Ultima base disponivel', '2022', 'Aviso visivel e global da publicacao atual.'],
    ['Periodo do dataset', dataset.periodo.rotulo, 'Recorte temporal declarado no schema do arquivo carregado.'],
    ['ARTs distintas no recorte', fmtInt(metrics.arts), 'Total agregado apos filtros aplicados.'],
    ['Linhas ou atividades', metrics.atividades ? fmtInt(metrics.atividades) : INSUF, 'Contagem agregada de atividades quando o campo existe no dataset.'],
    ['Classe A no recorte', fmtInt(classeA), 'Classe elegivel para leitura monetaria, mas nao prova honorario por si so.'],
    ['Classe A (% do recorte)', metrics.arts ? fmtPct((100 * classeA) / metrics.arts) : INSUF, 'Percentual recalculado com os filtros ativos.'],
    ['Cobertura de mapeamento', metrics.arts ? fmtPct((100 * metrics.mapped) / metrics.arts) : INSUF, 'Percentual de ARTs fora da categoria Nao mapeado.'],
    ['Correspondencia territorial oficial', metrics.arts ? fmtPct((100 * metrics.official) / metrics.arts) : INSUF, 'Percentual de ARTs que entram no mapa por nome oficial.'],
    ['Base publicada do ano', fmtInt(totalBase), 'Total publicado para o ano selecionado, antes de filtrar.'],
  ];
  $('kpis').innerHTML = cards.map(([label, value, note]) => (
    '<div class="kpi"><strong>' + label + '</strong><span>' + value + '</span><small>' + note + '</small></div>'
  )).join('');
}

function renderBars(containerId, descId, items){
  const max = Math.max(...items.map((item) => item.value), 1);
  $(containerId).innerHTML = items.length ? items.map((item) => {
    const width = Math.max(2, (100 * item.value) / max);
    return '<div class="row">' +
      '<div class="label" title="' + item.label + '">' + item.label + '</div>' +
      '<div class="bar" aria-hidden="true"><div class="fill" style="width:' + width + '%"></div></div>' +
      '<div class="value">' + item.display + '</div>' +
    '</div>';
  }).join('') : '<p class="muted">' + INSUF + '</p>';
  if(descId){
    $(descId).textContent = items.length
      ? items.map((item) => item.label + ': ' + item.display).join('. ')
      : INSUF;
  }
}

function renderClasses(metrics){
  const items = (dataset.dimensions.classes || []).map((classe) => ({
    label: classe,
    value: metrics.byClasse.get(classe) || 0,
    display: fmtInt(metrics.byClasse.get(classe) || 0),
  }));
  renderBars('classeBars', 'classeDesc', items);
}

function renderGeneralAlerts(){
  const items = [
    '<div class="warn" role="alert">A ultima base disponivel do painel e 2022. Nao ha atualizacao publica posterior verificada nesta branch.</div>',
    '<div class="warn" role="alert">' + (hasTruncationAlert()
      ? 'O dataset carregado registra suspeita de truncamento na origem para parte da serie historica anterior a 2022. Totais antigos devem ser lidos como minimo observado.'
      : INSUF) + '</div>',
    '<div class="note">A camada TOS esta desabilitada nesta publicacao. Motivo registrado: ' + sanitizeText(TOS.motivo || INSUF) + '</div>',
    '<div class="note">A ART nao e contrato, nota fiscal, recibo ou prova isolada de honorario. A leitura monetaria so existe como evidencia agregada elegivel.</div>',
  ];
  $('alertasGerais').innerHTML = items.join('');
}

function renderDemand(metrics){
  const services = [...metrics.byService.values()].sort((a, b) => b.arts - a.arts).slice(0, 15);
  renderBars('servicoBars', 'servicoDesc', services.map((item) => ({
    label: item.servico,
    value: item.arts,
    display: fmtInt(item.arts),
  })));

  const naoMapeado = services.filter((item) => /^Nao mapeado/.test(item.servico)).reduce((acc, item) => acc + item.arts, 0);
  $('demandaResumo').textContent =
    'ARTs mapeadas no recorte: ' + (metrics.arts ? fmtPct((100 * metrics.mapped) / metrics.arts) : INSUF) +
    '. ARTs em lacunas de mapeamento ou servicos novos: ' + fmtInt(naoMapeado) +
    '. O painel distingue ART, atividade e servico e nao converte automaticamente ambiguidade em certeza.';

  $('servicosTabela').querySelector('tbody').innerHTML = services.length ? services.map((item) => {
    const obs = /^Nao mapeado/.test(item.servico)
      ? 'Lacuna de mapeamento ou diagnostico de demanda preservado sem inventar equivalencia SENGE.'
      : 'Servico agregado sem desambiguar ART composta como verdade unica.';
    return '<tr><td>' + item.servico + '</td><td>' + item.grupo + '</td><td>' + fmtInt(item.arts) + '</td><td>' + fmtInt(item.atividades) + '</td><td>' + obs + '</td></tr>';
  }).join('') : '<tr><td colspan="5">' + INSUF + '</td></tr>';
}

function validMonetaryState(state){
  if(state.municipios.size){
    return 'Nao existe agregado monetario publico pre-calculado por municipio nesta publicacao.';
  }
  if(state.classes.size && !(state.classes.size === 1 && state.classes.has('A'))){
    return 'A visao monetaria so admite Classe A publicada. Qualquer outro filtro de classe sai do espaco elegivel.';
  }
  if(state.naturezas.size && !(state.naturezas.size === 1 && state.naturezas.has('provavel_honorario_tecnico'))){
    return 'A visao monetaria so admite a natureza provavel_honorario_tecnico ja agregada na publicacao.';
  }
  return '';
}

function monetaryRows(state){
  const message = validMonetaryState(state);
  if(message){ return { rows: [], message: INSUF + ' ' + message }; }

  const year = currentYearMeta().ano;
  const datasetId = 'historico-' + year;
  const rows = (PRECOS.rows || []).filter((row) => (
    row.dataset_id === datasetId
    && (!state.servicos.size || state.servicos.has(row.servico))
    && (!state.grupos.size || state.grupos.has(row.grupo))
  ));

  if(!rows.length){
    return { rows: [], message: INSUF + ' Nao existe agregado monetario publico correspondente ao filtro atual.' };
  }

  return {
    rows: rows.sort((a, b) => b.n - a.n || String(a.servico).localeCompare(String(b.servico), 'pt-BR')),
    message: 'Leitura monetaria restrita a agregados publicados com Classe A, natureza provavel honorario tecnico, n minimo e unidade preservada.',
  };
}

function renderMonetary(state){
  const result = monetaryRows(state);
  $('monetariaAviso').textContent = result.message;

  const tbody = $('monetariaTabela').querySelector('tbody');
  if(!result.rows.length){
    tbody.innerHTML = '<tr><td colspan="10">' + INSUF + '</td></tr>';
    $('iqrBars').innerHTML = '<p class="muted">' + INSUF + '</p>';
    $('iqrDesc').textContent = INSUF;
    return;
  }

  tbody.innerHTML = result.rows.map((row) => (
    '<tr><td>' + row.ano + '</td><td>' + row.servico + '</td><td>' + row.grupo + '</td><td>' + row.unidade + '</td><td>' + fmtInt(row.n) + '</td><td>' + fmtMoney(row.mediana) + '</td><td>' + fmtMoney(row.q1) + '</td><td>' + fmtMoney(row.q3) + '</td><td>' + fmtMoney(row.iqr) + '</td><td>' + row.nivel_confianca + '</td></tr>'
  )).join('');

  renderBars('iqrBars', 'iqrDesc', result.rows.slice(0, 12).map((row) => ({
    label: row.servico + ' / ' + row.unidade,
    value: row.iqr,
    display: fmtMoney(row.iqr),
  })));
}

function projectOutline(){
  if(!BAHIA_OUTLINE.length){ return null; }
  const pts = [];
  BAHIA_OUTLINE.forEach((ring) => ring.forEach(([lon, lat]) => pts.push({ lon, lat })));
  const lonMin = Math.min(...pts.map((p) => p.lon));
  const lonMax = Math.max(...pts.map((p) => p.lon));
  const latMin = Math.min(...pts.map((p) => p.lat));
  const latMax = Math.max(...pts.map((p) => p.lat));
  const scaleX = 320 / (lonMax - lonMin || 1);
  const scaleY = 380 / (latMax - latMin || 1);
  function project(lat, lon){
    return [(lon - lonMin) * scaleX + 10, 390 - (lat - latMin) * scaleY];
  }
  const path = BAHIA_OUTLINE.map((ring) => (
    'M' + ring.map(([lon, lat]) => project(lat, lon).map((v) => v.toFixed(1)).join(',')).join('L') + 'Z'
  )).join(' ');
  return { path, project };
}

function renderTerritory(metrics){
  const items = [...metrics.byMunicipio.entries()].sort((a, b) => b[1] - a[1]);
  const positioned = items.filter(([nome]) => MUNICIPIO_COORDS[nome]);
  const unpositioned = items.length - positioned.length;
  $('territorialResumo').textContent =
    'ARTs com correspondencia territorial oficial no recorte: ' +
    (metrics.arts ? fmtPct((100 * metrics.official) / metrics.arts) : INSUF) +
    '. Municipios posicionaveis no mapa: ' + fmtInt(positioned.length) +
    '. Municipios mantidos apenas na lista por falta de correspondencia oficial: ' + fmtInt(unpositioned) + '.';

  $('territorioTabela').querySelector('tbody').innerHTML = items.length ? items.map(([nome, count]) => (
    '<tr><td>' + nome + '</td><td>' + fmtInt(count) + '</td><td>' + (MUNICIPIO_COORDS[nome] ? 'Correspondencia oficial' : 'Sem correspondencia oficial verificavel') + '</td></tr>'
  )).join('') : '<tr><td colspan="3">' + INSUF + '</td></tr>';

  const outline = projectOutline();
  if(!items.length || !outline){
    $('mapa').innerHTML = '<p class="muted">' + INSUF + '</p>';
    $('mapaLegenda').textContent = INSUF;
    return;
  }

  const max = Math.max(...positioned.map(([, count]) => count), 1);
  let svg = '<svg viewBox="0 0 340 400" width="100%" height="400" aria-hidden="true">';
  svg += '<path d="' + outline.path + '" fill="#eef4ee" stroke="#7aa0a5" stroke-width="1.4"></path>';
  positioned.forEach(([nome, count]) => {
    const coord = MUNICIPIO_COORDS[nome];
    const projected = outline.project(coord[0], coord[1]);
    const radius = 2.5 + 8 * Math.sqrt(count / max);
    svg += '<circle cx="' + projected[0].toFixed(1) + '" cy="' + projected[1].toFixed(1) + '" r="' + radius.toFixed(1) + '" fill="rgba(20,108,116,.48)" stroke="#146c74" stroke-width="1.1"><title>' + nome + ': ' + count + ' ARTs</title></circle>';
  });
  svg += '</svg>';
  $('mapa').innerHTML = svg;
  $('mapaLegenda').textContent = 'Tamanho e cor das bolhas representam o volume de ARTs no recorte. Apenas nomes com correspondencia oficial entram no mapa.';
}

function renderQuality(){
  $('qualidadeResumo').textContent =
    'Schema de qualidade: ' + sanitizeText(QUALIDADE.schema_version) +
    '. Publicacao sem microdados: ' + String(QUALIDADE.checks.publicacao_sem_microdados) +
    '. Build deterministico: ' + String(QUALIDADE.checks.build_deterministico) +
    '. Fonte local ainda indisponivel para TOS: ' + sanitizeText(QUALIDADE.fontes_indisponiveis.tos_2022 || INSUF) + '.';

  const metaCards = [
    ['Schema historico', HIST_MANIFEST.schema_version, 'Contrato do manifesto historico publicado.'],
    ['Schema qualidade', QUALIDADE.schema_version, 'Contrato do manifesto de qualidade.'],
    ['Schema TOS', TOS.schema_version, 'Manifesto da camada TOS atualmente desabilitada.'],
    ['Atualizado em', fmtDate(HIST_MANIFEST.gerado_em), 'Data de geracao do manifesto historico.'],
    ['Cobertura anual', (HIST_MANIFEST.cobertura.anos || []).join(', '), 'Anos publicados no painel.'],
    ['Status TOS', sanitizeText(TOS.status || INSUF), 'A camada TOS nao e afirmada como disponivel sem fonte verificavel.'],
  ];
  $('metaPublicacao').innerHTML = metaCards.map(([label, value, note]) => (
    '<div class="kpi"><strong>' + label + '</strong><span style="font-size:20px">' + value + '</span><small>' + note + '</small></div>'
  )).join('');

  $('anosTabela').querySelector('tbody').innerHTML = (HIST_MANIFEST.anos || []).map((item) => (
    '<tr><td>' + item.ano + '</td><td>' + item.dataset_id + '</td><td>' + fmtInt(item.total_arts) + '</td><td>' + (item.tos_disponivel ? 'Sim' : 'Nao') + '</td></tr>'
  )).join('');
}

function applyFilters(){
  if(!dataset){ return; }
  const state = activeFilterState();
  const metrics = collectMetrics(state);
  renderChips(state);
  renderStatus(metrics);
  renderKpis(metrics);
  renderClasses(metrics);
  renderGeneralAlerts();
  renderDemand(metrics);
  renderMonetary(state);
  renderTerritory(metrics);
  renderQuality();
}

bindTabs();
bindSidebar();
loadCurrentDataset().catch((err) => {
  $('status').textContent = 'Falha ao carregar o painel. ' + err.message;
});
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
