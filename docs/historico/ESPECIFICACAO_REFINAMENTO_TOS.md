# Especificação de refinamento por TOS (Tabela de Obras e Serviços)

**Frente:** SENGE-BA — Nova metodologia de tabela de honorários
**Data:** 2026-06-24
**Natureza:** especificação técnica. Não implementa, não roda pipeline, não reclassifica.
**Objetivo:** definir como usar a TOS para reduzir o bucket "Não mapeado" e dar lastro por código (não só por palavra-chave).

> Convenção: **[FATO VERIFICADO]**, **[INFERÊNCIA TÉCNICA]**, **[RECOMENDAÇÃO]**.
> Onde não há base local: **"Informação insuficiente para verificar"**.
> O que é TOS: Tabela de Obras e Serviços do sistema CONFEA/CREA. **A presença e o formato oficial da TOS nos arquivos locais: "Informação insuficiente para verificar"** — esta especificação assume que a TOS oficial será localizada/recebida antes da implementação.

---

## 1. Verificar se há código TOS (ou equivalente) na base de ARTs

**[FATO VERIFICADO]**
- A base `base_classe_a_servicos_metodologia.csv` **já contém** uma coluna `codigo_atividade` numérica, populada (ex.: `3367`), derivada de `parts[8]` do CSV de ARTs em `gerar_metodologia_servicos.py`.
- Há também `qtd_codigos_atividade_art` (quantos códigos distintos a ART tem).

**[INFERÊNCIA TÉCNICA]** Existe um código de atividade por linha. Se esse código for o código TOS/CREA oficial (ou mapeável para ele), o mapeamento atividade→serviço pode passar de ~55% (palavra-chave) para cobertura quase total por **lookup determinístico**.

**[RECOMENDAÇÃO] Passo 0 (verificação, sem reclassificar):**
1. Extrair a lista de `codigo_atividade` distintos da base e suas frequências.
2. Cruzar com a TOS oficial (quando localizada).
3. Reportar taxa de match: % de ARTs cujo `codigo_atividade` casa com um código TOS válido.
4. Decidir, com base nessa taxa, se o código é eixo primário de mapeamento. Enquanto a TOS oficial não for confirmada: **"Informação insuficiente para verificar"** se `codigo_atividade` é TOS.

---

## 2. Mapear atividade declarada → estrutura TOS

**[RECOMENDAÇÃO]** Estrutura hierárquica alvo (nomes de campo padronizados):

| Campo novo | Conteúdo | Fonte |
|---|---|---|
| `grupo_tos` | Grupo da TOS | lookup por `codigo_atividade` na TOS |
| `subgrupo_tos` | Subgrupo da TOS | idem |
| `servico_tos` | Obra/serviço TOS | idem |
| `complemento_tos` | Complemento/qualificador TOS | idem |
| `servico_honorarios_padronizado` | Serviço equivalente na **tabela atual do SENGE** | tabela de-para TOS↔tabela atual |
| `nivel_confianca_mapeamento` | exato / aproximado / manual / nao_mapeado | regra abaixo |

**[INFERÊNCIA TÉCNICA]** A TOS é a chave técnica (linguagem CONFEA/CREA); a tabela do SENGE é a chave comercial/orientativa. Os dois eixos devem coexistir: TOS para precisão e auditabilidade; serviço SENGE para continuidade da tabela atual.

---

## 3. Definição dos campos TOS

**[RECOMENDAÇÃO]**
- `grupo_tos`, `subgrupo_tos`, `servico_tos`, `complemento_tos`: preenchidos **somente** por lookup determinístico no código. Sem código válido → "Informação insuficiente para verificar".
- Nunca inventar código, grupo, subgrupo ou complemento TOS. Se a TOS oficial não trouxer o nível (ex.: complemento), deixar "Informação insuficiente para verificar".

---

## 4. `servico_honorarios_padronizado` (preservar a tabela atual do SENGE)

