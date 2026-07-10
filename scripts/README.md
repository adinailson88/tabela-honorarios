# scripts

Diretorio reservado para scripts ativos do pipeline publico.

## Fluxo recomendado

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\executar_tudo_sem_codex.ps1 -SomenteValidar
```

## Scripts ativos

### `agrega_anos_publico.py`

Gera agregados intermediarios locais saneados a partir das bases anuais privadas, com parser CSV robusto e saida em `data/local/processado/publicacao_intermediaria/`.

### `publicar_datasets_publicos.py`

Migra os agregados intermediarios locais para a arquitetura publica saneada em `assets/datasets/`, com fallback de compatibilidade para o contrato legado quando esses insumos ainda existirem.

### `build_dashboard_publico.py`

Regenera `index.html` a partir dos manifests em `assets/datasets/`.

### `build_dashboard_tos_valor_municipio_layout_crea.py`

Wrapper de compatibilidade para o build publico atual.

### `01_validar_json_publico.py`

Varre todos os JSONs publicados em `assets/` e falha quando encontra vetores individualizados, caminhos locais, esquema ausente, `n < 5`, indices fora das dimensoes ou reconciliacoes invalidas.

### `rodar_validacoes_locais.ps1`

Executa build e validacoes locais basicas sem alterar a publicacao.

### `executar_tudo_sem_codex.ps1`

Executor operacional local em modo seguro, sem `git pull` automatico e com parada em erro. Publica datasets apenas quando encontra agregados intermediarios locais ou insumos legados.

### `00_inventariar_planilhas_arts.py`

Inventaria planilhas locais em `data/local/` para registrar disponibilidade de insumos privados sem publicar conteudo.

### `gerar_metodologia_servicos_tos_valor_municipio.py`

Regenera referencias metodologicas auxiliares em `assets/referencia/` a partir de fontes locais quando disponiveis.

## Scripts legados preservados

Os arquivos abaixo permanecem na raiz apenas por preservacao historica e rastreabilidade tecnica. Eles nao fazem parte do build publico atual validado em CI:

- `agrega_arts.py`
- `calibra_atividade.py`
- `flat_counts.py`
- `gera_dashboard.py`
- `gera_painel.py`
- `gera_planilha.py`
- `gera_apresentacao.py`
- `serie_temporal.py`
- `teste_filtros_codex.py`

O inventario consolidado desses artefatos esta em `docs/inventario_artefatos.md`.
