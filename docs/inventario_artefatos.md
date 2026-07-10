# Inventario de artefatos

## Escopo

Este inventario registra, com base no uso real observado na branch `codex/dashboard-seguro-v2` em 2026-07-10, quais arquivos estao no contrato publico atual, quais permanecem apenas como historico tecnico e quais exigem cautela antes de qualquer reutilizacao ou republicacao.

Nenhum arquivo foi removido automaticamente nesta fase. Itens incertos permaneceram preservados e classificados.

## Contrato publico ativo

### Publicacao efetiva

- `index.html`
- `assets/datasets/historico/**`
- `assets/datasets/precos/resumos.json`
- `assets/datasets/tos-2022/manifest.json`
- `assets/datasets/qualidade/manifest.json`

### Documentacao ativa do painel publico

- `docs/metodologia.md`
- `docs/limitacoes.md`
- `docs/fontes.md`
- `docs/dicionario-dados.md`
- `docs/auditoria.md`
- `docs/IMPLEMENTATION_STATUS.md`

### Scripts ativos do pipeline publico

- `scripts/agrega_anos_publico.py`
- `scripts/publicar_datasets_publicos.py`
- `scripts/build_dashboard_publico.py`
- `scripts/build_dashboard_tos_valor_municipio_layout_crea.py`
- `scripts/01_validar_json_publico.py`
- `scripts/executar_tudo_sem_codex.ps1`
- `scripts/rodar_validacoes_locais.ps1`
- `scripts/00_inventariar_planilhas_arts.py`
- `scripts/gerar_metodologia_servicos_tos_valor_municipio.py`

### Testes e CI ativos

- `tests/**`
- `.github/workflows/validar-publicacao.yml`
- `requirements.txt`

## Referencias auxiliares ativas ou preservadas

### Consumidas diretamente pelo painel publico atual

- `assets/referencia/municipios_bahia_ibge_centroides.csv`
- `assets/referencia/bahia_estado_contorno_ibge.geojson`

### Geradas ou lidas por scripts ativos, mas fora do contrato principal do painel

- `assets/referencia/dim_municipios_bahia.csv`
- `assets/referencia/agregado_servicos_tos_classe_a_valor_confiavel.csv`
- `assets/referencia/resumo_natureza_valor.csv`
- `assets/referencia/diagnostico_padronizacao_municipios.csv`

### Referencias metodologicas preservadas

- `assets/referencia/06_MATRIZ_ATIVIDADES_HONORARIOS.csv`
- `assets/referencia/MATRIZ_SERVICOS_TABELA_ATUAL.csv`
- `assets/referencia/MATRIZ_TABELA_ATUAL_X_ARTS.csv`
- `assets/referencia/agregado_servicos_classe_a.csv`
- `assets/referencia/frequencia_total_servicos.csv`
- `assets/referencia/resumo_classes_confiabilidade.csv`
- `assets/referencia/dim_municipio_crea.csv`

Esses arquivos permanecem uteis para auditoria, rastreabilidade metodologica e apoio institucional, mas nao compoem o contrato JSON efetivamente consumido por `index.html`.

## Artefatos historicos retidos

### Dados legados do dashboard anterior

- `dados/data.json`
- `dados/flat_counts.json`
- `dados/*.csv`
- `dados/REFERENCIA_CUB.md`

Status verificado: agregados historicos, sem evidencia de microdado individual nesta checagem, mas fora do contrato publico atual e ainda referenciados principalmente por documentos e scripts legados.

### Scripts legados mantidos na raiz por preservacao

- `scripts/agrega_arts.py`
- `scripts/calibra_atividade.py`
- `scripts/flat_counts.py`
- `scripts/gera_dashboard.py`
- `scripts/gera_painel.py`
- `scripts/gera_planilha.py`
- `scripts/gera_apresentacao.py`
- `scripts/serie_temporal.py`
- `scripts/teste_filtros_codex.py`

Status verificado: referenciados apenas por documentacao historica ou por trilhas antigas de execucao. Nao sao chamados pelo build publico atual nem pelo workflow `validar-publicacao.yml`.

### Historico documental

- `docs/historico/**`

Status verificado: arquivo de preservacao, auditoria e continuidade. Nao deve ser tratado como estado operacional vigente sem leitura contextual.

## Itens de cautela

### Contato institucional em arquivo de referencia

- `assets/referencia/dim_crea_unidades.csv`

Status verificado: contem colunas `endereco`, `email` e `telefone`. Nao foi identificado uso por `index.html` nem pelos testes de publicacao atual. Antes de qualquer reaproveitamento publico futuro, convem revisar a necessidade dessas colunas e o regime de divulgacao aplicavel.

### Arquivos ausentes ou ja descontinuados

- `assets/referencia/dados_metodologia_servicos.json`

Status verificado: arquivo nao encontrado no repositorio atual em 2026-07-10. Referencias residuais a esse nome aparecem apenas em documentacao historica.

## Decisao operacional desta fase

1. Manter o contrato publico atual centrado em `assets/datasets/**` e `index.html`.
2. Tratar `dados/**` e os scripts legados como historico tecnico retido, nao como pipeline vigente.
3. Preservar `assets/referencia/**` com leitura seletiva: parte ativa para mapa e metodologia, parte apenas historica ou institucional.
4. Nao mover nem excluir automaticamente arquivos incertos nesta rodada.
