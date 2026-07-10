# scripts

Diretorio reservado para scripts ativos do pipeline publico.

## Fluxo recomendado

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\executar_tudo_sem_codex.ps1 -SomenteValidar
```

## Scripts ativos

### `publicar_datasets_publicos.py`

Migra os JSONs legados para a arquitetura publica saneada em `assets/datasets/`, removendo da arvore rastreada os vetores alinhados por ART antes publicados.

### `build_dashboard_publico.py`

Regenera `index.html` a partir dos manifests em `assets/datasets/`.

### `build_dashboard_tos_valor_municipio_layout_crea.py`

Wrapper de compatibilidade para o build publico atual.

### `01_validar_json_publico.py`

Varre todos os JSONs publicados em `assets/` e falha quando encontra vetores individualizados, caminhos locais, esquema ausente, `n < 5`, indices fora das dimensoes ou reconciliacoes invalidas.

### `rodar_validacoes_locais.ps1`

Executa build e validacoes locais basicas sem alterar a publicacao.

### `executar_tudo_sem_codex.ps1`

Executor operacional local em modo seguro, sem `git pull` automatico e com parada em erro.
