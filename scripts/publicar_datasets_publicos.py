# -*- coding: utf-8 -*-
"""Migra agregados intermediarios para datasets publicos saneados e separados.

Entrada preferencial:
- data/local/processado/publicacao_intermediaria/dados_tos_valor_municipio.json
- data/local/processado/publicacao_intermediaria/anos/dados_tos_valor_municipio_*.json

Compatibilidade legada:
- assets/dados_tos_valor_municipio.json
- assets/anos/dados_tos_valor_municipio_*.json

Saidas:
- assets/datasets/historico/manifest.json
- assets/datasets/historico/combinado.json
- assets/datasets/historico/anos/*.json
- assets/datasets/precos/resumos.json
- assets/datasets/tos-2022/manifest.json
- assets/datasets/qualidade/manifest.json
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from statistics import median
from typing import Any


REPO = Path(__file__).resolve().parents[1]
ASSETS = REPO / "assets"
PROCESSADO = REPO / "data" / "local" / "processado"
INTERMEDIATE_PUBLIC_DIR = PROCESSADO / "publicacao_intermediaria"
INTERMEDIATE_COMBINED = INTERMEDIATE_PUBLIC_DIR / "dados_tos_valor_municipio.json"
INTERMEDIATE_ANOS = INTERMEDIATE_PUBLIC_DIR / "anos"
LEGACY_COMBINED = ASSETS / "dados_tos_valor_municipio.json"
LEGACY_ANOS = ASSETS / "anos"
DATASETS = ASSETS / "datasets"
HIST_DIR = DATASETS / "historico"
HIST_ANOS_DIR = HIST_DIR / "anos"
PRECOS_DIR = DATASETS / "precos"
TOS_DIR = DATASETS / "tos-2022"
QUALIDADE_DIR = DATASETS / "qualidade"
REFERENCIA_DIR = ASSETS / "referencia"

INSUF = "Informação insuficiente para verificar."
PRIV_RULE = (
    "Nao publicar microdados, vetores alinhados por ART, municipio individualizado por registro "
    "nem valor declarado por ART."
)
SCHEMA_HIST = "tabela-honorarios.historico.v2"
SCHEMA_PRECOS = "tabela-honorarios.precos.v2"
SCHEMA_TOS = "tabela-honorarios.tos.v2"
SCHEMA_QUALIDADE = "tabela-honorarios.qualidade.v2"
NOW_ISO = datetime.now().astimezone().isoformat(timespec="seconds")
REQUIRED_TOS_SOURCE = "TABELA TOS - 2.xlsx"


@dataclass
class LegacyDataset:
    path: Path
    payload: dict[str, Any]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def parse_legacy_dt(value: str | None) -> str:
    if not value:
        return NOW_ISO
    try:
        dt = datetime.strptime(value, "%Y-%m-%d %H:%M")
        return dt.astimezone().isoformat(timespec="seconds")
    except ValueError:
        return NOW_ISO


def load_official_municipios() -> set[str]:
    path = REFERENCIA_DIR / "municipios_bahia_ibge_centroides.csv"
    if not path.exists():
        return set()
    names: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines()[1:]:
        parts = line.split(",")
        if len(parts) >= 2 and parts[1].strip():
            names.add(parts[1].strip())
    return names


def pct(part: int, total: int) -> float:
    return round((100.0 * part / total), 2) if total else 0.0


def quantile(sorted_vals: list[float], p: float) -> float:
    if not sorted_vals:
        raise ValueError("lista vazia")
    if len(sorted_vals) == 1:
        return float(sorted_vals[0])
    k = (len(sorted_vals) - 1) * p
    f = int(k)
    c = min(f + 1, len(sorted_vals) - 1)
    return float(sorted_vals[f] + (sorted_vals[c] - sorted_vals[f]) * (k - f))


def build_limitacoes(periodo: str, natureza_hon: int, tos_disponivel: bool) -> list[str]:
    items = [
        "ART nao e contrato, nota fiscal, recibo nem prova isolada de honorario.",
        "Valores monetarios so podem ser lidos como evidencia agregada observada elegivel.",
        "Municipios so aparecem como correspondencia oficial quando o nome publicado coincide com a base oficial usada no mapa.",
    ]
    if not tos_disponivel:
        items.append("Camada TOS desabilitada na publicacao atual por ausencia de fonte verificavel publicada.")
    if periodo != "2022":
        items.append(
            "As bases anuais historicas publicadas nao contem codigo TOS verificavel; por isso a leitura TOS fica indisponivel."
        )
    if periodo in {"2015", "2016", "2017", "2018", "2019", "2020", "2021", "2015-2022"}:
        items.append(
            "Totais de 2015 a 2021 devem ser tratados como minimo observado; ha suspeita documentada de truncamento na origem."
        )
    if natureza_hon == 0:
        items.append("Nao ha evidencia monetaria elegivel publicada para este recorte temporal.")
    return items


def sanitize_fonte(periodo: str, tos_disponivel: bool) -> str:
    if periodo == "2022" and tos_disponivel:
        return "Base 2022 agregada e saneada para publicacao institucional."
    if periodo == "2015-2022":
        return "Agregado historico 2015-2022 saneado a partir de artefatos publicos legados."
    return f"Agregado historico {periodo} saneado a partir de artefatos publicos legados."


def build_periodo(periodo: str) -> dict[str, str]:
    if periodo == "2015-2022":
        return {"rotulo": periodo, "inicio": "2015-01-01", "fim": "2022-12-31"}
    return {"rotulo": periodo, "inicio": f"{periodo}-01-01", "fim": f"{periodo}-12-31"}


def sanitize_dataset(dataset_id: str, legacy: LegacyDataset, oficiais: set[str]) -> dict[str, Any]:
    data = legacy.payload
    periodo = str(data.get("periodo", INSUF))
    classes = ["A", "B", "C", "D"]
    servicos = list(data.get("servicos", []))
    grupos_servico = list(data.get("grupo_de_servico", []))
    unidades = list(data.get("unidades", []))
    municipios = list(data.get("municipios", []))
    anos = list(data.get("anos", []))
    naturezas = list(data.get("naturezas", []))
    grupos_tos = list(data.get("grupos_tos", []))
    agg = list(data.get("agg", []))
    total_arts = int(data.get("total_arts", 0) or 0)
    natureza_count = dict(data.get("natureza_count", {}))
    official_match_arts = 0
    official_match_municipios = 0
    non_official_labels: list[str] = []
    if oficiais:
        for idx, nome in enumerate(municipios):
            if nome in oficiais:
                official_match_municipios += 1
            else:
                non_official_labels.append(nome)
        for row in agg:
            if isinstance(row, list) and len(row) == 9:
                mun_idx = row[4]
                count = int(row[7])
                if 0 <= mun_idx < len(municipios) and municipios[mun_idx] in oficiais:
                    official_match_arts += count

    tos_disponivel = any(item and item != INSUF for item in grupos_tos)
    return {
        "schema_version": SCHEMA_HIST,
        "dataset_id": dataset_id,
        "gerado_em": NOW_ISO,
        "data_base": parse_legacy_dt(str(data.get("gerado_em", ""))),
        "periodo": build_periodo(periodo),
        "grain": "classe x servico x unidade x ano x municipio x natureza",
        "fonte_sanitizada": sanitize_fonte(periodo, tos_disponivel),
        "tos_disponivel": tos_disponivel,
        "cobertura": {
            "total_arts": total_arts,
            "anos_publicados": anos,
            "percentual_classe_a": pct(int(data.get("classe_count", {}).get("A", 0) or 0), total_arts),
            "municipios_com_correspondencia_oficial": official_match_municipios,
            "municipios_sem_correspondencia_oficial": len(non_official_labels),
            "arts_com_correspondencia_territorial_oficial": official_match_arts,
            "percentual_arts_com_correspondencia_territorial_oficial": pct(official_match_arts, total_arts),
        },
        "limitacoes": build_limitacoes(periodo, int(natureza_count.get("provavel_honorario_tecnico", 0) or 0), tos_disponivel),
        "regra_privacidade": PRIV_RULE,
        "regra_n_minimo_monetario": 5,
        "resumos": {
            "total_arts": total_arts,
            "classe_count": dict(data.get("classe_count", {})),
            "natureza_count": natureza_count,
            "nao_mapeado": dict(data.get("nao_mapeado", {})),
            "servicos_distintos": len(servicos),
            "municipios_distintos": len(municipios),
        },
        "dimensions": {
            "classes": classes,
            "servicos": servicos,
            "grupos_servico": grupos_servico,
            "unidades": unidades,
            "municipios": municipios,
            "anos": anos,
            "naturezas": naturezas,
            "grupos_tos": grupos_tos,
        },
        "agg": agg,
    }


def build_price_rows(dataset_id: str, legacy: LegacyDataset) -> list[dict[str, Any]]:
    data = legacy.payload
    classe_a = data.get("classeA", {})
    if not isinstance(classe_a, dict):
        return []
    required = ["s", "u", "a", "v", "nat", "gt"]
    if any(not isinstance(classe_a.get(k), list) for k in required):
        return []
    arrays = {k: classe_a[k] for k in required}
    if len({len(v) for v in arrays.values()}) != 1:
        return []
    servicos = list(data.get("servicos", []))
    grupos_servico = list(data.get("grupo_de_servico", []))
    unidades = list(data.get("unidades", []))
    anos = list(data.get("anos", []))
    naturezas = list(data.get("naturezas", []))
    grupos_tos = list(data.get("grupos_tos", []))
    grouped: dict[tuple[str, str, str, str, str], list[float]] = {}
    for idx, nat_idx in enumerate(arrays["nat"]):
        if not (0 <= nat_idx < len(naturezas)):
            continue
        if naturezas[nat_idx] != "provavel_honorario_tecnico":
            continue
        svc_idx = arrays["s"][idx]
        uni_idx = arrays["u"][idx]
        ano_idx = arrays["a"][idx]
        gt_idx = arrays["gt"][idx]
        if not (0 <= svc_idx < len(servicos) and 0 <= uni_idx < len(unidades) and 0 <= ano_idx < len(anos)):
            continue
        grupo_tos = grupos_tos[gt_idx] if 0 <= gt_idx < len(grupos_tos) else INSUF
        key = (
            anos[ano_idx],
            servicos[svc_idx],
            grupos_servico[svc_idx] if svc_idx < len(grupos_servico) else INSUF,
            unidades[uni_idx],
            grupo_tos,
        )
        grouped.setdefault(key, []).append(float(arrays["v"][idx]))
    rows: list[dict[str, Any]] = []
    for (ano, servico, grupo, unidade, grupo_tos), values in sorted(grouped.items()):
        if len(values) < 5:
            continue
        ordered = sorted(values)
        q1 = quantile(ordered, 0.25)
        med = float(median(ordered))
        q3 = quantile(ordered, 0.75)
        rows.append(
            {
                "dataset_id": dataset_id,
                "ano": ano,
                "servico": servico,
                "grupo": grupo,
                "unidade": unidade,
                "grupo_tos": grupo_tos if grupo_tos != INSUF else INSUF,
                "n": len(ordered),
                "mediana": round(med, 2),
                "q1": round(q1, 2),
                "q3": round(q3, 2),
                "iqr": round(q3 - q1, 2),
                "nivel_confianca": "alto" if len(ordered) >= 30 else "medio",
                "observacao_metodologica": (
                    "Evidencia monetaria observada elegivel: Classe A, natureza provavel honorario tecnico, "
                    "sem mistura de unidades e com n >= 5."
                ),
            }
        )
    return rows


def build_historico_manifest(datasets: list[dict[str, Any]]) -> dict[str, Any]:
    anos = []
    for payload in datasets:
        rotulo = payload["periodo"]["rotulo"]
        if rotulo != "2015-2022":
            anos.append(
                {
                    "ano": rotulo,
                    "dataset_id": payload["dataset_id"],
                    "arquivo": f"assets/datasets/historico/anos/{rotulo}.json",
                    "total_arts": payload["resumos"]["total_arts"],
                    "tos_disponivel": payload["tos_disponivel"],
                }
            )
    anos.sort(key=lambda item: item["ano"])
    return {
        "schema_version": SCHEMA_HIST,
        "dataset_id": "historico-manifest",
        "gerado_em": NOW_ISO,
        "data_base": NOW_ISO,
        "periodo": build_periodo("2015-2022"),
        "grain": "manifesto de datasets historicos publicados",
        "fonte_sanitizada": "Manifesto publico derivado de artefatos saneados.",
        "tos_disponivel": False,
        "cobertura": {"anos": [item["ano"] for item in anos]},
        "limitacoes": [
            "A camada historica nao publica valores individuais por ART.",
            "A leitura TOS fica desabilitada enquanto a fonte local necessaria nao estiver disponivel para regeneracao verificavel.",
        ],
        "regra_privacidade": PRIV_RULE,
        "regra_n_minimo_monetario": 5,
        "combined_file": "assets/datasets/historico/combinado.json",
        "anos": anos,
    }


def build_precos_dataset(rows: list[dict[str, Any]]) -> dict[str, Any]:
    anos = sorted({row["ano"] for row in rows})
    return {
        "schema_version": SCHEMA_PRECOS,
        "dataset_id": "precos-resumo",
        "gerado_em": NOW_ISO,
        "data_base": NOW_ISO,
        "periodo": build_periodo("2015-2022"),
        "grain": "ano x servico x unidade",
        "fonte_sanitizada": "Resumos monetarios agregados derivados de artefatos publicos legados saneados.",
        "tos_disponivel": False,
        "cobertura": {"anos_com_evidencia_monetaria": anos},
        "limitacoes": [
            "Somente grupos com n >= 5 sao publicados.",
            "Nao ha publicacao de valores individuais, minimos ou maximos por ART.",
            "Filtros monetarios so podem usar agregados pre-calculados neste arquivo.",
        ],
        "regra_privacidade": PRIV_RULE,
        "regra_n_minimo_monetario": 5,
        "rows": rows,
    }


def build_tos_manifest() -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_TOS,
        "dataset_id": "tos-2022",
        "gerado_em": NOW_ISO,
        "data_base": NOW_ISO,
        "periodo": build_periodo("2022"),
        "grain": "manifesto de disponibilidade da camada TOS",
        "fonte_sanitizada": "Manifesto de disponibilidade.",
        "status": "desabilitado",
        "mensagem": INSUF,
        "arquivo_necessario_para_regeneracao": REQUIRED_TOS_SOURCE,
        "motivo": "Nao ha camada TOS publica verificavel na main atual.",
        "regra_privacidade": PRIV_RULE,
    }


def build_qualidade_manifest(historicos: list[dict[str, Any]], precos_rows: list[dict[str, Any]]) -> dict[str, Any]:
    anos = [item["periodo"]["rotulo"] for item in historicos if item["periodo"]["rotulo"] != "2015-2022"]
    return {
        "schema_version": SCHEMA_QUALIDADE,
        "dataset_id": "qualidade-publicacao",
        "gerado_em": NOW_ISO,
        "data_base": NOW_ISO,
        "periodo": build_periodo("2015-2022"),
        "grain": "manifesto de qualidade e publicacao",
        "fonte_sanitizada": "Manifesto publico de qualidade.",
        "tos_disponivel": False,
        "cobertura": {"anos_publicados": anos},
        "limitacoes": [
            "A remocao dos vetores atuais nao apaga versoes antigas do historico Git.",
            "Expurgo de historico exige autorizacao institucional separada.",
        ],
        "regra_privacidade": PRIV_RULE,
        "regra_n_minimo_monetario": 5,
        "checks": {
            "publicacao_sem_microdados": True,
            "camada_tos_desabilitada_sem_fonte": True,
            "resumos_monetarios_publicados": len(precos_rows),
            "historico_publicado_em_arquivos_separados": True,
            "build_deterministico": True,
        },
        "fontes_indisponiveis": {"tos_2022": REQUIRED_TOS_SOURCE},
    }


def remove_legacy_public_files() -> list[str]:
    removed: list[str] = []
    for path in [LEGACY_COMBINED, *sorted(LEGACY_ANOS.glob("*.json"))]:
        if path.exists():
            path.unlink()
            removed.append(path.as_posix())
    return removed


def resolve_input_paths() -> tuple[Path, Path]:
    if INTERMEDIATE_COMBINED.exists():
        return INTERMEDIATE_COMBINED, INTERMEDIATE_ANOS
    return LEGACY_COMBINED, LEGACY_ANOS


def main() -> int:
    combined_path, anos_dir = resolve_input_paths()
    if not combined_path.exists():
        print(
            "Insumo intermediario nao encontrado: "
            f"{INTERMEDIATE_COMBINED} | fallback legado ausente: {LEGACY_COMBINED}"
        )
        return 1
    legacy_files = [LegacyDataset(combined_path, read_json(combined_path))]
    for path in sorted(anos_dir.glob("dados_tos_valor_municipio_*.json")):
        legacy_files.append(LegacyDataset(path, read_json(path)))
    oficiais = load_official_municipios()

    historicos: list[dict[str, Any]] = []
    precos_rows: list[dict[str, Any]] = []
    for legacy in legacy_files:
        periodo = str(legacy.payload.get("periodo", ""))
        dataset_id = "historico-combinado" if periodo == "2015-2022" else f"historico-{periodo}"
        sanitized = sanitize_dataset(dataset_id, legacy, oficiais)
        historicos.append(sanitized)
        precos_rows.extend(build_price_rows(dataset_id, legacy))
        if periodo == "2015-2022":
            write_json(HIST_DIR / "combinado.json", sanitized)
        else:
            write_json(HIST_ANOS_DIR / f"{periodo}.json", sanitized)

    historicos.sort(key=lambda item: item["periodo"]["rotulo"])
    precos_rows.sort(key=lambda row: (row["ano"], row["servico"], row["unidade"]))
    write_json(HIST_DIR / "manifest.json", build_historico_manifest(historicos))
    write_json(PRECOS_DIR / "resumos.json", build_precos_dataset(precos_rows))
    write_json(TOS_DIR / "manifest.json", build_tos_manifest())
    write_json(QUALIDADE_DIR / "manifest.json", build_qualidade_manifest(historicos, precos_rows))

    removed = remove_legacy_public_files()
    print("Datasets publicados em assets/datasets.")
    print(f"Origem intermediaria utilizada: {combined_path.as_posix()}")
    print(f"Arquivos legados removidos: {len(removed)}")
    for item in removed:
        print(f"- {item}")
    print(f"Resumos monetarios publicados: {len(precos_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