**[FATO VERIFICADO]** A tabela atual tem 13 famílias e 43 serviços; já existe `MATRIZ_SERVICOS_TABELA_ATUAL.csv` e `MATRIZ_TABELA_ATUAL_X_ARTS.csv` na pasta.
**[RECOMENDAÇÃO]**
- Construir uma **tabela de-para** `servico_tos` → `servico_honorarios_padronizado`, ancorada nos 43 serviços existentes.
- **Não criar serviço novo na tabela SENGE silenciosamente.** Quando uma atividade TOS não tiver serviço correspondente na tabela atual, marcar como **candidato a novo serviço** (lacuna), não forçar encaixe. Isso preserva e ao mesmo tempo evolui a tabela.
- Os serviços já evidenciados como lacuna (Fotovoltaica, Receituário, Topografia, Ambiental, Segurança do Trabalho) entram como candidatos formais.

---

## 5. `nivel_confianca_mapeamento` (4 níveis)

**[RECOMENDAÇÃO]** Definição operacional:

| Nível | Critério | Uso permitido |
|---|---|---|
| **exato** | mapeado por `codigo_atividade` casando com TOS oficial | cálculo monetário (se classe A) |
| **aproximado** | sem código válido, mapeado por palavra-chave do dicionário | frequência + cálculo com ressalva |
| **manual** | mapeado por decisão humana documentada (de-para revisado) | conforme decisão registrada |
| **nao_mapeado** | sem código e sem palavra-chave | apenas diagnóstico/volume |

**[INFERÊNCIA TÉCNICA]** Esse campo deve **propagar** para o agregado: uma mediana por serviço calculada majoritariamente sobre mapeamentos "aproximados" deve ser sinalizada com confiança menor que uma calculada sobre "exatos".

---

## 6. Separar mapeamento exato, aproximado, manual e não mapeado

**[RECOMENDAÇÃO]** No relatório de validação, reportar para cada serviço:
- nº de ARTs por nível de confiança;
- % exato; % aproximado; % manual; % não mapeado;
- e o impacto na mediana (mediana com só exatos vs. mediana com todos).

Isso torna a metodologia **auditável**: cada número carrega a procedência do mapeamento.

---

## 7. Cruzar TOS com a tabela atual de honorários

**[RECOMENDAÇÃO]** Produzir uma matriz `MATRIZ_TOS_X_TABELA_ATUAL.csv` (nome sugerido) com:
`codigo_tos; grupo_tos; subgrupo_tos; servico_tos; servico_honorarios_padronizado; familia_senge; unidade_referencia_tabela_atual; status_correspondencia (exata/parcial/lacuna)`
- **status = lacuna** identifica serviço da TOS sem correspondência na tabela atual → backlog de serviços novos.
- **status = parcial** identifica serviço da tabela atual cuja unidade de referência (BTN/m², kWp, hora, % CUB) não é diretamente extraível da ART → exige tratamento à parte.

**[FATO VERIFICADO]** A tabela atual usa unidades BTN/m², BTN/m³, BTN/km, BTN/ha, hora, % do CUB e valor fixo. As ARTs trazem **valor total da ART**, não a métrica física (área, potência, extensão). Logo, para serviços medidos por unidade física, a ART dá ordem de grandeza, **não** o valor unitário — registrar essa limitação na matriz.

---

## 8. Restrições inegociáveis
- Não alterar arquivos existentes; gerar novos artefatos `_TOS`.
- Não tratar `valor_art` como honorário líquido.
- Não somar linhas da mesma ART.
- Não inventar códigos TOS, serviços, subgrupos, normas ou municípios.
- Onde não verificável: "Informação insuficiente para verificar".

---

## Síntese
O refinamento TOS é **lookup por código antes de palavra-chave**, com de-para explícito para a tabela SENGE e marcação de confiança em 4 níveis. A base já tem `codigo_atividade`; o passo crítico inicial é confirmar se ele casa com a TOS oficial — antes disso, a magnitude do ganho é "Informação insuficiente para verificar".
