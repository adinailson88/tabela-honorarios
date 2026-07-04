# 04 — Modelo Conceitual da Tabela de Honorários

> Proposta de **modelo conceitual** (arquitetura do método), não de valores.
> Nenhum valor monetário é inventado. Onde o cálculo depende de dado ainda não disponível,
> está marcado **"Informação insuficiente para verificar"**.

---

## 1. Princípio orientador

A tabela **não é uma lista de preços**, e sim um **modelo de governança de honorários**:
um instrumento técnico **orientativo** que estima o esforço profissional de referência e
**combate o aviltamento**, sem impor preço (ver cuidados concorrenciais no doc. 08).

A proposta integra, numa única arquitetura, os três artefatos já existentes:

| Camada | Artefato existente que a origina | Papel |
|---|---|---|
| (A) Catálogo de atividades | `TABELA TOS - 2.xlsx` (Nível+Atividade CREA → Cód. TOS) | O que se precifica |
| (B) Valor-base por esforço | a construir (este documento) | Quanto vale o esforço técnico |
| (C) Ajuste regional | `CidadessCalculo` (pesos MCDM por cidade) | Onde se presta o serviço |
| (D) Calibração empírica | `ARTs 2022` (mediana/IQR) | Conferência com o mercado |

---

## 2. Estrutura de três camadas + calibração

```
VALOR DE REFERÊNCIA (faixa) =
    [ Valor-base por esforço técnico (B) ]
    × [ Fator de complexidade/porte/risco ]
    × [ Fator regional (C) ]
    ⟶ validado contra a faixa observada nas ARTs (D)
```

O resultado **não é um número único**, mas uma **faixa** (piso técnico – referência – teto),
o que é mais defensável tecnicamente e juridicamente.

---

## 3. Dimensões consideradas (e como entram no modelo)

| Dimensão | Como entra | Fonte de dado |
|---|---|---|
| **Tipo de atividade** | Define o item (catálogo CREA Nível+Atividade) | TABELA TOS / códigos CREA |
| **Complexidade técnica** | Multiplicador (baixa/média/alta) | A definir pela comissão; calibrar com IQR das ARTs |
| **Responsabilidade profissional** | Componente do valor-hora e do risco | Piso profissional *(Lei 4.950-A/66 — a confirmar)* |
| **Porte do empreendimento** | Faixas por quantidade (m², kWp, ha…) | Campo `quantidade`+`unidade` das ARTs |
| **Localidade** | Fator regional | CidadessCalculo + `cidade_obra` |
| **Tempo técnico estimado** | Núcleo do valor-base (homem-hora) | Parâmetros de engenharia / comissão |
| **Custo operacional** | Adicional sobre o valor-hora | Comissão / pesquisa de preços |
| **Risco profissional** | Multiplicador de risco | Comissão (ART de obras de risco) |
| **Valor de referência de mercado** | Calibração/validação | ARTs (mediana/IQR) + pesquisa de preços |
| **Piso técnico** | Limite inferior anti-aviltamento | Piso profissional + custo mínimo |
| **Faixas de honorários** | Saída do modelo (P25–mediana–P75) | ARTs + modelo |
| **Atualização monetária** | Reajuste periódico | CUB (construção) / índices por modalidade |
| **Revisão periódica** | Governança anual | Comissão SENGE |

---

## 4. O valor-base por esforço técnico (camada B)

Estrutura conceitual proposta (a parametrizar com a comissão):

```
Valor-base do item = Tempo técnico estimado (h) × Valor-hora de referência (R$/h)
                     + Custos operacionais diretos
Valor-hora de referência: ancorado no piso profissional vigente
   (Lei 4.950-A/66 — base de 6 salários mínimos para jornada padrão — A CONFIRMAR por fonte oficial)
```

> **Informação insuficiente para verificar:** os valores numéricos de tempo técnico por atividade
> e o valor-hora final dependem (a) da definição da comissão e (b) da pesquisa de preços.
> **Não devem ser inventados.** A tabela só recebe número após esse insumo.

---

## 5. Fatores multiplicadores (camada de ajuste)

| Fator | Faixa conceitual | Critério |
|---|---|---|
| Complexidade | baixa / média / alta | Definição técnica + IQR observado |
| Porte | por faixas de quantidade | Quartis de `quantidade` por unidade nas ARTs |
| Risco | normal / elevado | Tipo de obra/serviço |
| Regional | índice por município/região | Modelo MCDM de `CidadessCalculo` |

Os **valores numéricos** dos multiplicadores são **parâmetros a calibrar** — não inventados aqui.

---

## 6. Saída: faixas, não preço único

Para cada item (atividade × unidade × região), a tabela apresenta:

- **Piso técnico** — limite anti-aviltamento (não descer abaixo do custo + piso profissional).
- **Valor de referência** — estimativa central (mediana calibrada).
- **Teto orientativo** — referência superior (P75 observado / alta complexidade).

Faixas reduzem o risco concorrencial (não é "o preço", é "a referência de esforço")
e absorvem a heterogeneidade real do mercado.

---

## 7. Atualização monetária

- **Itens de construção civil:** manter CUB/m² (já consolidado, SINDUSCON-BA).
- **Itens de outras modalidades** (elétrica/kVA-kWp, agronomia/ha, etc.): avaliar índice
  mais aderente (ex.: variação do piso profissional, INCC, índices setoriais) —
  *escolha a ser fundamentada por fonte oficial; não definida aqui.*
- Registrar a fórmula e a data-base de cada reajuste (rastreabilidade).

---

## 8. Critérios de revisão periódica (governança)

1. Ciclo **anual** de revisão (manter/atualizar/inserir — Proporção de 1/3 do projeto).
2. **Nota técnica** a cada revisão documentando fonte, fórmula e data-base.
3. **Recalibração** das faixas contra a base de ARTs do ano mais recente.
4. **Versionamento** público (v1, v2…) e changelog.
5. Revisões emergenciais para tecnologias novas (ex.: novos serviços fotovoltaicos).

---

## 9. Como este modelo corrige as lacunas do diagnóstico (doc. 02)

| Lacuna (doc. 02) | Correção neste modelo |
|---|---|
| Valor sem rastreabilidade | Valor-base explícito (esforço × hora) + calibração documentada |
| CUB para tudo | Índice por modalidade; CUB só onde faz sentido |
| ART ignorada | ART vira camada de calibração/validação (D) |
| Risco concorrencial | Faixas orientativas + foco anti-aviltamento |
| Artefatos desconectados | Integração TOS + esforço + CidadessCalculo |
| Valor único | Faixas (piso–referência–teto) |

---

*Documento derivado. Não altera os arquivos originais. Nenhum valor monetário foi inventado.*
