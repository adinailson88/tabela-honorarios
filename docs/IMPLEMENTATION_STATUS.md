# IMPLEMENTATION STATUS

## Fase atual

Fases 1 e 2 concluidas com a migracao dos artefatos publicos para `assets/datasets/`, bloqueio da publicacao individualizada por ART e separacao entre agregados intermediarios locais e contrato publico versionado.

## Arquivos alterados

- scripts: `publicar_datasets_publicos.py`, `agrega_anos_publico.py`, `gerar_metodologia_servicos_tos_valor_municipio.py`, `01_validar_json_publico.py`, `build_dashboard_publico.py`, `build_dashboard_tos_valor_municipio_layout_crea.py`, `rodar_validacoes_locais.ps1`, `executar_tudo_sem_codex.ps1`, `README.md`
- dados publicos: `assets/datasets/**`, remocao dos JSONs legados em `assets/dados_tos_valor_municipio.json` e `assets/anos/*.json`
- documentacao: `README.md`, `scripts/README.md`, `docs/metodologia.md`, `docs/modelos/manifesto_bases_anuais_modelo.csv`

## Testes executados

- `python scripts\publicar_datasets_publicos.py`
- `python scripts\build_dashboard_publico.py`
- `python scripts\01_validar_json_publico.py --root assets --saida relatorios\validacao_json_publico.md`
- `python -m py_compile scripts\publicar_datasets_publicos.py scripts\01_validar_json_publico.py scripts\build_dashboard_publico.py scripts\build_dashboard_tos_valor_municipio_layout_crea.py`

## Pendencias

- Fase 3: ampliar validacao funcional do dashboard em navegador e revisar acessibilidade com teste visual.
- Fase 4: adicionar testes automatizados e workflow GitHub Actions.
- Fase 5: concluir inventario de obsolescencia e limpeza controlada dos artefatos historicos e auxiliares.
