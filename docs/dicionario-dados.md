# Dicionário de dados

Este documento descreve campos esperados ou derivados no pipeline metodológico.

## Campos de identificação

| Campo | Descrição | Publicar no GitHub Pages? |
|---|---|---|
| `id_art` | Identificador individual da ART, quando existir. | Não |
| `ano` | Ano de referência da ART ou da base processada. | Sim, agregado |
| `fonte_arquivo` | Nome do arquivo de origem. | Sim, em relatório |
| `fonte_aba` | Aba ou planilha de origem. | Sim, em relatório |

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
