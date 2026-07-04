# Limitações metodológicas

Este documento registra limitações conhecidas ou a verificar no projeto.

## Escopo atual da camada TOS

A camada TOS atualmente publicada corresponde a um subconjunto da base disponível. A ampliação para o universo completo de ARTs depende de validação dos campos disponíveis, compatibilidade entre planilhas e regra rastreável de mapeamento.

Quando a expansão não puder ser executada ou verificada, registrar:

`Informação insuficiente para verificar.`

## Agregado anual 2015-2022

O agregado público 2015-2022 foi gerado a partir das planilhas semestrais locais em `C:\Users\adina\Meu Drive\ARTS Adinailson` e do CSV consolidado `ARTs 2022 01022024.csv`.

As bases anuais brutas usadas nessa agregação não possuem campo `codigo_tos`. Por isso, nos registros anuais agregados, a dimensão TOS é mantida como:

`Informação insuficiente para verificar.`

Os arquivos `.xls` de 2015 (2º semestre) a 2019 (ambos semestres) têm 65.535 linhas de dados lidas em cada semestre, exatamente o limite do formato `.xls`. Isso indica truncamento quase certo na origem: os totais desses anos devem ser tratados como mínimo observado, não como universo necessariamente completo.

As planilhas `.xlsx` de 2015 (1º semestre), 2020 (ambos semestres) e 2021 (ambos semestres) também têm 65.534 linhas de dados por semestre. Esse valor não é limite técnico do formato `.xlsx`, mas é a mesma cifra do teto legado do `.xls` — a hipótese mais provável é que a exportação original (antes de virar `.xlsx`) tenha passado pelo mesmo processo de extração limitado a esse teto. Sem uma fonte oficial de total de ARTs por ano para comparar, essa suspeita não pode ser confirmada nem descartada; os totais desses semestres também devem ser tratados como mínimo observado.

O agregado gerado por `scripts/agrega_anos_publico.py` marca essa limitação no manifesto (`docs/modelos/manifesto_bases_anuais_modelo.csv`, coluna `observacao`) usando a contagem real de linhas lidas (65.534-65.536), não a extensão do arquivo — porque o mesmo teto suspeito apareceu em arquivos `.xls` e `.xlsx`. Apenas 2022 (CSV com 726.028 linhas) está fora dessa faixa e pode ser tratado como contagem completa da fonte.

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

Bases linha a linha derivadas das ARTs não devem ser publicadas no GitHub Pages por poderem conter identificadores, município, formação e valor por registro.

A publicação deve permanecer agregada.
