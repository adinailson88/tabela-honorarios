# -*- coding: utf-8 -*-
"""Gera uma variante visual institucional do painel TOS.

Entrada: assets/dados_tos_valor_municipio.json (combinado) e assets/anos/*.json
(um agregado por ano). Saida: outputs/dashboard_senge_honorarios_tos_valor_municipio_layout_crea.html
e index.html na raiz (publicado pelo GitHub Pages).

Nao substitui o dashboard validado. A variante reaproveita a logica de
filtros e cautelas metodologicas do painel TOS, mas usa o layout claro
com sidebar inspirado no painel institucional CREA-BA ja existente.

O painel carrega, por padrao, apenas o ano mais recente disponivel em
assets/anos/ (evita embutir todos os anos de uma vez no HTML, o que
travava o navegador). Trocar o filtro de ano busca sob demanda o JSON
correspondente via fetch(); a opcao "Todos os anos" carrega o agregado
combinado (mais pesado) somente quando escolhida explicitamente.
"""
import json
import re
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ASSETS_DIR = REPO / "assets"
ANOS_DIR = ASSETS_DIR / "anos"
DOCS_DIR = REPO / "docs"
DATA_PATH = ASSETS_DIR / "dados_tos_valor_municipio.json"
OUT_PATH = REPO / "outputs" / "dashboard_senge_honorarios_tos_valor_municipio_layout_crea.html"
INDEX_PATH = REPO / "index.html"

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

if not DATA_PATH.exists():
    raise SystemExit(f"Agregado combinado nao encontrado: {DATA_PATH}")


# ---------------------------------------------------------------------------
# Manifesto de anos disponiveis (carregamento sob demanda, ver Problema 1)
# ---------------------------------------------------------------------------

def _rel_web_path(path: Path) -> str:
    return path.resolve().relative_to(REPO.resolve()).as_posix()


def build_anos_manifest() -> list[dict]:
    anos_files = sorted(ANOS_DIR.glob("dados_tos_valor_municipio_*.json"))
    manifest = []
    for path in anos_files:
        m = re.search(r"_(\d{4})\.json$", path.name)
        if not m:
            continue
        ano = m.group(1)
        manifest.append({"value": ano, "label": ano, "file": _rel_web_path(path)})
    manifest.sort(key=lambda item: item["value"])
    if not manifest:
        raise SystemExit(f"Nenhum agregado anual encontrado em {ANOS_DIR}")
    primeiro, ultimo = manifest[0]["value"], manifest[-1]["value"]
    manifest.append(
        {
            "value": "todos",
            "label": f"Todos os anos ({primeiro}-{ultimo}, combinado)",
            "file": _rel_web_path(DATA_PATH),
        }
    )
    return manifest


ANOS_MANIFEST = build_anos_manifest()
DEFAULT_ANO = ANOS_MANIFEST[-2]["value"] if len(ANOS_MANIFEST) >= 2 else ANOS_MANIFEST[0]["value"]
ANOS_MANIFEST_JSON = json.dumps(ANOS_MANIFEST, ensure_ascii=False, separators=(",", ":"))


# ---------------------------------------------------------------------------
# Conversor minimo de Markdown -> HTML para a aba de documentacao (Problema 2)
# Cobre apenas a sintaxe efetivamente usada em docs/*.md: titulos (#, ##),
# paragrafos, listas com "- " e "1. ", codigo `entre crases` e tabelas
# markdown simples (| col | col |). Nao pretende ser um parser generico.
# ---------------------------------------------------------------------------

def _esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _inline(text: str) -> str:
    escaped = _esc(text)
    parts = escaped.split("`")
    if len(parts) % 2 == 0:
        return escaped
    out = []
    for i, part in enumerate(parts):
        out.append(f"<code>{part}</code>" if i % 2 == 1 else part)
    return "".join(out)


_OL_RE = re.compile(r"^\d+\.\s+")


