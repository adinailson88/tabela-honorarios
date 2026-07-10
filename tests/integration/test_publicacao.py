from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
SCRIPTS = REPO / "scripts"
INDEX = REPO / "index.html"
ASSETS = REPO / "assets"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Falha ao carregar modulo {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PublicacaoIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_module("validar_json_publico_test", SCRIPTS / "01_validar_json_publico.py")
        cls.builder = load_module("build_dashboard_publico_test", SCRIPTS / "build_dashboard_publico.py")

    def test_validacao_publica_passa_nos_jsons_versionados(self) -> None:
        issues: list[str] = []
        infos: list[str] = []
        for path in self.validator.scan_files(ASSETS):
            self.validator.validate_file(path, issues, infos)
        self.assertEqual(issues, [], msg="\n".join(issues))
        self.assertGreater(len(infos), 0)

    def test_build_dashboard_e_deterministico(self) -> None:
        before = INDEX.read_bytes()
        self.builder.main()
        first = INDEX.read_bytes()
        self.builder.main()
        second = INDEX.read_bytes()
        self.assertEqual(hashlib.sha256(first).hexdigest(), hashlib.sha256(second).hexdigest())
        self.assertEqual(first, second)
        self.assertEqual(first, before)

    def test_index_embute_javascript_sintaticamente_valido(self) -> None:
        js_check = """
const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const match = html.match(/<script>([\\s\\S]*)<\\/script>/);
if (!match) throw new Error('script not found');
new Function(match[1]);
console.log('ok');
"""
        result = subprocess.run(
            ["node", "-e", js_check],
            cwd=REPO,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("ok", result.stdout)

    def test_artefatos_publicos_nao_expoem_identificadores_nem_caminhos_locais(self) -> None:
        blocked_json = ["id_art", "valor_art", "classeA", "C:\\Users\\", "cpf", "cnpj", "contratante", "profissional"]
        blocked_csv = ["id_art", "valor_art", "classeA", "C:\\Users\\", "cpf", "cnpj", "contratante"]
        blocked_html = ["C:\\Users\\"]
        for path in sorted(ASSETS.rglob("*.json")):
            text = path.read_text(encoding="utf-8", errors="replace")
            for token in blocked_json:
                self.assertNotIn(token, text, msg=f"{token} encontrado em {path}")
        for path in sorted((ASSETS / "referencia").glob("*.csv")):
            text = path.read_text(encoding="utf-8", errors="replace")
            for token in blocked_csv:
                self.assertNotIn(token, text, msg=f"{token} encontrado em {path}")
        html_text = INDEX.read_text(encoding="utf-8", errors="replace")
        for token in blocked_html:
            self.assertNotIn(token, html_text, msg=f"{token} encontrado em {INDEX}")

    def test_referencias_publicas_do_manifesto_existem(self) -> None:
        hist_manifest = json.loads((ASSETS / "datasets" / "historico" / "manifest.json").read_text(encoding="utf-8"))
        combined = REPO / hist_manifest["combined_file"]
        self.assertTrue(combined.exists(), msg=str(combined))
        for item in hist_manifest["anos"]:
            target = REPO / item["arquivo"]
            self.assertTrue(target.exists(), msg=str(target))


if __name__ == "__main__":
    unittest.main()
