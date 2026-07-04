# -*- coding: utf-8 -*-
"""Valida o JSON agregado publicado pelo painel.

Uso recomendado no PowerShell, a partir da raiz do repositorio:

    python scripts/01_validar_json_publico.py --json assets/dados_tos_valor_municipio.json --saida relatorios/validacao_json_publico.md

O objetivo e detectar inconsistencias estruturais sem acessar dados linha a linha.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

OBRIGATORIAS = [
    "gerado_em",
    "fonte",
    "total_arts",
    "universo_total_2022",
    "classe_count",
    "natureza_count",
    "servicos",
    "grupo_de_servico",
    "unidades",
    "municipios",
    "anos",
    "naturezas",
    "grupos_tos",
    "agg",
    "classeA",
]

SINAIS_DADO_INDIVIDUAL = [
    re.compile(r"id[_\s-]*art", re.IGNORECASE),
    re.compile(r"cpf", re.IGNORECASE),
    re.compile(r"cnpj", re.IGNORECASE),
    re.compile(r"contratante", re.IGNORECASE),
    re.compile(r"profissional", re.IGNORECASE),
    re.compile(r"empresa", re.IGNORECASE),
]


def soma_dict(d: Dict[str, Any]) -> int:
    total = 0
    for v in d.values():
        try:
            total += int(v)
        except Exception:  # noqa: BLE001
            pass
    return total


def validar(data: Dict[str, Any], texto_json: str) -> List[str]:
    linhas: List[str] = []
    linhas.append("# Validacao do JSON publico")
    linhas.append("")
    linhas.append(f"Gerado em: {datetime.now().isoformat(timespec='seconds')}")
    linhas.append("")

    linhas.append("## Chaves obrigatorias")
    linhas.append("")
    ausentes = [k for k in OBRIGATORIAS if k not in data]
    if ausentes:
        for k in ausentes:
            linhas.append(f"- Ausente: `{k}`")
    else:
        linhas.append("- Todas as chaves obrigatorias foram localizadas.")
    linhas.append("")

    total = data.get("total_arts")
    universo = data.get("universo_total_2022")
    classe_count = data.get("classe_count", {}) if isinstance(data.get("classe_count"), dict) else {}
    natureza_count = data.get("natureza_count", {}) if isinstance(data.get("natureza_count"), dict) else {}

    linhas.append("## Contagens principais")
    linhas.append("")
    linhas.append(f"- `total_arts`: {total}")
    linhas.append(f"- `universo_total_2022`: {universo}")
    linhas.append(f"- soma `classe_count`: {soma_dict(classe_count)}")
    linhas.append(f"- soma `natureza_count`: {soma_dict(natureza_count)}")
    if isinstance(total, int):
        if soma_dict(classe_count) == total:
            linhas.append("- `classe_count` fecha com `total_arts`.")
        else:
            linhas.append("- ATENCAO: `classe_count` nao fecha com `total_arts`.")
        if soma_dict(natureza_count) == total:
            linhas.append("- `natureza_count` fecha com `total_arts`.")
        else:
            linhas.append("- ATENCAO: `natureza_count` nao fecha com `total_arts`.")
    linhas.append("")

    linhas.append("## Dimensoes")
    linhas.append("")
    for key in ["servicos", "grupo_de_servico", "unidades", "municipios", "anos", "naturezas", "grupos_tos", "agg"]:
        value = data.get(key)
        linhas.append(f"- `{key}`: {len(value) if isinstance(value, list) else 'Informacao insuficiente para verificar.'}")
    classe_a = data.get("classeA", {})
    if isinstance(classe_a, dict):
        linhas.append(f"- `classeA` campos: {', '.join(sorted(classe_a.keys()))}")
        vetores = {k: v for k, v in classe_a.items() if isinstance(v, list)}
        tamanhos = {k: len(v) for k, v in vetores.items()}
        if tamanhos:
            if len(set(tamanhos.values())) == 1:
                linhas.append(f"- `classeA` vetores alinhados: {next(iter(tamanhos.values()))} registros.")
            else:
                linhas.append(f"- ATENCAO: `classeA` vetores com tamanhos divergentes: {tamanhos}.")
        if "u" not in classe_a:
            linhas.append("- ATENCAO: `classeA.u` ausente; unidade de medida nao esta preservada por registro.")
    if isinstance(data.get("agg"), list):
        tamanhos_linhas = sorted({len(r) for r in data["agg"] if isinstance(r, list)})
        linhas.append(f"- tamanhos de linhas em `agg`: {tamanhos_linhas}")
        if tamanhos_linhas and tamanhos_linhas != [9]:
            linhas.append("- ATENCAO: `agg` deve usar 9 campos: classe, servico, unidade, ano, municipio, natureza, grupo_tos, n, atividades.")
    linhas.append("")

    linhas.append("## Sinais de dado individual")
    linhas.append("")
    achados = []
    for padrao in SINAIS_DADO_INDIVIDUAL:
        if padrao.search(texto_json):
            achados.append(padrao.pattern)
    if achados:
        linhas.append("- ATENCAO: foram encontrados termos que podem indicar dado individualizado:")
        for a in achados:
            linhas.append(f"  - `{a}`")
    else:
        linhas.append("- Nenhum sinal textual obvio de `id_art`, CPF, CNPJ, profissional, empresa ou contratante foi detectado no JSON.")
    linhas.append("")

    linhas.append("## Resultado")
    linhas.append("")
    if ausentes or achados:
        linhas.append("- Validacao concluida com pendencias.")
    else:
        linhas.append("- Validacao estrutural concluida sem pendencias criticas detectadas.")
    linhas.append("")
    linhas.append("Observacao: esta validacao nao substitui auditoria da base linha a linha.")
    return linhas


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida JSON agregado publico do painel.")
    parser.add_argument("--json", default="assets/dados_tos_valor_municipio.json", help="Caminho do JSON agregado.")
    parser.add_argument("--saida", default="relatorios/validacao_json_publico.md", help="Relatorio Markdown de saida.")
    args = parser.parse_args()

    json_path = Path(args.json)
    saida = Path(args.saida)
    saida.parent.mkdir(parents=True, exist_ok=True)

    if not json_path.exists():
        saida.write_text("# Validacao do JSON publico\n\nInformacao insuficiente para verificar: arquivo JSON nao encontrado.\n", encoding="utf-8")
        print(f"JSON nao encontrado: {json_path}")
        return 1

    texto = json_path.read_text(encoding="utf-8")
    data = json.loads(texto)
    linhas = validar(data, texto)
    saida.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"Relatorio gerado: {saida}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

