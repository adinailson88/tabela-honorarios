# -*- coding: utf-8 -*-
r"""Valida todos os JSONs publicos versionados.

Falha com codigo diferente de zero quando detecta:
- vetores individualizados (`classeA`, `valor_art`, `id_art`);
- caminhos locais `C:\Users\...`;
- esquema ausente;
- `n < 5` em estatistica monetaria publicada;
- indices fora das dimensoes em datasets historicos;
- reconciliacao basica incompatível.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
ASSETS_DIR = REPO / "assets"
DEFAULT_SAIDA = REPO / "relatorios" / "validacao_json_publico.md"
SCHEMAS_OK = {
    "tabela-honorarios.historico.v2",
    "tabela-honorarios.precos.v2",
    "tabela-honorarios.tos.v2",
    "tabela-honorarios.qualidade.v2",
}
BLOCKED_PATTERNS = [
    re.compile(r"classeA"),
    re.compile(r"\bid_art\b", re.IGNORECASE),
    re.compile(r"\bvalor_art\b", re.IGNORECASE),
    re.compile(r"cpf", re.IGNORECASE),
    re.compile(r"cnpj", re.IGNORECASE),
    re.compile(r"contratante", re.IGNORECASE),
    re.compile(r"profissional", re.IGNORECASE),
    re.compile(r"C:\\Users\\", re.IGNORECASE),
]


def scan_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.json") if path.is_file())


def add_issue(issues: list[str], relpath: str, msg: str) -> None:
    issues.append(f"- `{relpath}`: {msg}")


def validate_historico(payload: dict[str, Any], relpath: str, issues: list[str]) -> None:
    if payload.get("dataset_id") == "historico-manifest":
        if not isinstance(payload.get("anos"), list):
            add_issue(issues, relpath, "`anos` ausente ou invalido no manifesto historico.")
        if not payload.get("combined_file"):
            add_issue(issues, relpath, "`combined_file` ausente no manifesto historico.")
        return
    dims = payload.get("dimensions", {})
    if not isinstance(dims, dict):
        add_issue(issues, relpath, "`dimensions` ausente ou invalido.")
        return
    required_dims = ["classes", "servicos", "grupos_servico", "unidades", "municipios", "anos", "naturezas", "grupos_tos"]
    for key in required_dims:
        if not isinstance(dims.get(key), list):
            add_issue(issues, relpath, f"dimensao `{key}` ausente ou invalida.")
    agg = payload.get("agg")
    if not isinstance(agg, list):
        add_issue(issues, relpath, "`agg` ausente ou invalido.")
        return
    counts = payload.get("resumos", {}).get("classe_count", {})
    total_arts = int(payload.get("resumos", {}).get("total_arts", 0) or 0)
    if isinstance(counts, dict):
        soma = sum(int(v or 0) for v in counts.values())
        if total_arts and soma != total_arts:
            add_issue(issues, relpath, f"`classe_count` ({soma}) nao fecha com `total_arts` ({total_arts}).")
    dims_sizes = {
        0: len(dims.get("classes", [])),
        1: len(dims.get("servicos", [])),
        2: len(dims.get("unidades", [])),
        3: len(dims.get("anos", [])),
        4: len(dims.get("municipios", [])),
        5: len(dims.get("naturezas", [])),
        6: len(dims.get("grupos_tos", [])),
    }
    for idx, row in enumerate(agg):
        if not isinstance(row, list) or len(row) != 9:
            add_issue(issues, relpath, f"`agg[{idx}]` nao possui 9 campos.")
            break
        for pos, size in dims_sizes.items():
            value = row[pos]
            if not isinstance(value, int) or value < 0 or value >= size:
                add_issue(issues, relpath, f"`agg[{idx}][{pos}]` fora da dimensao correspondente.")
                return
        if not isinstance(row[7], int) or row[7] < 0:
            add_issue(issues, relpath, f"`agg[{idx}][7]` deve ser inteiro nao negativo.")
            return


def validate_precos(payload: dict[str, Any], relpath: str, issues: list[str]) -> None:
    rows = payload.get("rows")
    if not isinstance(rows, list):
        add_issue(issues, relpath, "`rows` ausente ou invalido.")
        return
    for idx, row in enumerate(rows):
        if not isinstance(row, dict):
            add_issue(issues, relpath, f"`rows[{idx}]` invalida.")
            return
        n = row.get("n")
        if not isinstance(n, int) or n < 5:
            add_issue(issues, relpath, f"`rows[{idx}]` publica estatistica monetaria com `n < 5`.")
            return
        for key in ["mediana", "q1", "q3", "iqr"]:
            value = row.get(key)
            if not isinstance(value, (int, float)):
                add_issue(issues, relpath, f"`rows[{idx}].{key}` ausente ou invalido.")
                return


def validate_file(path: Path, issues: list[str], infos: list[str]) -> None:
    relpath = path.resolve().relative_to(REPO.resolve()).as_posix()
    text = path.read_text(encoding="utf-8")
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        add_issue(issues, relpath, f"JSON invalido: {exc}")
        return
    schema = payload.get("schema_version")
    dataset_id = payload.get("dataset_id")
    infos.append(f"- `{relpath}` | schema=`{schema}` | dataset_id=`{dataset_id}`")
    if schema not in SCHEMAS_OK:
        add_issue(issues, relpath, "schema ausente, desconhecido ou sem versao.")
    if not dataset_id:
        add_issue(issues, relpath, "`dataset_id` ausente.")
    for pattern in BLOCKED_PATTERNS:
        if pattern.search(text):
            add_issue(issues, relpath, f"conteudo bloqueado detectado por `{pattern.pattern}`.")
            break
    if schema == "tabela-honorarios.historico.v2":
        validate_historico(payload, relpath, issues)
    elif schema == "tabela-honorarios.precos.v2":
        validate_precos(payload, relpath, issues)


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida todos os JSONs publicos publicados em assets/.")
    parser.add_argument("--root", default=str(ASSETS_DIR), help="Raiz dos artefatos publicos.")
    parser.add_argument("--saida", default=str(DEFAULT_SAIDA), help="Arquivo Markdown de saida.")
    args = parser.parse_args()

    root = Path(args.root)
    saida = Path(args.saida)
    saida.parent.mkdir(parents=True, exist_ok=True)

    files = scan_files(root)
    issues: list[str] = []
    infos: list[str] = []
    for path in files:
        validate_file(path, issues, infos)

    lines = [
        "# Validacao dos JSONs publicos",
        "",
        f"Gerado em: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Arquivos verificados",
        "",
        *infos,
        "",
        "## Resultado",
        "",
    ]
    if issues:
        lines.extend(issues)
        lines.append("")
        lines.append("Resultado final: falha.")
        code = 1
    else:
        lines.append("- Nenhuma violacao critica detectada.")
        lines.append("")
        lines.append("Resultado final: sucesso.")
        code = 0
    saida.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Relatorio gerado: {saida}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
