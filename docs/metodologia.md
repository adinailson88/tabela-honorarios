# Metodologia

Este documento registra a metodologia atual do projeto `tabela-honorarios`.

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
