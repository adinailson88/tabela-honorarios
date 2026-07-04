# Metodologia

Este documento explica como o painel de subsídio técnico para a Tabela de Honorários do SENGE/BA foi construído e como ele deve ser lido.

## Fonte dos dados

As informações usadas neste painel têm origem nas Anotações de Responsabilidade Técnica (ART) registradas no sistema SITAC do CREA-BA. Os dados são tratados, classificados e agregados antes da publicação; nenhuma ART individual é exibida.

## Finalidade

O projeto tem finalidade técnica, orientativa e agregada. O painel não define preço obrigatório, piso, tabela vinculante, ranking de profissionais, ranking de empresas ou comprovação individual de honorários.

Os dados de ARTs do CREA-BA são usados como evidência auxiliar, indireta e agregada de escopo, atividade, localidade, responsabilidade técnica e valor declarado.

A ART não é contrato, nota fiscal nem prova isolada de honorário profissional.

## Premissa sobre valor declarado

O valor declarado em ART não deve ser tratado automaticamente como honorário profissional real.

A natureza do valor deve ser classificada separando, no mínimo:

- provável honorário técnico;
- provável valor de obra ou contrato;
- taxa simbólica ou valor simbólico;
- valor inconsistente ou extremo;
- valor ausente;
- informação insuficiente para verificar.

Quando faltar evidência para classificar a natureza do valor, usar exatamente:

`Informação insuficiente para verificar.`

## Regra monetária do painel

Mediana, Q1, Q3 e IQR monetários só devem ser exibidos quando a base filtrada atender simultaneamente aos seguintes critérios:

1. Classe de confiabilidade A;
2. natureza do valor igual a provável honorário técnico;
3. amostra com `n >= 5`.

Quando `n < 5`, o resultado monetário deve ser tratado como:

`Informação insuficiente para verificar.`

## TOS

A camada atual com TOS é um subconjunto da base disponível. A expansão do mapeamento TOS para o universo completo de ARTs ou para planilhas de outros anos depende da existência de campos compatíveis e regra rastreável.

Cada registro ou agregado deve permitir diferenciar:

- TOS identificado;
- TOS inferido por regra documentada;
- TOS ausente;
- TOS inconsistente;
- informação insuficiente para verificar.

## Municípios

A padronização municipal deve preservar o valor original e criar campos padronizados somente quando houver correspondência segura.

A referência preferencial para município e código municipal é o IBGE.

O de-para `município -> inspetoria -> SUREG -> CREA-BA` só deve ser preenchido com fonte oficial ou arquivo institucional validado. Sem fonte oficial, registrar:

`Informação insuficiente para verificar.`

## Outliers

Registros extremos não devem ser apagados sem regra documentada.

A metodologia deve preservar:

- valor original;
- flag de valor extremo;
- critério aplicado;
- base agregada antes do tratamento;
- base agregada depois do tratamento;
- impacto sobre n, mediana, Q1, Q3, mínimo, máximo e média quando aplicável.

## Serviços novos e lacunas SENGE

Serviços com baixa amostra, especialmente `n < 5`, não devem ser convertidos em referência de honorário sem ressalva explícita.

Separar:

- referência confiável observada;
- baixa amostra;
- serviço novo;
- lacuna da tabela SENGE;
- diagnóstico de demanda;
- informação insuficiente para verificar.

## Termos estatísticos usados no painel

- **n**: número de ARTs que compõem o cálculo. Quanto maior, mais estável é a leitura; abaixo de 5, o painel não calcula referência monetária.
- **mediana**: valor central da distribuição de valores declarados — metade dos registros está acima e metade abaixo. É preferida à média porque é menos sensível a valores extremos.
- **Q1 e Q3 (primeiro e terceiro quartis)**: delimitam a faixa onde estão os 50% de valores mais centrais da distribuição (entre 25% e 75%).
- **IQR (intervalo interquartil)**: distância entre Q3 e Q1. Ajuda a visualizar a dispersão dos valores declarados para um mesmo serviço.
- **Classe de confiabilidade (A, B, C, D)**: indica o quanto um registro de ART pode ser associado com segurança a um único serviço e a um único valor. Classe A reúne ART com atividade única e valor associável com baixo risco de mistura entre serviços — por isso é a única classe usada para cálculo monetário. Classes B, C e D servem para análise secundária, diagnóstico de demanda ou apenas registro de volume, nunca para cálculo de honorário.
- **Provável honorário técnico**: uma das classificações possíveis para a natureza do valor declarado em ART, indicando que o valor é compatível com elaboração de projeto, consultoria ou atividade técnica (e não com execução de obra, taxa simbólica ou valor incongruente).

## Como ler o painel

- **Serviços com referência confiável de preço**: lista, de forma independente dos demais filtros, todo serviço que atinge Classe A + provável honorário técnico + n≥5 no ano carregado, com mediana, Q1, Q3 e os municípios em que aparece. Use essa lista para escolher diretamente o que investigar, em vez de testar filtro por filtro.
- **Filtro "Somente serviços com referência confiável de preço"**: restringe a lista de serviços do filtro lateral apenas aos que têm preço confiável. Os demais serviços permanecem visíveis nas opções normais, identificados como "sem referência confiável" ou "baixa amostra".
- **Boxplot agregado**: representa graficamente a caixa entre Q1 e Q3, com uma linha na mediana, para os serviços com referência confiável. Por ser construído a partir de quartis já agregados, ele não mostra valores mínimos, máximos, pontos individuais nem outliers — apenas a faixa central da distribuição.
- **Municípios do serviço/seleção filtrada**: mostra, em lista ordenada por quantidade de ARTs, os municípios em que o serviço ou a combinação de filtros escolhida aparece. Como não há geometria territorial (mapa) disponível nos dados agregados publicados, essa informação é exibida como lista/ranking, não como mapa.
- **Top grupos TOS**: ranking por quantidade de ARTs (contagem), não por valor monetário. Quando não há ARTs suficientes para os filtros aplicados, o painel explica isso em vez de exibir uma seção vazia.
- **Tabela "Serviços - referência confiável observada"**: mostra todo serviço/unidade dentro da seleção atual de filtros, indicando explicitamente quando o resultado é `Informação insuficiente para verificar.` por baixa amostra.
