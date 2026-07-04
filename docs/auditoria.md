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
