# scripts

Diretório reservado para scripts do pipeline.

## Situação atual

O script `build_dashboard_tos_valor_municipio_layout_crea.py` ainda permanece na raiz por compatibilidade com a estrutura atual do projeto.

Uma migração futura para `scripts/` deve atualizar os caminhos de entrada e saída e validar o GitHub Pages antes de publicar.

## Scripts esperados em evolução futura

- ingestão de planilhas anuais;
- validação de colunas obrigatórias;
- deduplicação por ART;
- mapeamento TOS;
- classificação da natureza do valor;
- padronização municipal com IBGE;
- tratamento de outliers;
- agregação pública;
- geração de relatórios de auditoria;
- build do painel.

## Regra

Scripts devem preservar dados linha a linha fora da publicação e gerar somente artefatos agregados para o GitHub Pages.
