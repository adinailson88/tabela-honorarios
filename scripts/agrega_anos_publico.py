# -*- coding: utf-8 -*-
"""Gera agregados publicos 2015-2022 a partir das planilhas locais de ARTs.

Nao publica linhas de ART, id_art, profissional, empresa ou contratante. O JSON
mantem apenas dimensoes codificadas e valores necessarios ao painel atual.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Tuple

import openpyxl
import xlrd

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from gerar_metodologia_servicos_tos_valor_municipio import (  # noqa: E402
    ABSURDO,
    INSUF,
    INSUF_UNIDADE,
    classify,
    map_servico,
    natureza_base,
    norm_key,
    unidade_segura,
)

DEFAULT_FONTE = Path(r"C:\Users\adina\Meu Drive\ARTS Adinailson")
MIN_N = 5
NAT_ORDER = [
    "provavel_honorario_tecnico",
    "provavel_valor_obra_contrato",
    "valor_simbolico_ou_taxa",
    "valor_inconsistente_ou_extremo",
    "informacao_insuficiente",
]
INSUF_PUBLICO = "Informação insuficiente para verificar."
RE_NIVEL = re.compile(r"Nivel\s*-\s*([^;]+?)\s*(?:Atividade|$)", re.I)
RE_ATIVIDADE = re.compile(r"Atividade\s*-\s*([^-;]+)", re.I)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Agrega bases anuais de ARTs sem publicar linhas.")
    parser.add_argument("--fonte-arts", default=str(DEFAULT_FONTE), help="Diretorio local com planilhas/CSV de ARTs.")
    parser.add_argument("--saida-assets", default=str(REPO / "assets"), help="Diretorio publico de saida.")
    return parser.parse_args()


def parse_valor(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        v = float(value)
        return v if 0 < v <= ABSURDO else None
    text = str(value).strip().replace("R$", "").replace(" ", "")
    if not text:
        return None
    text = re.sub(r"[^0-9,.\-]", "", text)
    if "," in text and "." in text:
        if text.rfind(",") > text.rfind("."):
            text = text.replace(".", "").replace(",", ".")
        else:
            text = text.replace(",", "")
    elif "," in text:
        text = text.replace(".", "").replace(",", ".")
    try:
        v = float(text)
    except ValueError:
        return None
    return v if 0 < v <= ABSURDO else None


def ano_from(value: Any, fallback: int | None) -> str:
    if isinstance(value, dt.datetime):
        return str(value.year)
    if isinstance(value, dt.date):
        return str(value.year)
    match = re.search(r"(20\d{2})", str(value or ""))
    return match.group(1) if match else (str(fallback) if fallback else INSUF_PUBLICO)


def infer_ano_arquivo(path: Path) -> int | None:
    match = re.search(r"20\d{2}", path.name)
    return int(match.group(0)) if match else None


def normaliza_header(values: Iterable[Any]) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for i, value in enumerate(values):
        key = str(value or "").strip().lower()
        if key and key not in out:
            out[key] = i
    return out


def value_at(row: Tuple[Any, ...] | List[Any], idx: Dict[str, int], key: str) -> Any:
    pos = idx.get(key)
    if pos is None or pos >= len(row):
        return None
    return row[pos]


def iter_xlsx(path: Path) -> Tuple[Iterator[Dict[str, Any]], Dict[str, Any]]:
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.worksheets[0]
    rows = ws.iter_rows(values_only=True)
    header = next(rows, ())
    idx = normaliza_header(header)
    meta = {"arquivo": path.name, "aba": ws.title, "ext": path.suffix.lower(), "xls_65536": False, "header": list(idx)}

    def gen() -> Iterator[Dict[str, Any]]:
        try:
            for row in rows:
                if not row or not any(cell not in (None, "") for cell in row):
                    continue
                yield {k: value_at(row, idx, k) for k in idx}
        finally:
            wb.close()

    return gen(), meta


def iter_xls(path: Path) -> Tuple[Iterator[Dict[str, Any]], Dict[str, Any]]:
    wb = xlrd.open_workbook(path, on_demand=True)
    sh = wb.sheet_by_index(0)
    idx = normaliza_header(sh.cell_value(0, c) for c in range(sh.ncols))
    meta = {
        "arquivo": path.name,
        "aba": sh.name,
        "ext": path.suffix.lower(),
        "xls_65536": sh.nrows >= 65536,
        "header": list(idx),
    }

    def cell(row_no: int, key: str) -> Any:
        pos = idx.get(key)
        if pos is None:
            return None
        value = sh.cell_value(row_no, pos)
        if sh.cell_type(row_no, pos) == xlrd.XL_CELL_DATE:
            try:
                return dt.datetime(*xlrd.xldate_as_tuple(value, wb.datemode))
            except Exception:  # noqa: BLE001
                return value
        return value

    def gen() -> Iterator[Dict[str, Any]]:
        try:
            for row_no in range(1, sh.nrows):
                row = {k: cell(row_no, k) for k in idx}
                if not any(v not in (None, "") for v in row.values()):
                    continue
                yield row
        finally:
            wb.release_resources()

    return gen(), meta


def iter_csv(path: Path) -> Tuple[Iterator[Dict[str, Any]], Dict[str, Any]]:
    fh = path.open("r", encoding="utf-8", errors="replace", newline="")
    header = fh.readline().rstrip("\n").split(";")
    meta = {"arquivo": path.name, "aba": path.name, "ext": path.suffix.lower(), "xls_65536": False, "header": header}

    def gen() -> Iterator[Dict[str, Any]]:
        try:
            for line in fh:
                parts = line.rstrip("\n").split(";")
                while parts and parts[-1].strip() == "":
                    parts.pop()
                if len(parts) < 13:
                    yield {
                        "id": parts[0] if len(parts) > 0 else "",
                        "tipo_art": parts[1] if len(parts) > 1 else "",
                        "formaderegistro": parts[2] if len(parts) > 2 else "",
                        "emissao": parts[3] if len(parts) > 3 else "",
                        "cidade_obra": parts[4] if len(parts) > 4 else "",
                        "uf": parts[5] if len(parts) > 5 else "",
                        "titulos": parts[6] if len(parts) > 6 else "",
                        "entidade": "",
                        "codigo": "",
                        "atividade": "",
                        "quantidade": "",
                        "unidade": "",
                        "valor_contrato": "",
                        "ano_registro_profissional": "",
                    }
                    continue
                yield {
                    "id": parts[0] if len(parts) > 0 else "",
                    "tipo_art": parts[1] if len(parts) > 1 else "",
                    "formaderegistro": parts[2] if len(parts) > 2 else "",
                    "emissao": parts[3] if len(parts) > 3 else "",
                    "cidade_obra": parts[4] if len(parts) > 4 else "",
                    "uf": parts[5] if len(parts) > 5 else "",
                    "titulos": parts[6] if len(parts) > 6 else "",
                    "entidade": parts[7] if len(parts) > 7 else "",
                    "codigo": parts[8] if len(parts) > 8 else "",
                    "atividade": " ".join(parts[9 : len(parts) - 4]).strip(),
                    "quantidade": parts[-4],
                    "unidade": parts[-3],
                    "valor_contrato": parts[-2],
                    "ano_registro_profissional": parts[-1],
                }
        finally:
            fh.close()

    return gen(), meta


def arquivos_base(fonte: Path) -> List[Path]:
    out = []
    for path in fonte.iterdir():
        name = path.name.lower()
        if not path.is_file():
            continue
        if name == "arts 2022 01022024.csv":
            out.append(path)
        elif name.startswith("arts 20") and not name.startswith("arts 2022") and path.suffix.lower() in {".xls", ".xlsx"}:
            out.append(path)
    return sorted(out, key=lambda p: (infer_ano_arquivo(p) or 9999, p.name.lower()))


def atividade_categoria(textos: Iterable[str]) -> str:
    counts: Counter[str] = Counter()
    for texto in textos:
        match = RE_ATIVIDADE.search(texto or "")
        if match:
            counts[match.group(1).strip()] += 1
    return counts.most_common(1)[0][0] if counts else ""


def nivel_atividade(textos: Iterable[str]) -> str:
    counts: Counter[str] = Counter()
    for texto in textos:
        match = RE_NIVEL.search(texto or "")
        if match:
            counts[match.group(1).strip()] += 1
    return counts.most_common(1)[0][0] if counts else ""


def municipio_seguro(value: Any) -> str:
    key = norm_key(value)
    if not key or key in {"CPF", "CNPJ", "RG"}:
        return INSUF_PUBLICO
    if re.fullmatch(r"[\d.\-/]+", key):
        return INSUF_PUBLICO
    return key


def add_art(arts: Dict[str, Dict[str, Any]], row: Dict[str, Any], fallback_ano: int | None, source_name: str) -> None:
    art_id = str(row.get("id") or "").strip()
    if not art_id:
        return
    if art_id.endswith(".0"):
        art_id = art_id[:-2]
    ano = ano_from(row.get("emissao"), fallback_ano)
    art_key = f"{ano}:{art_id}"
    valor = parse_valor(row.get("valor_contrato"))
    codigo = str(row.get("codigo") or "").strip()
    atividade = str(row.get("atividade") or "").strip()
    unidade = unidade_segura(row.get("unidade"))
    item = arts.get(art_key)
    if item is None:
        arts[art_key] = {
            "n": 1,
            "val": valor,
            "vary": 0,
            "cods": {codigo} if codigo else set(),
            "ativ": [atividade],
            "uni": [unidade],
            "tipo": str(row.get("tipo_art") or ""),
            "titulo": str(row.get("titulos") or ""),
            "cidade": str(row.get("cidade_obra") or ""),
            "uf": str(row.get("uf") or "").strip().upper(),
            "ano": ano,
            "sources": {source_name},
        }
        return
    item["n"] += 1
    item["sources"].add(source_name)
    if valor is not None:
        if item["val"] is None:
            item["val"] = valor
        elif abs(float(item["val"]) - valor) > 0.005:
            item["vary"] = 1
    if codigo:
        item["cods"].add(codigo)
    item["ativ"].append(atividade)
    item["uni"].append(unidade)
    if not item["ano"] or item["ano"] == INSUF_PUBLICO:
        item["ano"] = ano_from(row.get("emissao"), fallback_ano)


def rows_from_arts(arts: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    classe_count: Counter[str] = Counter()
    for art in arts.values():
        n = art["n"]
        val = art["val"]
        ncods = max(1, len(art["cods"]))
        classe, motivo = classify(n, val, art["vary"], ncods)
        classe_count[classe] += 1
        unidade = Counter(art["uni"]).most_common(1)[0][0] if art["uni"] else INSUF_UNIDADE
        nivel = nivel_atividade(art["ativ"])
        categoria = atividade_categoria(art["ativ"])
        texto_servico = norm_key(" ".join([categoria] + art["ativ"]))
        servico, grupo = map_servico(texto_servico, norm_key(art["tipo"]))
        if servico == "Nao mapeado":
            servico = "Nao mapeado (candidato a novo servico)"
            grupo = INSUF_PUBLICO
        natureza, nat_conf, nat_mot = natureza_base(val, nivel, unidade, [nivel], art["uni"])
        rows.append(
            {
                "ano": art["ano"],
                "municipio_key": municipio_seguro(art["cidade"]),
                "uf": art["uf"],
                "servico_honorarios_padronizado": servico,
                "grupo_servico_honorarios": grupo,
                "unidade_medida": unidade,
                "codigo_tos": INSUF_PUBLICO,
                "grupo_tos": INSUF_PUBLICO,
                "natureza_valor": natureza,
                "confiabilidade_natureza_valor": nat_conf,
                "motivo_natureza_valor": nat_mot,
                "valor_art": val if val is not None else "",
                "classe_confiabilidade": classe,
                "qtd_atividades_art": len(set(x for x in art["ativ"] if x)) or n,
                "motivo_exclusao_calculo": motivo,
            }
        )
    return rows


def pct(vals: List[float], p: float) -> float:
    vals = sorted(vals)
    k = (len(vals) - 1) * p
    f = math.floor(k)
    c = min(f + 1, len(vals) - 1)
    return vals[f] + (vals[c] - vals[f]) * (k - f)


def aplicar_outliers(rows: List[Dict[str, Any]]) -> int:
    vals_by_group: Dict[Tuple[str, str], List[float]] = defaultdict(list)
    for row in rows:
        if row["classe_confiabilidade"] == "A" and row["natureza_valor"] == "provavel_honorario_tecnico":
            value = row["valor_art"]
            if isinstance(value, (int, float)):
                vals_by_group[(row["servico_honorarios_padronizado"], row["unidade_medida"])].append(float(value))
    limits = {}
    for key, vals in vals_by_group.items():
        if len(vals) >= 30:
            q1 = pct(vals, 0.25)
            q3 = pct(vals, 0.75)
            limits[key] = q3 + 3 * (q3 - q1)
    n_out = 0
    for row in rows:
        value = row["valor_art"]
        key = (row["servico_honorarios_padronizado"], row["unidade_medida"])
        limit = limits.get(key)
        if isinstance(value, (int, float)) and limit is not None and value > limit:
            row["natureza_valor"] = "valor_inconsistente_ou_extremo"
            row["motivo_natureza_valor"] = "outlier IQR (> Q3 + 3*IQR) no servico e unidade"
            n_out += 1
    return n_out


def build_public_json(rows: List[Dict[str, Any]], fonte: str, periodo: str) -> Dict[str, Any]:
    svc_list: List[str] = []
    unidade_list: List[str] = []
    mun_list: List[str] = []
    ano_list: List[str] = []
    nat_list: List[str] = []
    gt_list: List[str] = []
    svc_idx: Dict[str, int] = {}
    unidade_idx: Dict[str, int] = {}
    mun_idx: Dict[str, int] = {}
    ano_idx: Dict[str, int] = {}
    nat_idx: Dict[str, int] = {}
    gt_idx: Dict[str, int] = {}
    grp_of: Dict[int, str] = {}

    def gi(lst: List[str], idx: Dict[str, int], key: str) -> int:
        if key not in idx:
            idx[key] = len(lst)
            lst.append(key)
        return idx[key]

    classe_map = {"A": 0, "B": 1, "C": 2, "D": 3}
    classe_count = Counter(row["classe_confiabilidade"] for row in rows)
    natureza_count = Counter(row["natureza_valor"] for row in rows)
    nao_map_senge = sum(1 for row in rows if row["servico_honorarios_padronizado"].startswith("Nao mapeado"))
    c_a = {"s": [], "u": [], "m": [], "a": [], "v": [], "nat": [], "gt": []}
    agg = defaultdict(lambda: [0, 0])

    for row in rows:
        s = gi(svc_list, svc_idx, row["servico_honorarios_padronizado"])
        grp_of[s] = row["grupo_servico_honorarios"]
        u = gi(unidade_list, unidade_idx, row["unidade_medida"])
        m = gi(mun_list, mun_idx, row["municipio_key"])
        a = gi(ano_list, ano_idx, row["ano"])
        nt = gi(nat_list, nat_idx, row["natureza_valor"])
        gt = gi(gt_list, gt_idx, row["grupo_tos"])
        ci = classe_map[row["classe_confiabilidade"]]
        cell = agg[(ci, s, u, a, m, nt, gt)]
        cell[0] += 1
        cell[1] += int(row["qtd_atividades_art"] or 0)
        if row["classe_confiabilidade"] == "A" and isinstance(row["valor_art"], (int, float)):
            c_a["s"].append(s)
            c_a["u"].append(u)
            c_a["m"].append(m)
            c_a["a"].append(a)
            c_a["v"].append(round(float(row["valor_art"]), 2))
            c_a["nat"].append(nt)
            c_a["gt"].append(gt)

    return {
        "gerado_em": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "fonte": fonte,
        "periodo": periodo,
        "total_arts": len(rows),
        "universo_total_periodo": len(rows),
        "universo_total_2022": sum(1 for row in rows if row["ano"] == "2022"),
        "classe_count": {k: classe_count.get(k, 0) for k in ["A", "B", "C", "D"]},
        "nao_mapeado": {"old_keyword": nao_map_senge, "new_tos": len(rows), "new_senge": nao_map_senge, "total_subconjunto": len(rows)},
        "natureza_count": {k: natureza_count.get(k, 0) for k in NAT_ORDER},
        "servicos": svc_list,
        "grupo_de_servico": [grp_of.get(i, "") for i in range(len(svc_list))],
        "unidades": unidade_list,
        "municipios": mun_list,
        "anos": ano_list,
        "naturezas": nat_list,
        "grupos_tos": gt_list,
        "classeA": c_a,
        "agg": [[*key, values[0], values[1]] for key, values in agg.items()],
    }


def write_csv(path: Path, header: List[str], rows: Iterable[Iterable[Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.writer(fh)
        writer.writerow(header)
        writer.writerows(rows)


def write_service_csv(rows: List[Dict[str, Any]], path: Path) -> None:
    groups: Dict[Tuple[str, str], List[float]] = defaultdict(list)
    meta: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for row in rows:
        if row["classe_confiabilidade"] == "A" and row["natureza_valor"] == "provavel_honorario_tecnico":
            value = row["valor_art"]
            if isinstance(value, (int, float)):
                key = (row["servico_honorarios_padronizado"], row["unidade_medida"])
                groups[key].append(float(value))
                meta[key] = {"grupo": row["grupo_servico_honorarios"]}
    out = []
    for (servico, unidade), vals in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        n = len(vals)
        if n >= MIN_N:
            q1 = pct(vals, 0.25)
            med = pct(vals, 0.5)
            q3 = pct(vals, 0.75)
            out.append([servico, unidade, meta[(servico, unidade)]["grupo"], n, round(med, 2), round(q1, 2), round(q3, 2), round(q3 - q1, 2), "media" if n < 30 else "alta"])
        else:
            out.append([servico, unidade, meta[(servico, unidade)]["grupo"], n, INSUF, INSUF, INSUF, INSUF, "insuficiente"])
    write_csv(path, ["servico_honorarios_padronizado", "unidade_medida", "grupo_servico_honorarios", "n_arts", "mediana_valor", "q1", "q3", "iqr", "confiabilidade"], out)


def main() -> int:
    args = parse_args()
    fonte_dir = Path(args.fonte_arts)
    assets_dir = Path(args.saida_assets)
    if not fonte_dir.exists():
        print(f"Fonte nao encontrada: {fonte_dir}")
        return 1

    arts: Dict[str, Dict[str, Any]] = {}
    manifest = []
    for path in arquivos_base(fonte_dir):
        if path.suffix.lower() == ".csv":
            iterator, meta = iter_csv(path)
        elif path.suffix.lower() == ".xls":
            iterator, meta = iter_xls(path)
        else:
            iterator, meta = iter_xlsx(path)
        before = len(arts)
        rows_lidas = 0
        fallback_ano = infer_ano_arquivo(path)
        for row in iterator:
            rows_lidas += 1
            add_art(arts, row, fallback_ano, path.name)
        after = len(arts)
        limitacao = "linhas lidas == limite .xls 65536; possivel truncamento" if meta["xls_65536"] else ""
        manifest.append(
            {
                "ano": fallback_ano or INSUF_PUBLICO,
                "arquivo": path.name,
                "aba": meta["aba"],
                "linhas": rows_lidas,
                "arts_incrementais": after - before,
                "status": "processado",
                "limitacao": limitacao,
                "campos": "; ".join(meta["header"]),
            }
        )
        print(f"lido {path.name} | linhas {rows_lidas} | ARTs novas {after-before} | total {after}")

    rows = rows_from_arts(arts)
    outliers = aplicar_outliers(rows)
    years = sorted({row["ano"] for row in rows})
    assets_dir.mkdir(parents=True, exist_ok=True)
    anos_dir = assets_dir / "anos"
    anos_dir.mkdir(parents=True, exist_ok=True)

    fonte_texto = f"Planilhas anuais locais em {fonte_dir}; TOS direto ausente nas bases anuais, exceto camada TOS 2022 separada."
    combined = build_public_json(rows, fonte_texto, f"{years[0]}-{years[-1]}")
    (assets_dir / "dados_tos_valor_municipio.json").write_text(json.dumps(combined, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    for year in years:
        year_rows = [row for row in rows if row["ano"] == year]
        data = build_public_json(year_rows, fonte_texto, year)
        (anos_dir / f"dados_tos_valor_municipio_{year}.json").write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    write_service_csv(rows, REPO / "agregado_servicos_tos_classe_a_valor_confiavel.csv")
    write_csv(
        REPO / "docs" / "modelos" / "manifesto_bases_anuais_modelo.csv",
        ["ano", "arquivo_origem", "aba_ou_planilha", "caminho_local", "total_linhas", "total_arts_unicas", "campo_art", "campo_municipio", "campo_valor", "campo_tos", "campo_servico", "status_processamento", "observacao"],
        (
            [
                m["ano"],
                m["arquivo"],
                m["aba"],
                str(fonte_dir / m["arquivo"]),
                m["linhas"],
                m["arts_incrementais"],
                "id",
                "cidade_obra",
                "valor_contrato",
                INSUF_PUBLICO,
                "atividade",
                m["status"],
                m["limitacao"] or "TOS direto ausente; agregado por atividade/servico/unidade.",
            ]
            for m in manifest
        ),
    )

    rel = [
        "# Auditoria das bases anuais 2015-2022",
        "",
        f"Gerado em: {dt.datetime.now().isoformat(timespec='seconds')}",
        f"Fonte local: `{fonte_dir}`",
        f"ARTs unicas processadas: {len(rows)}",
        f"Outliers reclassificados por servico/unidade: {outliers}",
        "",
        "| Ano | Arquivo | Linhas lidas | ARTs novas | Limitacao |",
        "|---:|---|---:|---:|---|",
    ]
    for m in manifest:
        rel.append(f"| {m['ano']} | {m['arquivo']} | {m['linhas']} | {m['arts_incrementais']} | {m['limitacao'] or 'TOS direto ausente nas bases anuais.'} |")
    rel.append("")
    rel.append("Os arquivos publicos gerados estao em `assets/dados_tos_valor_municipio.json` e `assets/anos/`. Nenhuma base linha a linha foi gravada.")
    (REPO / "relatorios").mkdir(exist_ok=True)
    (REPO / "relatorios" / "auditoria_bases_anuais.md").write_text("\n".join(rel) + "\n", encoding="utf-8")

    print("OK agregado anual publico")
    print("anos:", ", ".join(years))
    print("arts:", len(rows), "| classeA:", len(combined["classeA"]["v"]), "| unidades:", len(combined["unidades"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
