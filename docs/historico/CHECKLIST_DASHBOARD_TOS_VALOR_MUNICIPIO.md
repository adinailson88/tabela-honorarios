# Checklist de validação — dashboard TOS + Natureza do Valor + Município

**Arquivo:** `dashboard_senge_honorarios_tos_valor_municipio.html`
**Data:** 2026-06-24
Legenda: ✅ verificado nesta rodada · ☐ a conferir manualmente pelo usuário.

> Como abrir localmente: no terminal, dentro de `PROPOSTA CLAUDE`, rodar
> `python -m http.server 8765` e abrir `http://localhost:8765/dashboard_senge_honorarios_tos_valor_municipio.html`
> (ou abrir o arquivo direto no navegador — os dados estão embutidos no HTML).

| # | Teste | Status | Observação |
|---|---|---|---|
| 1 | Abrir o dashboard novo | ✅ | Carrega; título "camada TOS + Natureza do Valor + Município"; sem erro no console |
| 2 | Dashboard anterior continua intacto | ✅ | `dashboard_senge_honorarios_metodologia_servicos.html` idêntico ao backup (MD5 igual) |
| 3 | Filtrar Classe A | ✅ | KPIs recomputam; base confiável e mediana exibidas |
| 4 | Filtrar Classe B | ☐ | Recompute; mediana bloqueada (B não é base de cálculo) |
| 5 | Filtrar Classe C | ✅ | 28.362 ARTs; mediana "—"; aviso de bloqueio visível |
| 6 | Filtrar Classe D | ☐ | Mediana bloqueada; só volume |
| 7 | Filtrar serviço mapeado | ☐ | Tabela e KPIs restringem ao serviço |
| 8 | Filtrar "Não mapeado (candidato a novo serviço)" | ☐ | Aparece na contagem; **não** entra na tabela de referência confiável |
| 9 | Filtrar natureza do valor | ✅ | "obra/contrato" → mediana "—"+aviso; "honorário" → mediana R$ 1.000,00 |
| 10 | Mediana some quando valor não é confiável | ✅ | Bloqueio com Classe C/D ou natureza ≠ honorário |
| 11 | Valores extremos sinalizados | ✅ | Outliers IQR (763) reclassificados como inconsistente/extremo; barra de natureza mostra fatia |
| 12 | Testar município | ☐ | Buscar/selecionar município; KPIs restringem (confiabilidade registrada) |
| 13 | Limpar filtros | ✅ | Botão "Limpar filtros" zera seleção e volta ao subconjunto completo |
| 14 | Valores financeiros em R$ | ✅ | `formatBRL`: R$ 1.000,00; R$ 1.261,44; R$ 600,00 – R$ 1.800,00 |
| 15 | Contagens NÃO em R$ | ✅ | n=1.206, ARTs filtradas como número simples |
| 16 | Percentuais como % | ✅ | 86,0%; 66,2%; 0,0% |
| 17 | Códigos TOS/IBGE/atividade não em R$ | ✅ | Códigos não são formatados como moeda |
| 18 | Tabelas centralizadas | ✅ | th centro; td numérico centro; vertical-align middle |
| 19 | Colunas textuais longas legíveis | ✅ | `td.col-texto` (Serviço/Grupo) alinhadas à esquerda |
| 20 | Seção Metodologia visível | ✅ | `<details open>` com a premissa "evidência auxiliar, indireta e agregada…" |
| 21 | Campos sem valor confiável mostram "—" / "Informação insuficiente para verificar" | ✅ | n<5 → "Informação insuficiente para verificar"; KPIs bloqueados → "—" |

## Filtros — lógica
- ✅ Multisseleção mantida em todos os filtros (`<select multiple>`).
- ✅ Regra **OU** dentro do mesmo filtro / **E** entre filtros diferentes (ex.: Classe A *ou* B, **e** serviço X, **e** município Y).
- ✅ Indicador de filtros ativos e contador "filtradas / total".

## Itens para conferência manual recomendada
- ☐ Itens 4, 6, 7, 8, 12 (variações de filtro não testadas automaticamente).
- ☐ Conferir responsividade em tela menor, se necessário.
