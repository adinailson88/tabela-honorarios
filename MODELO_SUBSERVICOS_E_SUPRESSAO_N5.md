# Modelo de subserviços e regra de supressão n < 5

**Frente:** SENGE-BA — Nova metodologia de tabela de honorários
**Data:** 2026-06-24
**Natureza:** especificação de modelo. Não implementa, não roda pipeline.

> Convenção: **[FATO VERIFICADO]**, **[INFERÊNCIA TÉCNICA]**, **[RECOMENDAÇÃO]**.
> Onde não há base local: **"Informação insuficiente para verificar"**.

---

## 1. Problema: da família ampla ao subserviço

**[FATO VERIFICADO]**
- A granularidade atual tem ~18 famílias amplas (ex.: "Instalações Elétricas", "Pericias e Laudos").
- Nessa granularidade, **nenhum** serviço ficou com `n < 5` em Classe A.
- Mas famílias amplas misturam modalidades muito diferentes: ex. "Climatização/Ventilação" tem mediana R$ 9.465 com Q3 R$ 58.634 (n=956) — sinal de subgrupos heterogêneos somados.

**[INFERÊNCIA TÉCNICA]** A ausência de `n < 5` hoje é **artefato da agregação grossa**, não prova de robustez. Ao descer para subserviço (que é o nível da tabela atual: 43 serviços), muitos subserviços terão poucos registros Classe A. Portanto a regra `n < 5` **passa a ser essencial** e deve operar **no nível de subserviço**, não no de família.

---

## 2. Esquema de granularidade alvo

**[RECOMENDAÇÃO]** Hierarquia de 5 níveis, alinhada à TOS e à tabela atual:

```
familia            (13 famílias da tabela atual SENGE)
 └─ grupo          (grupo_tos)
     └─ subgrupo   (subgrupo_tos)
         └─ servico        (servico_tos / servico_honorarios_padronizado)
             └─ complemento (complemento_tos — qualificador)
```

O **nível de cálculo monetário** recomendado é `servico` (com `complemento` quando houver n suficiente). Família e grupo servem para navegação e demanda; complemento só vira eixo de preço se sustentar `n ≥ 5`.

---

## 3. Estrutura de linha do agregado por subserviço

**[RECOMENDAÇÃO]** Cada linha do agregado de subserviço (`agregado_subservicos_classe_a_TOS.csv`, nome sugerido) deve conter:

| Campo | Descrição |
|---|---|
| `familia` | família da tabela atual SENGE |
| `grupo` | `grupo_tos` |
| `subgrupo` | `subgrupo_tos` |
| `servico` | `servico_honorarios_padronizado` |
| `complemento` | `complemento_tos` ou "Informação insuficiente para verificar" |
| `unidade_referencia` | unidade da tabela atual (BTN/m², kWp, hora, % CUB, valor fixo) ou "Informação insuficiente para verificar" |
| `modalidade` | modalidade/título profissional predominante (sem expor indivíduo) |
| `classe_confiabilidade` | A (cálculo), B (secundário) |
| `n_arts_classe_a` | nº de ARTs Classe A no subserviço |
| `mediana` | mediana de `valor_art` (se `n ≥ 5`) |
| `q1` | 1º quartil (se `n ≥ 5`) |
| `q3` | 3º quartil (se `n ≥ 5`) |
| `iqr` | Q3 − Q1 (se `n ≥ 5`) |
| `nivel_confianca_mapeamento_predominante` | exato/aproximado/manual |
| `regra_n5_aplicada` | sim/não |
| `observacao` | ressalva (ex.: "valor da ART, não honorário líquido") |

**[FATO VERIFICADO]** A unidade física (área, potência, extensão) **não** está na ART como métrica — a ART traz `valor_art` total. Logo, para subserviços medidos por unidade (BTN/m², kWp), `mediana` é do **valor total da ART**, não do valor por unidade. Registrar isso em `observacao`.

---

## 4. Regra de supressão `n < 5` no nível de subserviço

**[FATO VERIFICADO]** A regra `n < 5` já existe, mas hoje incide sobre o serviço amplo (`agregado_servicos_classe_a.csv`: serviços com n<5 recebem "Informação insuficiente para verificar").

**[RECOMENDAÇÃO]** Estender a mesma lógica ao novo nível de subserviço/complemento:
1. Calcular `n_arts_classe_a` por subserviço (e por complemento, se for eixo).
2. Se `n_arts_classe_a < 5`:
   - **não** publicar mediana/Q1/Q3/IQR;
   - preencher esses campos com **"Informação insuficiente para verificar"**;
   - `regra_n5_aplicada = sim`;
   - manter a **frequência** (contagem) visível — supressão é só do valor monetário, não do volume.
3. **Agregação ascendente (rollup):** quando um subserviço cai em `n < 5`, ele pode ser somado ao nível imediatamente acima (subgrupo→grupo→família) **apenas para frequência**. Para valor, o rollup só vale se o nível superior for homogêneo em unidade de referência; caso contrário, manter suprimido. Decisão de homogeneidade: **"Informação insuficiente para verificar"** até o de-para TOS↔unidade existir.

**[INFERÊNCIA TÉCNICA]** A razão estatística do limiar 5: medianas/quartis sobre n<5 não têm estabilidade amostral e podem ser dominadas por um único registro. Para honorários, publicar um valor frágil é pior que publicar "insuficiente". O limiar 5 é o já adotado no projeto; se o grupo quiser elevar (ex.: n<10 para publicação externa), é decisão de política — registrar como parâmetro configurável.

---

## 5. Coluna `observacao` — usos típicos

**[RECOMENDAÇÃO]** Valores padronizados para `observacao`:
- `"valor da ART, não honorário líquido"` (padrão para todos os valores).
- `"n < 5: sem base estatística para referência monetária"`.
- `"unidade física não extraível da ART; valor total"`.
- `"serviço novo / lacuna da tabela atual"`.
- `"mapeamento predominantemente aproximado; confiança reduzida"`.

---

## 6. Por que a regra deve descer de nível (resumo)

**[INFERÊNCIA TÉCNICA]**
- No nível de família ampla, a regra `n < 5` quase nunca dispara → **falsa sensação de robustez**.
- A tabela atual é por serviço (43 itens), não por 18 famílias → o cálculo precisa descer a esse nível para ser utilizável.
- Ao descer, subserviços raros aparecerão; sem a regra no nível certo, publicaríamos medianas instáveis. Logo, **a regra n<5 só protege se aplicada no nível de subserviço/complemento.**

---

## Síntese
Sair de 18 famílias para subserviços é o que dá aderência à tabela atual. O preço disso é a multiplicação de células com n pequeno — por isso `n < 5` deve operar no nível de subserviço/complemento, suprimindo valor (não frequência) e preferindo "Informação insuficiente para verificar" a um número frágil.
