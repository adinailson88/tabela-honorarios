# 02 — Diagnóstico da Metodologia Existente

> Análise dos arquivos da pasta `NOVA METODOLOGIA` e dos artefatos correlatos já produzidos
> (TABELA TOS, CidadessCalculo, Tabela de Honorários atual).
> Base documental verificável. Onde não foi possível confirmar pelos arquivos, está marcado
> **"Informação insuficiente para verificar"**.

---

## 1. Documentos analisados

| Arquivo | Pasta | Natureza |
|---|---|---|
| `Pré-Projeto tabela de honorários - SENGE.docx` (17/10/2024) | NOVA METODOLOGIA | Pré-projeto resumido (6 etapas, cronograma) |
| `Projeto tabela de honorários - SENGE.docx` (03/02/2025) | NOVA METODOLOGIA | Projeto completo (10 capítulos) |
| `TABELA TOS - 2.xlsx` | NOVO ARQUIVO | Protótipo de matriz atividade→valor médio/unidade |
| `CidadessCalculo atualizado 07.11.2024.xlsx` | SENGE | Modelo de regionalização com pesos (MCDM) |
| `Tabela honorarios Adinailson.docx/.xlsx` (ANTIGO e ATUALIZADO) | SENGE | Tabela vigente e seu reajuste por CUB |

---

## 2. Qual é a proposta atual (síntese fiel ao documento)

A metodologia **vigente** de atualização da tabela do SENGE/BA, conforme descrita no `Projeto tabela de honorários`, baseia-se no **Custo Unitário Básico (CUB)**:

> Preço Atualizado (R$/unidade) = Preço Anterior (R$/unidade) × CUB Atual (R$/m²) ÷ CUB Anterior (R$/m²)

- O CUB é divulgado mensalmente pelo SINDUSCON-BA.
- O documento cita a Lei 4.591/64 e a NBR 12.721/93 como base normativa do CUB.
  ⚠️ **Achado:** os PDFs do CUB na pasta SENGE referenciam **NBR 12.721:2006** (não "/93").
  Corrigir a citação para a versão vigente (confirmar em fonte oficial). Ver `dados/REFERENCIA_CUB.md`.
- **Dado verificável:** CUB R-1 Normal (Sinduscon-BA) Nov/2017 = R$1.724,35 → Jun/2024 = R$2.341,44 (**+35,8%**),
  enquanto a mediana observada nas ARTs subiu ~+57% (2017→2022): trajetórias **divergentes** — o CUB
  não é proxy fiel da evolução de honorários (grandezas distintas; comparação só de tendência).

A **nova metodologia proposta** pelo projeto organiza-se em torno de três eixos:

1. **Princípio da "Proporção de 1/3"** — em cada revisão: 1/3 manter o que funciona, 1/3 atualizar o existente, 1/3 inserir novos itens (ex.: energia fotovoltaica, automação).
2. **Pesquisa de preços colaborativa** — coleta com entidades de classe, mínimo de 5 preços por item, regionalizada, com unidades de medida adequadas (m², kVA, kWp, m³…).
3. **Governança e sustentabilidade** — comissão multidisciplinar presidida pelo SENGE; atualização anual; estratégias de monetização (publicidade, versão paga, app); curadoria final pelo SENGE.

O cronograma original previa conclusão entre fevereiro e setembro de 2025 (8–10 meses).

---

## 3. Critérios que aparecem na metodologia atual

- **Critério de reajuste:** índice CUB (correção monetária por fator multiplicativo).
- **Critério de cobertura:** categorização por serviço; unidade de medida por item.
- **Critério de representatividade (proposto):** ≥ 5 preços por item, variação regional, padrão de construção.
- **Critério de governança (proposto):** comissão + ciclo anual + consultas públicas.
- **Critério de regionalização (já prototipado em `CidadessCalculo`):** pesos sobre nº de engenheiros, remuneração média (TCM 2023), população IBGE, relação recurso/obra. *Isto é um modelo MCDM incipiente já existente.*

---

## 4. Lacunas identificadas

1. **Origem histórica não documentada.** O projeto registra literalmente "elaborada pelo engenheiro XXXXXXX no ano YYYY" — autoria e ano da primeira tabela estão em branco. → *Informação insuficiente para verificar.*

2. **CUB como único reajustador.** O próprio documento reconhece que o CUB "não acompanha mais fielmente a evolução dos preços". O CUB mede custo de **construção civil por m²**, não esforço/honorário profissional de todas as modalidades (elétrica, agronomia, segurança, mecânica). Aplicar um índice de construção a serviços de agronomia ou elétrica é frágil.

