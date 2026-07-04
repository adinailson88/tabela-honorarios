# Limitações metodológicas

Este documento registra limitações conhecidas ou a verificar no projeto.

## Escopo atual da camada TOS

A camada TOS atualmente publicada corresponde a um subconjunto da base disponível. A ampliação para o universo completo de ARTs depende de validação dos campos disponíveis, compatibilidade entre planilhas e regra rastreável de mapeamento.

Quando a expansão não puder ser executada ou verificada, registrar:

`Informação insuficiente para verificar.`

## Agregado anual 2015-2022

O agregado público do período 2015-2022 foi gerado a partir de planilhas semestrais de ARTs do CREA-BA e de uma base consolidada de 2022.

As bases anuais brutas usadas nessa agregação não possuem campo `codigo_tos`. Por isso, nos registros anuais agregados, a dimensão TOS é mantida como:

`Informação insuficiente para verificar.`

As planilhas semestrais de 2015 (2º semestre) a 2019 (ambos semestres) têm 65.535 linhas de dados lidas em cada semestre, exatamente o limite técnico do formato antigo de planilha eletrônica em que foram exportadas. Isso indica truncamento quase certo na origem: os totais desses anos devem ser tratados como mínimo observado, não como universo necessariamente completo.

As planilhas de 2015 (1º semestre), 2020 (ambos semestres) e 2021 (ambos semestres) também têm 65.534 linhas de dados por semestre. Esse valor não é limite técnico do formato em que essas planilhas foram entregues, mas é a mesma cifra do teto do formato mais antigo — a hipótese mais provável é que a exportação original tenha passado pelo mesmo processo de extração limitado a esse teto. Sem uma fonte oficial de total de ARTs por ano para comparar, essa suspeita não pode ser confirmada nem descartada; os totais desses semestres também devem ser tratados como mínimo observado.

Apenas a base de 2022 (726.028 linhas) está fora dessa faixa suspeita e pode ser tratada como contagem completa da fonte.

## Valor declarado em ART

O valor declarado em ART não equivale automaticamente a honorário profissional.

Pode representar, entre outras possibilidades:

- honorário técnico;
- valor de obra;
- valor contratual;
- taxa simbólica;
- valor de preenchimento inconsistente;
- valor extremo;
- campo sem evidência suficiente para interpretação.

O painel deve preservar essa distinção e evitar conclusão monetária sem filtro metodológico.

## Baixa amostra

Serviços com `n < 5` não devem ser usados como referência estatística de honorários.

Esses casos podem ser úteis como diagnóstico de demanda, indicação de serviço emergente ou lacuna de classificação, desde que a ressalva esteja explícita.

## Municípios, distritos e grafias variantes

Bases de ART podem conter municípios, distritos, localidades, grafias incompletas, erros de digitação e localidades fora da Bahia.

A padronização deve preservar o texto original e só atribuir código IBGE quando houver correspondência segura.

## Inspetoria e SUREG

O de-para `município -> inspetoria -> SUREG -> CREA-BA` depende de fonte oficial.

Sem fonte oficial, usar:

`Informação insuficiente para verificar.`

## Tabela SENGE

O cruzamento com a tabela SENGE exige fonte, versão, unidade de medida e regra de correspondência.

Não presumir equivalência entre descrição de ART e item SENGE sem evidência.

## CUB e esforço profissional

Qualquer uso de CUB, unidade de medida ou critério de esforço profissional deve estar vinculado a fonte documentada.

Sem fonte verificável, registrar:

`Informação insuficiente para verificar.`

## Dados não publicados

Bases linha a linha derivadas das ARTs não são publicadas neste painel por poderem conter identificadores, município, formação e valor por registro individual.

A publicação deve permanecer agregada.
