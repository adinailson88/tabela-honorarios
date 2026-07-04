# Diagnóstico do significado de `codigo_atividade` e do Código TOS

**Frente:** SENGE-BA — Nova metodologia de tabela de honorários
**Data:** 2026-06-24
**Natureza:** diagnóstico. Não altera arquivos originais.

> Convenção: **[FATO VERIFICADO]**, **[INFERÊNCIA TÉCNICA]**, **[RECOMENDAÇÃO]**.
> Onde não há base local: **"Informação insuficiente para verificar"**.

---

## 1. Há dois códigos distintos (não confundir)

**[FATO VERIFICADO]** Verificando o cabeçalho da base original (`ARTs 2022 01022024.csv`) e a aba TOS (`ARTs CREA 2022 (TOS)`), existem **códigos diferentes**:

| Código | Onde aparece | Exemplos | O que é |
|---|---|---|---|
| `codigo` (base original) → campo `codigo_atividade` do pipeline anterior | `ARTs 2022 01022024.csv`, coluna `codigo` | `73`, `3367` | Código **interno de atividade** do CREA, inteiro simples |
| `Código Atividade Profissional` (aba TOS) | `TABELA TOS - 2.xlsx` | `44`, `24`, `40`, `80` | Código do **verbo/atividade profissional** (ex.: 44 = Execução de desenho técnico) |
| **`CÓDIGO TOS`** (aba TOS) | `TABELA TOS - 2.xlsx` | `34.6.1.2`, `2.1.1`, `42.1.15` | Código **hierárquico da TOS** (grupo.subgrupo.obra/serviço) |

## 2. Exemplos de códigos e descrições associadas

**[FATO VERIFICADO]** Resolução do `CÓDIGO TOS` contra a hierarquia (`Table 1`):
- `34.6.1.2` → Grupo **Geodésia** / Subgrupo **Georreferenciamento** / Serviço **rural**
- `2.1.1` → Grupo **Estruturas** / Subgrupo **Estruturas de Concreto e Argamassa Armada** / Serviço **de estrutura de concreto armado**
- `42.1.15` → Grupo **Prevenção e Controle de Riscos** / Subgrupo **Gerenciamento e Controle de Riscos** / Serviço **de Programa de Gerenciamento de Riscos (PGR)**
- `1.1.1.1` → Grupo **Construção Civil** / Subgrupo **Edificações** / Serviço **de alvenaria**
- `7.6.2` → Grupo **Meio Ambiente** / Subgrupo **Gestão Ambiental** / Serviço **de viabilidade ambiental**

## 3. Há match com alguma tabela local?

**[FATO VERIFICADO]**
- O `CÓDIGO TOS` da aba `ARTs CREA 2022 (TOS)` casa **100%** com a hierarquia da aba `Table 1` (mesmo arquivo). Todas as 182.261 linhas têm Código TOS, e todas resolvem a um Grupo.
- O `codigo_atividade` (código interno `73`/`3367`) da base original **não é** o Código TOS e **não foi** usado para o mapeamento TOS — ele é apenas o código de atividade do CREA, mais pobre.

## 4. Percentual de códigos mapeados (camada TOS)

**[FATO VERIFICADO]** (subconjunto de 59.764 ARTs / 182.261 linhas):
- Linhas com `CÓDIGO TOS`: **100,0%**.
- Linhas cujo Código TOS resolve a Grupo/Subgrupo/Serviço pela `Table 1`: **100,0%**.
- ARTs com pelo menos um Código TOS: **59.764 / 59.764 (100%)**.

## 5. Percentual não mapeado

**[FATO VERIFICADO]**
- No **nível TOS** (grupo/subgrupo/serviço): **0,0%** "não mapeado" dentro da camada TOS.
- No **nível tabela SENGE** (de-para TOS → 43 serviços atuais): **15,3%** (9.164 ARTs) ainda **sem correspondência** na tabela atual → marcadas como **"candidato a novo serviço"**, não como erro.
- **Fora da camada TOS** (170.+ mil ARTs do universo de 230.928 não presentes na aba): Código TOS = **"Informação insuficiente para verificar"**.

## 6. Conclusão

**[FATO VERIFICADO]**
- O campo `codigo_atividade` da **base original** (`73`/`3367`): **NÃO usa TOS** — é o código interno de atividade do CREA.
- O arquivo `TABELA TOS - 2.xlsx`: **USA TOS** — traz `CÓDIGO TOS` hierárquico, 100% resolvível, para um **subconjunto** de 59.764 ARTs de 2022.

**[RECOMENDAÇÃO]**
1. Adotar o `CÓDIGO TOS` (do xlsx) como **eixo primário** de mapeamento — é determinístico e auditável.
2. Manter o `codigo_atividade` (CREA) e o `Código Atividade Profissional` como atributos secundários na base nova.
3. Buscar, em rodada futura, o arquivo-fonte que mapeie TOS para **todas** as 230.928 ARTs (hoje só 59.764 estão cobertas). Enquanto não existir: "Informação insuficiente para verificar" para o restante.
