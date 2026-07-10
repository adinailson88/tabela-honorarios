from __future__ import annotations

import csv
import importlib.util
import sys
import tempfile
import types
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO / "scripts" / "agrega_anos_publico.py"


def load_module():
    sys.modules.setdefault("openpyxl", types.SimpleNamespace(load_workbook=None))
    sys.modules.setdefault(
        "xlrd",
        types.SimpleNamespace(open_workbook=None, XL_CELL_DATE=3, xldate_as_tuple=None),
    )
    spec = importlib.util.spec_from_file_location("agrega_anos_publico_test", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Falha ao carregar agrega_anos_publico.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AgregaAnosPublicoUnitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mod = load_module()

    def write_csv(self, rows: list[list[str]]) -> Path:
        temp_dir = Path(tempfile.mkdtemp())
        path = temp_dir / "arts_2022.csv"
        with path.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.writer(fh, delimiter=";", quotechar='"')
            writer.writerows(rows)
        return path

    def test_iter_csv_respeita_aspas_ponto_virgula_e_hifen(self) -> None:
        path = self.write_csv(
            [
                [
                    "id",
                    "tipo_art",
                    "formaderegistro",
                    "emissao",
                    "cidade_obra",
                    "uf",
                    "titulos",
                    "entidade",
                    "codigo",
                    "atividade",
                    "quantidade",
                    "unidade",
                    "valor_contrato",
                    "ano_registro_profissional",
                ],
                [
                    "1001",
                    "Obra",
                    "Online",
                    "01/02/2022",
                    "Salvador",
                    "BA",
                    "Eng. Civil",
                    "CREA",
                    "A-1",
                    "Atividade - Projeto; complementar - detalhe",
                    "1",
                    "unidade",
                    "R$ 1.234,56",
                    "2015",
                ],
            ]
        )
        iterator, meta = self.mod.iter_csv(path)
        rows = list(iterator)
        row = rows[0]
        self.assertIn("atividade", row)
        self.assertEqual(row["atividade"], "Atividade - Projeto; complementar - detalhe")
        self.assertEqual(meta["header"][9], "atividade")
        self.assertEqual(self.mod.parse_valor(row["valor_contrato"]), 1234.56)

    def test_add_art_agrega_art_multilinha_e_multiplos_codigos(self) -> None:
        arts = {}
        base = {
            "id": "2002",
            "emissao": "10/03/2022",
            "cidade_obra": "Itabuna",
            "uf": "BA",
            "titulos": "Eng. Eletricista",
            "tipo_art": "Servico",
        }
        row1 = dict(base, codigo="COD1", atividade="Atividade - Laudo", unidade="hora", valor_contrato="1000")
        row2 = dict(base, codigo="COD2", atividade="Atividade - Vistoria", unidade="", valor_contrato="1000")
        self.mod.add_art(arts, row1, 2022, "fonte.csv")
        self.mod.add_art(arts, row2, 2022, "fonte.csv")

        rows = self.mod.rows_from_arts(arts)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["qtd_atividades_art"], 2)
        self.assertEqual(rows[0]["uf"], "BA")
        self.assertEqual(rows[0]["unidade_medida"], "hora")

    def test_rows_from_arts_preserva_municipio_fora_bahia_no_registro_agregado(self) -> None:
        arts = {
            "2022:3003": {
                "n": 1,
                "val": 500.0,
                "vary": 0,
                "cods": {"CODX"},
                "ativ": ["Atividade - Consulta"],
                "uni": ["hora"],
                "tipo": "Servico",
                "titulo": "Eng. Civil",
                "cidade": "Belo Horizonte",
                "uf": "MG",
                "ano": "2022",
                "sources": {"fonte.csv"},
            }
        }
        rows = self.mod.rows_from_arts(arts)
        self.assertEqual(rows[0]["municipio_key"], "BELO HORIZONTE")
        self.assertEqual(rows[0]["uf"], "MG")

    def test_write_service_csv_trata_n4_como_insuficiente_e_n5_como_publicavel(self) -> None:
        rows = []
        for value in [100, 110, 120, 130]:
            rows.append(
                {
                    "classe_confiabilidade": "A",
                    "natureza_valor": "provavel_honorario_tecnico",
                    "valor_art": value,
                    "servico_honorarios_padronizado": "Servico N4",
                    "unidade_medida": "hora",
                    "grupo_servico_honorarios": "Grupo 1",
                }
            )
        for value in [200, 210, 220, 230, 240]:
            rows.append(
                {
                    "classe_confiabilidade": "A",
                    "natureza_valor": "provavel_honorario_tecnico",
                    "valor_art": value,
                    "servico_honorarios_padronizado": "Servico N5",
                    "unidade_medida": "hora",
                    "grupo_servico_honorarios": "Grupo 2",
                }
            )
        out_dir = Path(tempfile.mkdtemp())
        out_path = out_dir / "agregado.csv"
        self.mod.write_service_csv(rows, out_path)
        text = out_path.read_text(encoding="utf-8-sig")
        self.assertIn("Servico N4", text)
        self.assertIn("insuficiente", text)
        self.assertIn("Servico N5", text)
        self.assertIn("220.0", text)


if __name__ == "__main__":
    unittest.main()
