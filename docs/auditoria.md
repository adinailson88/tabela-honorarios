# Auditoria

Este documento define a trilha mínima de auditoria para cada processamento anual de ARTs.

## Objetivo

Garantir rastreabilidade entre arquivos de entrada, regras de tratamento, bases intermediárias, dados agregados e o que é publicado no painel público.

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

Não publicar dados linha a linha de ART neste painel.

A publicação deve conter somente dados agregados suficientes para visualização institucional, sem identificação individual de profissional, empresa, contratante ou ART específica.

## Processamento anual executado em 2026-07-04

O processamento mais recente consolidou as bases de ART de 2015 a 2022 e atualizou os agregados públicos consumidos pelo painel, incluindo o agregado combinado do período e um agregado individual por ano.

Totais consolidados observados:

- ARTs únicas agregadas no período 2015-2022: 513384;
- ARTs únicas em 2022 no CSV consolidado: 230928;
- registros Classe A com valor no vetor público do painel: 194051;
- anos publicados no seletor do painel: 2015, 2016, 2017, 2018, 2019, 2020, 2021 e 2022.

Limitação registrada: as bases anuais não contêm `codigo_tos`; nesses registros, TOS foi mantido como `Informação insuficiente para verificar.`. Os `.xls` de 2015-2019 atingem o limite técnico do formato e têm possível truncamento na origem.
