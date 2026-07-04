# Dicionário de dados

Este documento explica os campos e classificações usados para transformar registros de ART em dados agregados exibidos no painel.

## Campos de identificação

| Campo | Descrição | Aparece no painel público? |
|---|---|---|
| `id_art` | Identificador individual da ART, quando existir. | Não |
| `ano` | Ano de referência da ART ou da base processada. | Sim, agregado |
| `fonte_arquivo` | Referência à planilha ou base de origem do registro. | Não, uso interno de rastreabilidade |
| `fonte_aba` | Aba ou período de origem dentro da base. | Não, uso interno de rastreabilidade |

## Classe de confiabilidade

Cada ART recebe uma classe que indica o quanto ela pode ser associada com segurança a um único serviço e a um único valor declarado.

| Classe | Significado | Uso permitido | Uso proibido |
|---|---|---|---|
| `A` | ART com atividade única e valor associável, com baixo risco de mistura entre serviços. | Cálculo monetário de referência (mediana, Q1, Q3); base principal do painel. | Ranking individual de profissional ou empresa. |
| `B` | ART com múltiplas linhas homogêneas (mesmo código, valor único replicado). | Análise secundária ou simulação, sempre com ressalva explícita. | Base principal de valor sem ressalva. |
| `C` | ART com múltiplas atividades ou códigos e valor único não decomponível entre elas. | Frequência, indicação de demanda e detecção de serviços novos. | Cálculo monetário por serviço. |
| `D` | ART com valor ausente, zerado ou implausível, ou serviço não mapeável. | Apenas registro de volume e motivo de exclusão. | Qualquer cálculo monetário. |

Somente a Classe A, combinada com natureza do valor igual a provável honorário técnico e `n >= 5`, gera referência monetária no painel.

## Campos territoriais

| Campo | Descrição | Observação |
|---|---|---|
| `municipio_original` | Valor textual como veio da base. | Preservar em base local. |
| `municipio_padronizado` | Nome padronizado após normalização. | Só preencher com correspondência segura. |
| `codigo_ibge` | Código oficial IBGE do município. | Exige fonte oficial. |
| `inspetoria_crea_ba` | Inspetoria CREA-BA associada ao município. | Exige fonte oficial. |
| `sureg_crea_ba` | SUREG CREA-BA associada ao município. | Exige fonte oficial. |

Sem correspondência segura, usar:

`Informação insuficiente para verificar.`

## Campos TOS

| Campo | Descrição |
|---|---|
| `codigo_tos` | Código TOS identificado ou mapeado. |
| `grupo_tos` | Grupo TOS associado. |
| `status_tos` | Situação do mapeamento TOS. |
| `regra_tos` | Regra usada para identificar ou inferir o TOS. |

Valores mínimos esperados para `status_tos`:

- `identificado`;
- `inferido_por_regra_documentada`;
- `ausente`;
- `inconsistente`;
- `informacao_insuficiente`.

## Campos de serviço

| Campo | Descrição |
|---|---|
| `servico_original` | Texto original do serviço ou descrição equivalente. |
| `servico_padronizado` | Serviço padronizado usado no painel. |
| `grupo_servico` | Grupo metodológico ou grupo SENGE associado. |
| `status_senge` | Correspondência com tabela SENGE, quando houver fonte. |

Valores mínimos esperados para `status_senge`:

- `correspondencia_confirmada`;
- `correspondencia_parcial`;
- `lacuna_senge`;
- `servico_novo`;
- `diagnostico_demanda`;
- `informacao_insuficiente`.

## Campos monetários

| Campo | Descrição | Publicar? |
|---|---|---|
| `valor_declarado_original` | Valor declarado por ART. | Não, linha a linha. |
| `valor_declarado_normalizado` | Valor convertido para número. | Não, linha a linha. |
| `natureza_valor` | Classificação da natureza do valor. | Sim, agregado. |
| `flag_valor_extremo` | Indica valor extremo conforme regra documentada. | Sim, agregado. |

Valores mínimos esperados para `natureza_valor`:

- `provavel_honorario_tecnico`;
- `provavel_valor_obra_contrato`;
- `valor_simbolico_ou_taxa`;
- `valor_inconsistente_ou_extremo`;
- `valor_zerado`;
- `valor_ausente`;
- `informacao_insuficiente`.

## Campos estatísticos agregados

| Campo | Descrição |
|---|---|
| `n` | Número de registros no agregado. |
| `mediana` | Mediana do valor, quando permitido pela regra metodológica. |
| `q1` | Primeiro quartil, quando permitido. |
| `q3` | Terceiro quartil, quando permitido. |
| `iqr` | Intervalo interquartil. |
| `media` | Média, se usada com ressalva metodológica. |
| `minimo` | Menor valor observado após regra declarada. |
| `maximo` | Maior valor observado após regra declarada. |

Para `n < 5`, valores monetários de referência devem ser substituídos por:

`Informação insuficiente para verificar.`
