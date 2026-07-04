# Fontes

Este documento deve registrar as fontes usadas no projeto.

## Fontes confirmadas no repositório

| Fonte | Uso | Situação |
|---|---|---|
| `TABELA TOS - 2.xlsx`, aba `ARTs CREA 2022 (TOS)` | Camada TOS atual do painel agregado | Fonte indicada no JSON publicado |
| `dados_tos_valor_municipio.json` | Base agregada usada pelo painel | Publicada no repositório |
| `index.html` | Arquivo publicado pelo GitHub Pages | Publicado na raiz |
| `build_dashboard_tos_valor_municipio_layout_crea.py` | Script de geração do painel institucional | Publicado na raiz |

## Fontes a verificar antes de uso metodológico

| Fonte necessária | Finalidade | Situação padrão |
|---|---|---|
| Planilhas anuais completas de ARTs | Inclusão de outros anos | Informação insuficiente para verificar. |
| Base oficial IBGE de municípios | Padronização municipal e código IBGE | Informação insuficiente para verificar. |
| De-para oficial CREA-BA município/inspetoria/SUREG | Regionalização institucional | Informação insuficiente para verificar. |
| Tabela atual do SENGE/BA | Cruzamento de serviços, unidades e lacunas | Informação insuficiente para verificar. |
| Critério documentado de CUB | Referência de custo quando aplicável | Informação insuficiente para verificar. |
| Critérios técnicos de esforço profissional | Discussão metodológica de honorários | Informação insuficiente para verificar. |

## Regra de preenchimento

Não registrar fonte por inferência.

Cada fonte deve conter, quando disponível:

- nome do arquivo ou documento;
- origem institucional;
- versão ou data;
- caminho local ou URL pública, quando permitido;
- campo ou coluna utilizada;
- etapa do pipeline em que foi usada;
- limitação de uso.

Quando qualquer elemento essencial não puder ser verificado, registrar:

`Informação insuficiente para verificar.`
