# Fontes

Este documento descreve, para quem consulta o painel, de onde vêm os dados exibidos e o que ainda não está confirmado por fonte oficial.

## Fonte primária dos dados

Os dados que alimentam o painel têm origem nas Anotações de Responsabilidade Técnica (ART) registradas no sistema SITAC do CREA-BA. A ART é o documento pelo qual um profissional registra, junto ao Conselho, a responsabilidade técnica por uma atividade ou serviço de engenharia, e nela consta um valor declarado.

Esse valor declarado não é, por si só, comprovante de honorário: pode representar honorário técnico, valor de obra ou contrato, taxa simbólica, ou até um valor inconsistente. Por isso o painel classifica a natureza do valor antes de qualquer uso estatístico — ver a seção Metodologia desta documentação.

## Cobertura temporal

Os agregados publicados cobrem o período de 2015 a 2022. Para os anos de 2015 a 2021, os totais anuais devem ser lidos como mínimo observado, não necessariamente como o total real de ARTs emitidas naquele ano: as planilhas semestrais de origem desses anos apresentam uma quantidade de linhas muito próxima do limite técnico de formatos antigos de planilha eletrônica, o que sugere possível truncamento na extração original. Apenas o ano de 2022 está fora dessa faixa e pode ser tratado como contagem completa. Detalhes na seção Limitações desta documentação.

## Camada de classificação por tipo de serviço (TOS)

Uma parte da base de 2022 foi classificada por tipo de serviço (TOS), permitindo agrupar as ARTs por atividade de forma mais padronizada. Essa classificação ainda não está disponível para todos os anos: quando o campo TOS não existe na base de um ano, o painel exibe `Informação insuficiente para verificar.` em vez de presumir um agrupamento.

## Fontes complementares ainda não incorporadas

As informações abaixo são relevantes para a metodologia, mas ainda não têm fonte oficial confirmada e incorporada ao painel. Enquanto isso, qualquer leitura que dependeria delas deve ser tratada como `Informação insuficiente para verificar.`

| Informação necessária | Finalidade | Situação |
|---|---|---|
| Base oficial do IBGE de municípios | Padronização de nomes de município e código IBGE | Informação insuficiente para verificar. |
| De-para oficial do CREA-BA entre município, inspetoria e SUREG | Leitura regional/institucional | Informação insuficiente para verificar. |
| Tabela de honorários vigente do SENGE/BA | Cruzamento entre serviço, unidade de medida e eventuais lacunas de tabela | Informação insuficiente para verificar. |
| Critério técnico documentado de CUB | Referência de custo de construção, quando aplicável | Informação insuficiente para verificar. |
| Critérios técnicos de esforço profissional | Discussão metodológica de honorários | Informação insuficiente para verificar. |

## Regra de leitura

Nenhuma fonte é presumida. Quando uma informação não pode ser confirmada por fonte oficial, o painel e esta documentação registram exatamente:

`Informação insuficiente para verificar.`
