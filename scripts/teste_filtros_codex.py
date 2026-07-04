from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

def normalize_key(value):
    text = "" if value is None else str(value)
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s*[-/]\s*BA$", "", text, flags=re.I)
    return text.strip().upper()

def count(flat, ano=(), municipio=(), modalidade=(), unidade=(), tipo=()):
    selected = {
        "ano": {normalize_key(v) for v in ano},
        "municipio": {normalize_key(v) for v in municipio},
        "modalidade": {normalize_key(v) for v in modalidade},
        "unidade": {normalize_key(v) for v in unidade},
        "tipo": {normalize_key(v) for v in tipo},
    }
    def ok(row):
        values = {
            "ano": normalize_key(flat["anos"][row[0]]),
            "municipio": normalize_key(flat["municipios"][row[1]]),
            "modalidade": normalize_key(flat["modalidades"][row[2]]),
            "unidade": normalize_key(flat["unidades"][row[3]]),
            "tipo": normalize_key(flat["tipos"][row[4]]),
        }
        return all(not choices or values[name] in choices for name, choices in selected.items())
    rows = [r for r in flat["recs"] if ok(r)]
    return sum(r[5] for r in rows), len(rows)

if __name__ == "__main__":
    flat = json.loads((REPO / "dados" / "flat_counts.json").read_text(encoding="utf-8"))
    tests = {
        "Itabuna": count(flat, municipio=["Itabuna"]),
        "Ilhéus": count(flat, municipio=["Ilhéus"]),
        "Salvador": count(flat, municipio=["Salvador"]),
        "Itabuna + Ilhéus": count(flat, municipio=["Itabuna", "Ilhéus"]),
        "2024 + 2026": count(flat, ano=["2024", "2026"]),
        "2021 + 2022": count(flat, ano=["2021", "2022"]),
        "duas modalidades": count(flat, modalidade=["Eng. Civil", "Eng. Eletricista"]),
        "município + ano + modalidade": count(flat, municipio=["Itabuna"], ano=["2022"], modalidade=["Eng. Civil"]),
    }
    for name, (atividades, grupos) in tests.items():
        print(f"{name}: {atividades} atividades | {grupos} grupos")

