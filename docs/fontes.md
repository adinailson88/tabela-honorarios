# Fontes

Este documento deve registrar as fontes usadas no projeto.

## Fontes confirmadas no repositório

| Fonte | Uso | Situação |
|---|---|---|
| `TABELA TOS - 2.xlsx`, aba `ARTs CREA 2022 (TOS)` | Camada TOS atual do painel agregado | Fonte indicada no JSON publicado |
| `dados_tos_valor_municipio.json` | Base agregada usada pelo painel | Publicada no repositório |
| `index.html` | Arquivo publicado pelo GitHub Pages | Publicado na raiz |
| `build_dashboard_tos_valor_municipio_layout_crea.py` | Script de geração do painel institucional | Publicado na raiz |
| `C:\Users\adina\Meu Drive\ARTS Adinailson\arts 2015 1 semestre - feito.xlsx` | Agregação anual pública de ARTs 2015 | Fonte local bruta, não versionada |
| `C:\Users\adina\Meu Drive\ARTS Adinailson\arts 2015 2 semestre.xls` a `arts 2019 2 semestre.xls` | Agregação anual pública de ARTs 2015-2019 | Fonte local bruta, não versionada; `.xls` no limite do formato |
| `C:\Users\adina\Meu Drive\ARTS Adinailson\arts 2020 1 semestre.xlsx` a `arts 2021 2 semestre.xlsx` | Agregação anual pública de ARTs 2020-2021 | Fonte local bruta, não versionada |
| `C:\Users\adina\Meu Drive\ARTS Adinailson\ARTs 2022 01022024.csv` | Agregação anual pública de ARTs 2022 | Fonte local bruta, não versionada |
| `C:\Users\adina\Meu Drive\ARTS Adinailson\Análise ARTs.xlsx` e `Análise ARTs Agronomia.xlsx` | Workbooks de análise/limpeza com abas metodológicas e abas 2020-2022 | Inspecionados como material auxiliar; não usados como fonte primária do agregado anual |

## Fontes a verificar antes de uso metodológico

| Fonte necessária | Finalidade | Situação padrão |
|---|---|---|
| Planilhas anuais completas de ARTs | Inclusão de outros anos | Processadas localmente em `scripts/agrega_anos_publico.py`; brutos não versionados |
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
