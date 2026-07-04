# Diagnóstico do bucket "Não mapeado"

**Frente:** SENGE-BA — Nova metodologia de tabela de honorários
**Data:** 2026-06-24
**Natureza:** documento de diagnóstico. Não altera base, não reclassifica.

> Convenção: **[FATO VERIFICADO]**, **[INFERÊNCIA TÉCNICA]**, **[RECOMENDAÇÃO]**.
> Onde não há base local: **"Informação insuficiente para verificar"**.

---

## 1. Tamanho do bucket

**[FATO VERIFICADO]** (`frequencia_total_servicos.csv`):
- "Não mapeado" — `freq_total` = **102.554** ARTs.
- É a maior categoria isolada da base, à frente de "Microgeração/Fotovoltaica" (31.811) e "Composto (múltiplos serviços)" (30.139).

## 2. Percentual da base

**[FATO VERIFICADO]** 102.554 / 230.928 = **≈ 44,4%** do total de ARTs.
**[INFERÊNCIA TÉCNICA]** Em termos práticos, **quase metade dos registros** não tem serviço identificado. Soma-se a isso o bucket "Composto (múltiplos serviços)" (30.139; ≈13,1%), que também não é um serviço atribuível.

## 3. Quantidade Classe A no "Não mapeado"

**[FATO VERIFICADO]:**
- Classe A em "Não mapeado": **19.975** (`frequencia_total_servicos.csv` e `agregado_servicos_classe_a.csv`).
- Total Classe A: 53.190.
- Logo, **≈ 37,6% de toda a base monetária Classe A** está em "Não mapeado".
- Estatística do bucket (Classe A): mediana **R$ 2.200**, Q1 R$ 1.000, Q3 R$ 15.000, max **R$ 819.308.220**, 898 municípios, 88 modalidades.

## 4. Por que isso é crítico

**[INFERÊNCIA TÉCNICA]**
1. **Cobertura monetária insuficiente:** mais de 1/3 do "combustível" do cálculo (Classe A) está sem serviço. Qualquer mediana por serviço hoje é calculada sobre ~62% da base A efetivamente atribuída.
2. **Viés de seleção desconhecido:** não se sabe *quais* serviços estão escondidos no bucket. Se atividades de alto valor (ou de baixo valor) estiverem concentradas ali, as medianas dos serviços já mapeados estão enviesadas.
3. **Heterogeneidade extrema:** 88 modalidades e max de R$ 819 mi no próprio bucket indicam que ele mistura tudo — de taxas simbólicas a valores de contrato de obra.
4. **Risco reputacional:** apresentar uma metodologia "por serviço" em que ~45% não tem serviço fragiliza a defesa técnica perante CREA/contratantes.

## 5. Como afeta a mediana por serviço

**[INFERÊNCIA TÉCNICA]**
- As medianas atuais são de **serviços já capturados**; são estáveis ao desbloquear o bucket apenas se as ARTs hoje "Não mapeadas" se distribuírem proporcionalmente. Não há garantia disso.
- **Exemplo de mecanismo:** se parte do "Não mapeado" for, na verdade, "Instalações Elétricas" de baixo valor, a mediana de Instalações Elétricas (hoje R$ 2.500) tende a **cair** ao incorporá-las. O sentido e a magnitude do deslocamento são, hoje, **"Informação insuficiente para verificar"** — só o refinamento dirá.

## 6. Como afeta a identificação de novos serviços

**[INFERÊNCIA TÉCNICA]**
- Serviços novos/lacunas já emergiram **apesar** do bucket (Fotovoltaica, Receituário, Ambiental, Topografia, Segurança do Trabalho). Isso é um acerto.
- Porém, novos serviços ainda **não nomeados** estão provavelmente ocultos dentro do "Não mapeado". Reduzir o bucket é a via para descobrir lacunas adicionais da tabela atual de forma sistemática, e não só por palavras-chave já previstas.

## 7. Como afeta a tabela de honorários

**[INFERÊNCIA TÉCNICA]**
- A tabela atual é **organizada por serviço** (43 serviços, 13 famílias). Para atualizá-la dinamicamente via ARTs, é preciso *casar* atividade declarada → serviço da tabela.
- Com 45% sem mapeamento, a atualização dinâmica cobre hoje menos da metade dos serviços com lastro estatístico próprio. A tabela ficaria parcialmente "alimentada" e parcialmente estática.

## 8. Que tipo de refinamento é necessário

**[RECOMENDAÇÃO]** (detalhe operacional em `ESPECIFICACAO_REFINAMENTO_TOS.md`):
1. **Verificar o `codigo_atividade`:** a base **já tem** um campo numérico `codigo_atividade` (ex.: `3367`). Antes de mexer em palavras-chave, testar se esse código permite mapear via tabela oficial. *Se é código TOS/CREA padronizado:* "Informação insuficiente para verificar" — precisa cruzar com a TOS oficial.
2. **Mapear por código (TOS) antes de por texto:** mapeamento por código é exato; por palavra-chave é aproximado. Priorizar `grupo_tos`/`subgrupo_tos`/`servico_tos`.
3. **Expandir o dicionário de palavras-chave** apenas para o resíduo que não tiver código.
4. **Marcar nível de confiança do mapeamento** (exato / aproximado / manual / não mapeado) para que a mediana por serviço carregue a qualidade do mapeamento que a originou.
5. **Tratar "Composto (múltiplos serviços)"** à parte — não é "não mapeado", é multi-serviço; precisa de regra de ponderação (já há `METODO_PONDERACAO_SERVICOS_COMPOSTOS.md` na pasta a ser cruzado).
6. **Meta operacional sugerida:** reduzir "Não mapeado" para um patamar em que a base A atribuída cubra a maioria dos serviços da tabela atual. O número-alvo exato deve ser decidido pelo grupo técnico — **"Informação insuficiente para verificar"** qual patamar é aceitável institucionalmente.

---

## Síntese
O bucket "Não mapeado" (≈44,4% da base; ≈37,6% da base A) é o **gargalo central** da metodologia. Ele não invalida o desenho, mas **limita a cobertura e a credibilidade** do cálculo por serviço. O caminho é mapeamento por código (TOS) antes de texto, com marcação de confiança — não retrabalho do dashboard.
