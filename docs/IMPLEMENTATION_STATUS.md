# IMPLEMENTATION STATUS

## Fase atual

Fases 1, 2, 3 e 4 concluidas com a migracao dos artefatos publicos para `assets/datasets/`, bloqueio da publicacao individualizada por ART, separacao entre agregados intermediarios locais e contrato publico versionado, redesenho do dashboard por finalidade e nivel de evidencia, e adicao de testes automatizados, dependencias declaradas e workflow de validacao publica.

## Arquivos alterados

- scripts: `publicar_datasets_publicos.py`, `agrega_anos_publico.py`, `gerar_metodologia_servicos_tos_valor_municipio.py`, `01_validar_json_publico.py`, `build_dashboard_publico.py`, `build_dashboard_tos_valor_municipio_layout_crea.py`, `rodar_validacoes_locais.ps1`, `executar_tudo_sem_codex.ps1`, `README.md`
- dados publicos: `assets/datasets/**`, remocao dos JSONs legados em `assets/dados_tos_valor_municipio.json` e `assets/anos/*.json`
- dashboard e documentacao: `index.html`, `README.md`, `scripts/README.md`, `docs/metodologia.md`, `docs/modelos/manifesto_bases_anuais_modelo.csv`
- testes e CI: `tests/**`, `requirements.txt`, `.github/workflows/validar-publicacao.yml`

## Testes executados

- `python scripts\publicar_datasets_publicos.py`
- `python scripts\build_dashboard_publico.py`
- `python scripts\01_validar_json_publico.py --root assets --saida relatorios\validacao_json_publico.md`
- `python -m py_compile scripts\publicar_datasets_publicos.py scripts\01_validar_json_publico.py scripts\build_dashboard_publico.py scripts\build_dashboard_tos_valor_municipio_layout_crea.py`
- `python -m py_compile scripts\build_dashboard_publico.py`
- `node -e "new Function(script_embutido_do_index_html)"`
- `python -m http.server 8765` com verificacao HTTP 200 para `index.html` e os datasets publicos
- busca no `index.html` para confirmar ausencia dos rotulos antigos proibidos, com excecao da mencao explicativa de substituicao do boxplot
- `python -m pip install -r requirements.txt`
- `python -m unittest discover -s tests -p "test_*.py" -v`
- `powershell -ExecutionPolicy Bypass -File .\scripts\executar_tudo_sem_codex.ps1 -SomenteValidar`

## Pendencias

- Fase 5: concluir inventario de obsolescencia e limpeza controlada dos artefatos historicos e auxiliares.
- Validacao visual assistida em navegador para desktop e mobile ainda nao foi executada neste turno.