def _render_table(rows: list[str]) -> str:
    cells = [[c.strip() for c in row.strip().strip("|").split("|")] for row in rows]
    header, body = cells[0], cells[1:]
    if body and re.match(r"^[\s:-]+$", "".join(body[0])):
        body = body[1:]
    out = ['<table class="doctable"><thead><tr>']
    out += [f"<th>{_inline(c)}</th>" for c in header]
    out.append("</tr></thead><tbody>")
    for row in body:
        out.append("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in row) + "</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def md_to_html(md_text: str) -> str:
    lines = md_text.splitlines()
    html: list[str] = []
    para: list[str] = []

    def flush_para() -> None:
        if para:
            html.append(f"<p>{_inline(' '.join(para))}</p>")
            para.clear()

    i, n = 0, len(lines)
    while i < n:
        line = lines[i].rstrip()
        if not line.strip():
            flush_para()
            i += 1
            continue
        if line.startswith("## "):
            flush_para()
            html.append(f"<h3>{_inline(line[3:].strip())}</h3>")
            i += 1
            continue
        if line.startswith("# "):
            flush_para()
            html.append(f"<h2>{_inline(line[2:].strip())}</h2>")
            i += 1
            continue
        if line.startswith("- "):
            flush_para()
            items = []
            while i < n and lines[i].startswith("- "):
                items.append(f"<li>{_inline(lines[i][2:].strip())}</li>")
                i += 1
            html.append("<ul>" + "".join(items) + "</ul>")
            continue
        if _OL_RE.match(line):
            flush_para()
            items = []
            while i < n and _OL_RE.match(lines[i]):
                items.append(f"<li>{_inline(_OL_RE.sub('', lines[i]).strip())}</li>")
                i += 1
            html.append("<ol>" + "".join(items) + "</ol>")
            continue
        if line.startswith("|"):
            flush_para()
            table_lines = []
            while i < n and lines[i].startswith("|"):
                table_lines.append(lines[i])
                i += 1
            html.append(_render_table(table_lines))
            continue
        para.append(line.strip())
        i += 1
    flush_para()
    return "\n".join(html)


DOC_FILES = [
    ("metodologia", "Metodologia", "metodologia.md"),
    ("limitacoes", "Limitações", "limitacoes.md"),
    ("fontes", "Fontes", "fontes.md"),
    ("dicionario", "Dicionário de dados", "dicionario-dados.md"),
    ("auditoria", "Auditoria", "auditoria.md"),
]


def build_docs_html() -> str:
    nav = " · ".join(f'<a href="#doc-{key}">{label}</a>' for key, label, _ in DOC_FILES)
    sections = [f'<p class="docnav">{nav}</p>']
    for key, label, filename in DOC_FILES:
        path = DOCS_DIR / filename
        if not path.exists():
            sections.append(
                f'<section class="docsec" id="doc-{key}"><h2>{_inline(label)}</h2>'
                f"<p>{_inline('Informação insuficiente para verificar.')}</p></section>"
            )
            continue
        text = path.read_text(encoding="utf-8")
        sections.append(f'<section class="docsec" id="doc-{key}">{md_to_html(text)}</section>')
    return "\n".join(sections)


DOCS_HTML = build_docs_html()

HTML = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SENGE/BA - Painel TOS, Natureza do Valor e Município</title>
<style>
:root{
  --b950:#061b3a;--b900:#082b58;--b800:#063f7a;--b700:#07579f;--b600:#0b68b5;--b500:#0f7ccf;
  --green:#0f8a5f;--orange:#d96c2c;--red:#b5543e;--amber:#b58900;--gray050:#f8fafc;--gray100:#f1f5f9;
  --gray200:#e2e8f0;--gray300:#cbd5e1;--gray600:#475569;--gray700:#334155;--gray800:#1e293b;
  --card:#fff;--radius:14px;--shadow:0 10px 24px rgba(15,23,42,.10);--soft:0 4px 14px rgba(15,23,42,.08);
  --honor:#0f8a5f;--obra:#d96c2c;--simb:#b58900;--inc:#9a3b3b;--insf:#64748b;
}
*{box-sizing:border-box}
body{margin:0;font-family:Inter,Arial,Helvetica,sans-serif;color:var(--gray800);background:var(--gray100)}
#app{min-height:100vh;background:radial-gradient(circle at 20% 10%,rgba(15,124,207,.14),transparent 30%),linear-gradient(135deg,#f8fafc,#eef4fb 45%,#f8fafc)}
.shell{display:grid;grid-template-columns:292px minmax(0,1fr);min-height:100vh}
.sidebar{background:linear-gradient(180deg,var(--b950),var(--b900) 48%,#073d72);color:#fff;padding:18px;position:sticky;top:0;height:100vh;overflow-y:auto;box-shadow:8px 0 22px rgba(2,6,23,.18);z-index:10}
.brand{display:flex;gap:12px;align-items:center;padding:10px 8px 18px;border-bottom:1px solid rgba(255,255,255,.14);margin-bottom:16px}
.logo{width:54px;height:54px;border-radius:14px;display:grid;place-items:center;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.25);font-weight:900;font-size:18px}
.brand h1{margin:0;font-size:21px;letter-spacing:0}.brand p{margin:5px 0 0;font-size:11px;opacity:.84;line-height:1.2}
.ftitle{font-size:13px;font-weight:800;letter-spacing:.3px;margin:12px 4px 14px;text-transform:uppercase}
.fcard{background:rgba(255,255,255,.97);color:var(--b950);border-radius:12px;padding:10px 12px;margin-bottom:10px;box-shadow:var(--soft)}
.fcard label{display:block;margin-bottom:7px;font-size:12.5px;font-weight:800}
.fcard select,.fcard input{width:100%;border:1px solid var(--gray200);border-radius:10px;background:#fff;color:var(--gray800);padding:9px;font-size:13px;outline:none}
.fcard select[multiple]{height:92px}
.fcard select:focus,.fcard input:focus{border-color:var(--b500);box-shadow:0 0 0 3px rgba(15,124,207,.16)}
.btn{width:100%;margin-top:4px;background:rgba(255,255,255,.12);color:#fff;border:1px solid rgba(255,255,255,.25);border-radius:10px;padding:9px;font-size:13px;font-weight:700;cursor:pointer}
.btn:hover{background:rgba(255,255,255,.2)}
.note{margin-top:16px;border-radius:14px;padding:13px;background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.13);font-size:11.5px;line-height:1.45;color:rgba(255,255,255,.88)}
.note strong{display:block;margin-bottom:6px;color:#fff;font-size:12.5px}
.main{min-width:0;padding:20px 22px 26px}
.head{border-radius:22px;padding:20px 22px;background:linear-gradient(135deg,var(--b950),var(--b800) 58%,#0f5895);color:#fff;display:flex;justify-content:space-between;gap:20px;align-items:flex-start;box-shadow:var(--shadow);margin-bottom:14px}
.head h2{margin:0;font-size:clamp(22px,2.2vw,34px);letter-spacing:0;line-height:1.06}.head p{margin:8px 0 0;opacity:.88;font-size:13.5px}
.hmeta{min-width:210px;text-align:right;font-size:12px;opacity:.94;line-height:1.45}.hmeta strong{display:block;font-size:13px;color:#fff}
.status{margin:0 0 14px;padding:10px 14px;border:1px solid var(--gray200);background:rgba(255,255,255,.86);color:var(--gray700);border-radius:12px;font-size:12.5px;box-shadow:var(--soft)}
.status.warn{border-color:#f59e0b;background:#fffbeb;color:#92400e}
.kpis{display:grid;grid-template-columns:repeat(6,minmax(140px,1fr));gap:12px;margin-bottom:12px}
.kpi{background:var(--card);border:1px solid rgba(148,163,184,.26);border-radius:var(--radius);padding:13px;min-height:104px;box-shadow:var(--soft);display:grid;grid-template-columns:40px 1fr;gap:10px;align-items:center}
.kicon{width:40px;height:40px;border-radius:50%;display:grid;place-items:center;background:linear-gradient(135deg,var(--b900),var(--b600));color:#fff;font-size:15px;font-weight:900;box-shadow:0 6px 14px rgba(7,87,159,.24)}
.ktitle{margin:0 0 6px;font-size:11.5px;color:var(--gray700);font-weight:700}.kval{margin:0;font-size:clamp(20px,2vw,28px);color:var(--b950);font-weight:900;letter-spacing:0;line-height:1.05}
.ksub{margin:5px 0 0;color:var(--gray600);font-size:11px}.kpi.green .kval{color:var(--green)}.kpi.red .kval{color:var(--red)}.kpi.orange .kval{color:var(--orange)}
.grid{display:grid;grid-template-columns:repeat(12,1fr);gap:12px}
.card{background:rgba(255,255,255,.96);border:1px solid rgba(148,163,184,.26);border-radius:var(--radius);box-shadow:var(--soft);padding:14px 16px;min-width:0;position:relative}
.card h3{margin:0 0 4px;color:var(--b950);font-size:14.5px;letter-spacing:0}.card .sub{margin:0 0 10px;color:var(--gray600);font-size:11.5px}
.s3{grid-column:span 3}.s4{grid-column:span 4}.s5{grid-column:span 5}.s6{grid-column:span 6}.s7{grid-column:span 7}.s8{grid-column:span 8}.s12{grid-column:span 12}
.barstack{display:flex;height:28px;border-radius:9px;overflow:hidden;border:1px solid var(--gray200);background:#fff;margin-top:8px}
.barstack span{display:flex;align-items:center;justify-content:center;font-size:11px;color:#061b3a;font-weight:800;white-space:nowrap}
.legend{display:flex;gap:13px;flex-wrap:wrap;margin-top:8px;font-size:12px;color:var(--gray600)}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:5px;vertical-align:middle}
.bars{display:grid;gap:8px;margin-top:10px}
.hbar{display:grid;grid-template-columns:minmax(130px,1fr) minmax(120px,2.3fr) 72px;gap:10px;align-items:center;font-size:12px}
.hbar .label{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:var(--gray700);font-weight:700}
.track{height:16px;background:#e8eef5;border-radius:8px;overflow:hidden;border:1px solid var(--gray200)}
.fill{height:100%;background:linear-gradient(90deg,var(--b700),var(--b500));border-radius:8px}
.value{text-align:right;color:var(--gray600);font-variant-numeric:tabular-nums}
.tablewrap{max-height:520px;overflow:auto;border:1px solid var(--gray200);border-radius:12px;background:#fff}
table{width:100%;border-collapse:collapse;font-size:13px}
th{position:sticky;top:0;background:#f8fafc;color:var(--gray600);font-weight:800;text-align:center;vertical-align:middle;border-bottom:1px solid var(--gray200);padding:8px}
td{border-bottom:1px solid var(--gray200);padding:8px;text-align:center;vertical-align:middle;font-variant-numeric:tabular-nums}
td.txt{text-align:left;font-variant-numeric:normal}.muted{color:var(--gray600)}.small{font-size:12px}
.tag{display:inline-block;font-size:10px;padding:2px 7px;border-radius:20px;border:1px solid var(--gray300);color:var(--gray600);white-space:nowrap}
.tag.new{color:#8a5a00;border-color:#f3c969;background:#fff7d6}.tag.low{color:#b5543e;border-color:#f0b09d;background:#fff0e8}
details summary{cursor:pointer;font-weight:800;color:var(--b950)}
.foot{margin-top:12px;border-radius:12px;background:#eaf2fb;border:1px solid #d8e7f7;color:var(--gray700);padding:10px 12px;font-size:11.5px;line-height:1.4}
.tabs{display:flex;gap:8px;margin-bottom:14px}
.tabbtn{border:1px solid var(--gray200);background:#fff;color:var(--gray700);border-radius:10px;padding:8px 16px;font-size:13px;font-weight:800;cursor:pointer}
.tabbtn.active{background:var(--b900);color:#fff;border-color:var(--b900)}
.tabview{display:none}.tabview.active{display:block}
.linklike{background:none;border:none;color:var(--b600);font-weight:800;cursor:pointer;padding:0;font-size:inherit;text-decoration:underline}
.docnav{font-size:12.5px;margin:0 0 14px}
.docsec{margin-bottom:6px}
.docsec h2{color:var(--b950);font-size:18px;margin:22px 0 8px}
.docsec h3{color:var(--b800);font-size:14.5px;margin:16px 0 6px}
.docsec p{font-size:13px;line-height:1.55;color:var(--gray700);margin:6px 0}
.docsec ul,.docsec ol{font-size:13px;line-height:1.55;color:var(--gray700);margin:6px 0;padding-left:22px}
.doctable{width:100%;border-collapse:collapse;margin:8px 0 14px;font-size:12.5px}
.doctable th,.doctable td{border:1px solid var(--gray200);padding:6px 9px;text-align:left;vertical-align:top}
.doctable th{background:#f8fafc;color:var(--gray700)}
.loading-overlay{position:fixed;inset:0;background:rgba(6,27,58,.55);display:none;align-items:center;justify-content:center;z-index:50}
.loading-overlay.show{display:flex}
.loading-box{background:#fff;padding:18px 28px;border-radius:12px;font-weight:800;color:var(--b950);box-shadow:var(--shadow);font-size:14px}
@media(max-width:1280px){.kpis{grid-template-columns:repeat(3,minmax(150px,1fr))}.s3,.s4,.s5,.s6,.s7,.s8{grid-column:span 6}}
@media(max-width:920px){.shell{grid-template-columns:1fr}.sidebar{position:relative;height:auto}.main{padding:14px}.kpis{grid-template-columns:repeat(2,1fr)}.s3,.s4,.s5,.s6,.s7,.s8,.s12{grid-column:span 12}.head{flex-direction:column}.hmeta{text-align:left}.fcard select[multiple]{height:74px}}
@media(max-width:560px){.kpis{grid-template-columns:1fr}.hbar{grid-template-columns:1fr}.value{text-align:left}.head h2{font-size:22px}}
</style>
</head>
<body>
<div id="app"><div class="shell">
<aside class="sidebar">
  <div class="brand"><div class="logo">BA</div><div><h1>SENGE · CREA-BA</h1><p>TOS, natureza do valor e municípios</p></div></div>
  <div class="ftitle">Ano</div>
  <div class="fcard"><label for="fAno">Ano da base carregada</label><select id="fAno"></select></div>
  <div class="ftitle">Filtros</div>
  <div class="fcard"><label for="fClasse">Classe de confiabilidade</label><select id="fClasse" multiple><option value="A">A - base de cálculo</option><option value="B">B - secundária</option><option value="C">C - só diagnóstico</option><option value="D">D - excluída</option></select></div>
  <div class="fcard"><label for="fNat">Natureza do valor</label><select id="fNat" multiple></select></div>
  <div class="fcard"><label for="fGrupo">Grupo SENGE</label><select id="fGrupo" multiple></select></div>
  <div class="fcard"><label for="fServico">Serviço padronizado</label><select id="fServico" multiple></select></div>
  <div class="fcard"><label for="fGrupoTos">Grupo TOS</label><select id="fGrupoTos" multiple></select></div>
  <div class="fcard"><label for="munSearch">Município</label><input id="munSearch" placeholder="filtrar lista"><select id="fMun" multiple></select></div>
  <button class="btn" id="btnLimpar">Limpar filtros</button>
  <div class="note"><strong>Sobre os dados</strong>Camada TOS com dados agregados. A ART é evidência auxiliar e indireta; valor declarado não é honorário líquido. Mediana e IQR só aparecem para Classe A + provável honorário técnico. Trocar o ano recarrega só o agregado daquele ano.</div>
</aside>
<main class="main">
  <div class="tabs">
    <button class="tabbtn active" data-target="viewPainel">Painel</button>
    <button class="tabbtn" data-target="viewDocs">Documentação</button>
  </div>
  <div id="viewPainel" class="tabview active">
  <header class="head">
    <div><h2>Painel TOS · Natureza do Valor · Município</h2><p>Subsídio técnico para análise orientativa da Tabela de Honorários do SENGE/BA.</p></div>
    <div class="hmeta">Gerado em<strong id="gerado"></strong><span id="fonteCurta">dados locais agregados</span></div>
  </header>
  <div id="status" class="status warn"></div>
  <section class="kpis">
    <div class="kpi"><div class="kicon">ART</div><div><p class="ktitle">ARTs filtradas</p><p class="kval" id="kArts">0</p><p class="ksub" id="kArtsSub">subconjunto TOS</p></div></div>
    <div class="kpi"><div class="kicon">A</div><div><p class="ktitle">Classe A</p><p class="kval" id="kBaseA">0</p><p class="ksub">base de cálculo filtrada</p></div></div>
    <div class="kpi green"><div class="kicon">R$</div><div><p class="ktitle">Base confiável</p><p class="kval" id="kHonor">0</p><p class="ksub">A + provável honorário</p></div></div>
    <div class="kpi green"><div class="kicon">Md</div><div><p class="ktitle">Mediana confiável</p><p class="kval" id="kMed">—</p><p class="ksub">valor em R$ por unidade</p></div></div>
    <div class="kpi"><div class="kicon">IQR</div><div><p class="ktitle">Q1-Q3 confiável</p><p class="kval" id="kIqr" style="font-size:18px">—</p><p class="ksub">faixa interquartil</p></div></div>
    <div class="kpi orange"><div class="kicon">Obr</div><div><p class="ktitle">% obra/contrato</p><p class="kval" id="kObra">—</p><p class="ksub">na seleção atual</p></div></div>
  </section>
  <section class="grid">
    <div class="card s4"><h3>Bucket "Não mapeado"</h3><p class="sub">Mesmo subconjunto TOS: comparação antes/depois.</p><div class="bars" id="barsNaoMapeado"></div></div>
    <div class="card s4"><h3>Natureza do valor declarado</h3><p class="sub">Distribuição da seleção atual.</p><div class="barstack" id="natbar"></div><div class="legend" id="natLegend"></div></div>
    <div class="card s4"><h3>Classes de confiabilidade</h3><p class="sub">Distribuição do subconjunto TOS completo.</p><div class="barstack" id="classbar"></div><div class="legend" id="classLegend"></div></div>
    <div class="card s6"><h3>Top serviços/unidades na base confiável</h3><p class="sub">Classe A + provável honorário técnico; cada unidade de medida forma grupo próprio.</p><div class="bars" id="barsServicos"></div></div>
    <div class="card s6"><h3>Top grupos TOS na seleção</h3><p class="sub">Frequência agregada, independentemente da natureza monetária.</p><div class="bars" id="barsGrupoTos"></div></div>
    <div class="card s12"><h3>Serviços - referência confiável observada</h3><p class="sub">Mediana, Q1, Q3 e IQR em R$ por unidade de medida, apenas para Classe A + provável honorário técnico. n&lt;5 = Informação insuficiente para verificar.</p><div class="tablewrap"><table id="svcTable"><thead><tr><th>Serviço</th><th>Unidade</th><th>Grupo</th><th>n</th><th>Mediana</th><th>Q1</th><th>Q3</th><th>IQR</th><th>Obs.</th></tr></thead><tbody></tbody></table></div></div>
    <div class="card s12"><details open><summary>Metodologia e limitações (resumo)</summary><div class="small muted" style="margin-top:8px">
      <p><b>Premissa central.</b> Os dados de ART são evidência auxiliar, indireta e agregada de escopo, atividade, localidade, responsabilidade técnica e valor declarado, não prova isolada de honorário profissional contratado.</p>
      <p><b>Uso monetário.</b> Mediana e IQR são exibidos apenas para a base confiável: Classe A + provável honorário técnico + n>=5. Classes C/D, valor de obra/contrato, taxa, valor simbólico ou extremo não formam referência de honorário.</p>
      <p><b>Escopo.</b> O agregado carregado contém <span id="escopoTos"></span> ARTs no período exibido, com universo agregado de <span id="escopoUniverso"></span>. Quando o campo TOS não existe na base anual, a classificação TOS é Informação insuficiente para verificar.</p>
      <p><b>Finalidade.</b> Documento de subsídio técnico, orientativo e agregado; não é preço obrigatório, piso, tabela vinculante nem ranking de pessoas ou empresas.</p>
      <p><button type="button" class="linklike" data-goto-docs>Ver documentação completa (metodologia, limitações, fontes, dicionário de dados, auditoria) →</button></p>
    </div></details></div>
    <div class="foot s12">Painel institucional derivado da metodologia validada do projeto tabela-honorarios. Esta variante não depende de internet externa, exceto para buscar o JSON do ano selecionado no próprio repositório.</div>
  </section>
  </div>
  <div id="viewDocs" class="tabview">
    <div class="card s12">
__DOCS_HTML__
    </div>
  </div>
</main>
</div></div>
<div id="loadingOverlay" class="loading-overlay"><div class="loading-box">Carregando dados de <span id="loadingAno"></span>...</div></div>
<script>
const ANOS_MANIFEST = __ANOS_MANIFEST__;
const DEFAULT_ANO = "__DEFAULT_ANO__";
const INSUF='Informação insuficiente para verificar.';
const NAT_LABEL={provavel_honorario_tecnico:'provável honorário técnico',provavel_valor_obra_contrato:'provável obra/contrato',valor_simbolico_ou_taxa:'simbólico/taxa',valor_inconsistente_ou_extremo:'inconsistente/extremo',informacao_insuficiente:'informação insuficiente'};
const NAT_COLOR={provavel_honorario_tecnico:'var(--honor)',provavel_valor_obra_contrato:'var(--obra)',valor_simbolico_ou_taxa:'var(--simb)',valor_inconsistente_ou_extremo:'var(--inc)',informacao_insuficiente:'var(--insf)'};
const CLASS_COLOR={A:'var(--green)',B:'var(--amber)',C:'var(--orange)',D:'var(--gray300)'};
const CLASSES=['A','B','C','D'];
const $=id=>document.getElementById(id);
const fmt=n=>Number.isFinite(Number(n))?Number(n).toLocaleString('pt-BR'):'—';
const pct=(x,t)=>t?(100*x/t).toFixed(1)+'%':'—';
function formatBRL(value){const n=Number(value);if(!Number.isFinite(n))return INSUF;return n.toLocaleString('pt-BR',{style:'currency',currency:'BRL',minimumFractionDigits:2,maximumFractionDigits:2});}
function esc(s){return String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
let D=null, SERV,GRP,UNID,MUN,NAT,GTOS,CC,A,AGG,TOTAL,HON;
const cache=new Map();
function unidadeLabel(u){if(typeof u==='string')return u;return UNID[u]||INSUF;}
function brlUnidade(value,u){return formatBRL(value)+' / '+unidadeLabel(u);}
function bindData(){
  SERV=D.servicos;GRP=D.grupo_de_servico;UNID=D.unidades||[INSUF];MUN=D.municipios;NAT=D.naturezas;GTOS=D.grupos_tos;CC=D.classe_count;
  A=D.classeA;AGG=D.agg;TOTAL=D.total_arts;HON=NAT.indexOf('provavel_honorario_tecnico');
}
function fill(sel,items,valIsIdx){const el=$(sel);items.forEach((t,i)=>{const o=document.createElement('option');o.value=valIsIdx?i:t;o.textContent=t;el.appendChild(o);});}
function selected(id){return new Set([...$(id).selectedOptions].map(o=>isNaN(o.value)?o.value:+o.value));}
function qtiles(arr){if(!arr.length)return null;const a=[...arr].sort((x,y)=>x-y);const p=q=>{const k=(a.length-1)*q,f=Math.floor(k),c=Math.min(f+1,a.length-1);return a[f]+(a[c]-a[f])*(k-f);};return{med:p(.5),q1:p(.25),q3:p(.75),n:a.length};}
function groupServices(groupSet){if(!groupSet.size)return null;const out=new Set();SERV.forEach((_,i)=>{if(groupSet.has(GRP[i]))out.add(i);});return out;}
function filterState(){return{cl:selected('fClasse'),nt:selected('fNat'),gr:selected('fGrupo'),sv:selected('fServico'),gt:selected('fGrupoTos'),mu:selected('fMun')};}
function matchesAgg(r,f,groupSvc){
  return (!f.cl.size||f.cl.has(CLASSES[r[0]]))&&(!f.sv.size||f.sv.has(r[1]))&&(!groupSvc||groupSvc.has(r[1]))&&(!f.mu.size||f.mu.has(r[4]))&&(!f.nt.size||f.nt.has(r[5]))&&(!f.gt.size||f.gt.has(r[6]));
}
function renderBars(id,items,maxVal){
  const el=$(id);el.innerHTML='';
  if(!items.length){el.innerHTML='<div class="small muted">Nenhum registro para a seleção.</div>';return;}
  items.forEach(item=>{
    const row=document.createElement('div');row.className='hbar';
    const width=maxVal?Math.max(2,100*item.value/maxVal):0;
    row.innerHTML='<div class="label" title="'+esc(item.label)+'">'+esc(item.label)+'</div><div class="track"><div class="fill" style="width:'+width+'%"></div></div><div class="value">'+esc(item.display||fmt(item.value))+'</div>';
    el.appendChild(row);
  });
}
function renderStack(id,counts,total,labels,colors){
  const el=$(id);el.innerHTML='';
  if(!total){el.innerHTML='<span style="width:100%;background:var(--gray200)">sem dados</span>';return;}
  labels.forEach(label=>{
    const value=counts[label.key]||0;if(!value)return;
    const w=100*value/total;
    const s=document.createElement('span');s.style.width=w+'%';s.style.background=colors[label.key];s.title=label.label+': '+fmt(value)+' ('+w.toFixed(1)+'%)';s.textContent=w>8?w.toFixed(0)+'%':'';
    el.appendChild(s);
  });
}
function renderLegend(id,labels,colors){
  $(id).innerHTML=labels.map(l=>'<span><i class="dot" style="background:'+colors[l.key]+'"></i>'+esc(l.label)+'</span>').join('');
}
function renderNaoMapeado(){
  const items=[
    {label:'Antes - palavra-chave',value:D.nao_mapeado.old_keyword,display:pct(D.nao_mapeado.old_keyword,TOTAL)},
    {label:'Depois - Código TOS',value:D.nao_mapeado.new_tos,display:pct(D.nao_mapeado.new_tos,TOTAL)},
    {label:'Resíduo - tabela SENGE',value:D.nao_mapeado.new_senge,display:pct(D.nao_mapeado.new_senge,TOTAL)}
  ];
  renderBars('barsNaoMapeado',items,Math.max(...items.map(i=>i.value),1));
}
function renderStatic(){
  $('gerado').textContent=D.gerado_em||INSUF;
  $('fonteCurta').textContent='ARTs locais agregadas';
  $('escopoTos').textContent=fmt(TOTAL);
  const universo=D.universo_total_periodo||D.universo_total_2022;
  $('escopoUniverso').textContent=fmt(universo);
  $('status').textContent='Escopo: agregado '+(D.periodo||'')+' = '+fmt(TOTAL)+' ARTs; universo agregado = '+fmt(universo)+' ARTs. Onde TOS direto não existe, '+INSUF;
  renderNaoMapeado();
  const classLabels=CLASSES.map(c=>({key:c,label:c+' - '+(c==='A'?'base de cálculo':c==='B'?'secundária':c==='C'?'só diagnóstico':'excluída')}));
  renderStack('classbar',CC,CC.A+CC.B+CC.C+CC.D,classLabels,CLASS_COLOR);
  renderLegend('classLegend',classLabels,CLASS_COLOR);
}
function resetDynamicFilterOptions(){
  ['fNat','fGrupo','fServico','fGrupoTos','fMun'].forEach(id=>{$(id).innerHTML='';});
  const grupos=[...new Set(GRP)].sort((a,b)=>a.localeCompare(b,'pt-BR'));fill('fGrupo',grupos,false);
  NAT.forEach((t,i)=>{const o=document.createElement('option');o.value=i;o.textContent=NAT_LABEL[t]||t;$('fNat').appendChild(o);});
  SERV.map((s,i)=>[s,i]).sort((a,b)=>a[0].localeCompare(b[0],'pt-BR')).forEach(([s,i])=>{const o=document.createElement('option');o.value=i;o.textContent=s;$('fServico').appendChild(o);});
  GTOS.map((s,i)=>[s,i]).sort((a,b)=>a[0].localeCompare(b[0],'pt-BR')).forEach(([s,i])=>{const o=document.createElement('option');o.value=i;o.textContent=s;$('fGrupoTos').appendChild(o);});
  MUN.map((s,i)=>[s,i]).sort((a,b)=>a[0].localeCompare(b[0],'pt-BR')).forEach(([s,i])=>{const o=document.createElement('option');o.value=i;o.textContent=s;o.dataset.k=s.toLowerCase();$('fMun').appendChild(o);});
  [...$('fClasse').options].forEach(o=>o.selected=false);
  $('munSearch').value='';
  [...$('fMun').options].forEach(o=>o.hidden=false);
}
function setLoading(isLoading,anoValue){
  const overlay=$('loadingOverlay');
  if(isLoading){const item=ANOS_MANIFEST.find(a=>a.value===anoValue);$('loadingAno').textContent=item?item.label:anoValue;overlay.classList.add('show');}
  else{overlay.classList.remove('show');}
}
async function loadAno(value){
  setLoading(true,value);
  try{
    if(!cache.has(value)){
      const item=ANOS_MANIFEST.find(a=>a.value===value);
      if(!item)throw new Error('ano desconhecido: '+value);
      const resp=await fetch(item.file,{cache:'no-store'});
      if(!resp.ok)throw new Error('HTTP '+resp.status+' ao buscar '+item.file);
      cache.set(value,await resp.json());
    }
    D=cache.get(value);
    bindData();
    resetDynamicFilterOptions();
    renderStatic();
    recompute();
  }catch(err){
    $('status').className='status warn';
    $('status').textContent='Falha ao carregar os dados do ano selecionado. '+INSUF+' Detalhe técnico: '+esc(err.message);
  }finally{
    setLoading(false,value);
  }
}
function initTabs(){
  document.querySelectorAll('.tabbtn').forEach(btn=>btn.addEventListener('click',()=>{
    document.querySelectorAll('.tabbtn').forEach(b=>b.classList.remove('active'));
    document.querySelectorAll('.tabview').forEach(v=>v.classList.remove('active'));
    btn.classList.add('active');
    $(btn.dataset.target).classList.add('active');
  }));
  document.querySelectorAll('[data-goto-docs]').forEach(el=>el.addEventListener('click',()=>{
    document.querySelector('.tabbtn[data-target="viewDocs"]').click();
  }));
}
function initStaticUI(){
  const selAno=$('fAno');
  ANOS_MANIFEST.forEach(a=>{const o=document.createElement('option');o.value=a.value;o.textContent=a.label;selAno.appendChild(o);});
  selAno.value=DEFAULT_ANO;
  selAno.addEventListener('change',e=>loadAno(e.target.value));
  $('munSearch').addEventListener('input',e=>{const q=e.target.value.toLowerCase();[...$('fMun').options].forEach(o=>{o.hidden=q&&!o.dataset.k.includes(q);});});
  ['fClasse','fNat','fGrupo','fServico','fGrupoTos','fMun'].forEach(id=>$(id).addEventListener('change',recompute));
  $('btnLimpar').addEventListener('click',()=>{['fClasse','fNat','fGrupo','fServico','fGrupoTos','fMun'].forEach(id=>[...$(id).options].forEach(o=>o.selected=false));$('munSearch').value='';[...$('fMun').options].forEach(o=>o.hidden=false);recompute();});
  initTabs();
}
function recompute(){
  const f=filterState(), groupSvc=groupServices(f.gr);
  let nArts=0,baseA=0;const natCnt={},gtCnt={};
  for(const r of AGG){if(matchesAgg(r,f,groupSvc)){nArts+=r[7];if(r[0]===0)baseA+=r[7];natCnt[r[5]]=(natCnt[r[5]]||0)+r[7];gtCnt[r[6]]=(gtCnt[r[6]]||0)+r[7];}}
  $('kArts').textContent=fmt(nArts);$('kArtsSub').textContent=fmt(TOTAL)+' no subconjunto TOS';$('kBaseA').textContent=fmt(baseA);
  const aAllowed=!f.cl.size||f.cl.has('A'), honAllowed=!f.nt.size||f.nt.has(HON), blocked=!aAllowed||!honAllowed;
  const bySUnit={};
  if(!blocked){
    for(let i=0;i<A.v.length;i++){
      if(A.nat[i]!==HON)continue;
      const s=A.s[i],u=A.u[i];
      if(/^Nao mapeado/.test(SERV[s]))continue;
      if((f.sv.size&&!f.sv.has(s))||(groupSvc&&!groupSvc.has(s))||(f.mu.size&&!f.mu.has(A.m[i]))||(f.gt.size&&!f.gt.has(A.gt[i])))continue;
      const key=s+'|'+u;
      (bySUnit[key]=bySUnit[key]||{s:s,u:u,vals:[]}).vals.push(A.v[i]);
    }
  }
  const grupos=Object.values(bySUnit), totalHonor=grupos.reduce((acc,g)=>acc+g.vals.length,0);
  const grupoUnico=grupos.length===1?grupos[0]:null;
  const q=grupoUnico?qtiles(grupoUnico.vals):null;
  const unidadeKpi=grupoUnico?grupoUnico.u:(grupos.length?'unidades múltiplas':0);
  $('kHonor').textContent=blocked?'—':fmt(totalHonor);
  $('kMed').textContent=q?brlUnidade(q.med,unidadeKpi):(INSUF+' / '+unidadeLabel(unidadeKpi));
  $('kIqr').textContent=q?(brlUnidade(q.q1,unidadeKpi)+' - '+brlUnidade(q.q3,unidadeKpi)):(INSUF+' / '+unidadeLabel(unidadeKpi));
  const obraIdx=NAT.indexOf('provavel_valor_obra_contrato');$('kObra').textContent=pct(natCnt[obraIdx]||0,nArts);
  const natLabels=NAT.map((name,i)=>({key:i,label:NAT_LABEL[name]||name}));
  const natColors=Object.fromEntries(NAT.map((name,i)=>[i,NAT_COLOR[name]]));
  renderStack('natbar',natCnt,nArts,natLabels,natColors);renderLegend('natLegend',natLabels,natColors);
  const gtItems=Object.entries(gtCnt).map(([k,v])=>({label:GTOS[+k]||INSUF,value:v})).sort((a,b)=>b.value-a.value).slice(0,10);
  renderBars('barsGrupoTos',gtItems,gtItems.length?gtItems[0].value:1);
  renderServiceBarsAndTable(bySUnit,blocked);
}
function renderServiceBarsAndTable(bySUnit,blocked){
  const tb=document.querySelector('#svcTable tbody');tb.innerHTML='';
  if(blocked){tb.innerHTML='<tr><td colspan="9" class="txt muted">Indisponível: a base confiável exige Classe A + natureza provável honorário técnico.</td></tr>';renderBars('barsServicos',[],1);return;}
  const rows=Object.values(bySUnit).map(g=>({s:g.s,u:g.u,vals:g.vals,q:qtiles(g.vals)})).sort((a,b)=>b.vals.length-a.vals.length||SERV[a.s].localeCompare(SERV[b.s],'pt-BR')||unidadeLabel(a.u).localeCompare(unidadeLabel(b.u),'pt-BR'));
  renderBars('barsServicos',rows.slice(0,10).map(r=>({label:SERV[r.s]+' / '+unidadeLabel(r.u),value:r.vals.length})),rows.length?rows[0].vals.length:1);
  if(!rows.length){tb.innerHTML='<tr><td colspan="9" class="txt muted">Nenhum registro confiável para o filtro.</td></tr>';return;}
  rows.forEach(r=>{
    const n=r.vals.length,grp=GRP[r.s],unidade=unidadeLabel(r.u),isNew=/Servi[cç]o novo/.test(grp),low=n<5;
    const obs=(low?'<span class="tag low">n&lt;5</span> ':'')+(isNew?'<span class="tag new">novo</span>':'');
    const tr=document.createElement('tr');
    if(low){tr.innerHTML='<td class="txt">'+esc(SERV[r.s])+'</td><td class="txt">'+esc(unidade)+'</td><td class="txt muted">'+esc(grp)+'</td><td>'+fmt(n)+'</td><td colspan="4" class="muted">'+INSUF+' / '+esc(unidade)+'</td><td>'+obs+'</td>';}
    else{tr.innerHTML='<td class="txt">'+esc(SERV[r.s])+'</td><td class="txt">'+esc(unidade)+'</td><td class="txt muted">'+esc(grp)+'</td><td>'+fmt(n)+'</td><td>'+brlUnidade(r.q.med,r.u)+'</td><td>'+brlUnidade(r.q.q1,r.u)+'</td><td>'+brlUnidade(r.q.q3,r.u)+'</td><td>'+brlUnidade(r.q.q3-r.q.q1,r.u)+'</td><td>'+obs+'</td>';}
    tb.appendChild(tr);
  });
}
initStaticUI();
loadAno(DEFAULT_ANO);
</script>
</body>
</html>"""

out = HTML.replace("__ANOS_MANIFEST__", ANOS_MANIFEST_JSON).replace("__DEFAULT_ANO__", DEFAULT_ANO).replace("__DOCS_HTML__", DOCS_HTML)
OUT_PATH.write_text(out, encoding="utf-8")
INDEX_PATH.write_text(out, encoding="utf-8")
print(f"HTML gerado: {len(out)} chars -> {OUT_PATH.name}")
print(f"HTML publicado localmente: {INDEX_PATH.name}")
print(f"Anos disponiveis para carregamento sob demanda: {[a['value'] for a in ANOS_MANIFEST]}")
print(f"Ano padrao carregado no primeiro acesso: {DEFAULT_ANO}")
