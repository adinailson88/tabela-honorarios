# Auditoria

Este documento define a trilha mínima de auditoria para cada processamento anual de ARTs.

## Objetivo

Garantir rastreabilidade entre arquivos de entrada, regras de tratamento, bases intermediárias, dados agregados e arquivos publicados no GitHub Pages.

## Registro mínimo por processamento

Para cada ano processado, registrar:

- ano de referência;
- arquivo de origem;
- aba ou planilha de origem;
- data de obtenção do arquivo, quando disponível;
- total de linhas lidas;
- total de ARTs únicas;
- duplicidades removidas;
- registros sem município;
- registros sem TOS;
- registros sem valor declarado;
- registros com valor zerado;
- registros com valor extremo;
- registros classificados como provável honorário técnico;
- registros classificados como provável valor de obra ou contrato;
- registros classificados como taxa simbólica ou valor simbólico;
- registros com informação insuficiente para verificar;
- total agregado publicado;
- total não publicado por conter dado individualizado.

## Campos usados

Documentar os campos efetivamente usados em cada etapa:

- identificador da ART;
- ano;
- município original;
- município padronizado;
- código IBGE, quando houver;
- serviço original;
- serviço padronizado;
- código TOS;
- grupo TOS;
- valor declarado;
- natureza do valor;
- classe de confiabilidade;
- flags de exclusão ou cautela.

Quando algum campo não existir ou não puder ser localizado, registrar:

`Informação insuficiente para verificar.`

## Critérios de exclusão

Nenhum registro deve ser excluído sem regra documentada.

Cada exclusão deve informar:

- regra aplicada;
- quantidade de registros afetados;
- percentual sobre a base lida;
- impacto sobre os agregados publicados;
- justificativa metodológica.

## Critérios de normalização

Registrar separadamente:

- normalização textual;
- normalização municipal;
- mapeamento TOS;
- classificação da natureza do valor;
- identificação de outliers;
- tratamento de baixa amostra.

## Saídas esperadas

Cada processamento deve produzir, quando aplicável:

- relatório de auditoria anual;
- resumo de qualidade da base;
- dados agregados para publicação;
- lista de limitações;
- log de validação dos arquivos gerados.

## Publicação

Não publicar dados linha a linha de ART no GitHub Pages.

A publicação deve conter somente dados agregados suficientes para visualização institucional, sem identificação individual de profissional, empresa, contratante ou ART específica.

## Processamento anual executado em 2026-07-04

O script `scripts/agrega_anos_publico.py` processou as bases locais de 2015-2022 e gerou:

- `assets/dados_tos_valor_municipio.json`;
- `assets/anos/dados_tos_valor_municipio_2015.json` a `assets/anos/dados_tos_valor_municipio_2022.json`;
- `docs/modelos/manifesto_bases_anuais_modelo.csv`;
- `relatorios/auditoria_bases_anuais.md`.

Totais consolidados observados:

- ARTs únicas agregadas no período 2015-2022: 513384;
- ARTs únicas em 2022 no CSV consolidado: 230928;
- registros Classe A com valor no vetor público do painel: 194051;
- anos publicados no seletor do painel: 2015, 2016, 2017, 2018, 2019, 2020, 2021 e 2022.

Limitação registrada: as bases anuais não contêm `codigo_tos`; nesses registros, TOS foi mantido como `Informação insuficiente para verificar.`. Os `.xls` de 2015-2019 atingem o limite técnico do formato e têm possível truncamento na origem.