3. **Ausência de modelo de cálculo do valor-base.** A "Proporção de 1/3" organiza o *processo de revisão*, mas **não define como se chega ao valor de um item novo** além de "média de ≥5 preços". Não há fórmula de esforço técnico (homem-hora), nem ancoragem em piso salarial profissional (Lei 4.950-A/66 — *a confirmar por fonte oficial*).

4. **Pesquisa de preços ainda não executada.** Toda a etapa empírica depende de coleta futura com entidades. Enquanto isso, **a base de ARTs já disponível (726 mil registros de 2022) não está sendo usada como evidência** — é uma oportunidade desperdiçada.

5. **Risco concorrencial não tratado.** O documento fala em "padrão de mercado" e "aplicação uniforme em diferentes regiões", expressões que, sem ressalva, podem ser lidas como tabelamento/cartelização. Falta o enquadramento de **referência orientativa**, não impositiva.

6. **Monetização antes de validação.** O projeto detalha bastante a monetização (venda, app, patrocínio) — porém isso é secundário frente à fragilidade do método de cálculo, que é o que sustenta a defesa técnica perante o CREA-BA.

> **Ativo prévio relevante:** a aba "Honorários" da `TABELA TOS - 2.xlsx` já contém uma **matriz de
> 24.286 linhas** mapeando Código Nível + Código Atividade (CREA) → Cód. TOS → Descrição/grupo →
> Unidade → **Valor Médio/unidade**, e a aba "ARTs CREA 2022 (TOS)" traz o **de-para oficial de
> códigos**. Cópia derivada em `dados/tos_honorarios_existente.csv`. A proposta deve **reconciliar/calibrar**
> essa matriz contra a evidência observada (mediana/IQR), em vez de recomeçar.

7. **Desconexão entre os artefatos.** `TABELA TOS` (matriz atividade→valor médio por ART), `CidadessCalculo` (regionalização) e `Projeto` (texto) existem **em paralelo, sem integração metodológica declarada**. Eles deveriam ser as três camadas de um mesmo modelo.

---

## 5. O que precisa ser melhor fundamentado

- **Definição do valor-base de cada item**: passar de "média de 5 preços" para um modelo explícito (esforço técnico × valor-hora de referência + custos + risco), com a pesquisa de preços e as ARTs servindo de **calibração e validação cruzada**, não de fonte única.
- **Justificativa do(s) índice(s) de atualização**: avaliar manter CUB para itens de construção e adotar índices/critérios distintos por modalidade.
- **Tratamento estatístico das ARTs**: mediana e intervalo interquartil por atividade/unidade/região (a ART tem outliers extremos — ver doc. 03).
- **Enquadramento jurídico-concorrencial**: posicionar como parâmetro técnico orientativo e instrumento anti-aviltamento, com base no piso profissional, sem imposição de preço.

---

## 6. Riscos técnicos

| Risco | Descrição | Severidade |
|---|---|---|
| Índice inadequado | CUB aplicado a modalidades não-construção | Alta |
| Valor sem rastreabilidade | "Média de 5 preços" sem critério amostral documentado | Alta |
| Outliers de ART | Valores de ART variam de R$0,01 a centenas de bilhões (erros/heterogeneidade) | Alta |
| Mistura de unidades | Mesmo serviço em m², unidade, kVA… dificulta comparação | Média |
| Cobertura incompleta | Serviços emergentes ausentes da tabela atual | Média |

## 7. Riscos institucionais

| Risco | Descrição | Severidade |
|---|---|---|
| Leitura concorrencial | Tabela vista como tabelamento/cartel | Alta |
| Dependência de coleta futura | Método trava sem a pesquisa de preços das entidades | Média |
| Baixa adesão | Sem validação técnica robusta, CREA-BA/entidades podem não chancelar | Média |
| Foco em monetização | Pode soar como interesse comercial antes do interesse técnico | Média |

## 8. Oportunidades de melhoria

1. **Integrar os três artefatos** em um modelo de 3 camadas: (a) matriz de atividades (TOS), (b) valor-base por esforço técnico, (c) ajuste regional (CidadessCalculo/MCDM).
2. **Usar as ARTs de 2022 como evidência empírica de mercado** — agregada e anonimizada — para calibrar/validar faixas, em vez de partir do zero.
3. **Substituir "valor único" por "faixas de honorários"** (piso–referência–teto) por mediana e IQR, mais defensável e menos exposto à crítica concorrencial.
4. **Adotar governança documentada** (ciclo anual + nota técnica + versionamento), aproveitando a comissão já prevista.
5. **Reposicionar o discurso**: valorização profissional e combate ao aviltamento, com base no piso da Lei 4.950-A/66 *(a confirmar)*, em vez de "padrão de mercado uniforme".

---

*Documento derivado. Não altera os arquivos originais.*
