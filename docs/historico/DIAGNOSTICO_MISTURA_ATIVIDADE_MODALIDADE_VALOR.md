# Diagnóstico da Mistura entre Atividade, Modalidade e Valor nas ARTs

**Frente:** Metodologia da tabela de honorários — SENGE-BA / CREA-BA
**Base analisada:** "ARTs 2022 01022024.csv" (pasta *ARTS Adinailson*), exercício de referência 2022.
**Caráter do documento:** subsídio metodológico de natureza orientativa. Não estabelece preço obrigatório, preço mínimo compulsório nem tabela vinculante.
**Natureza dos dados:** somente agregados. Não há exposição de dados pessoais, de profissionais, empresas ou contratantes, nem ranking de qualquer natureza.

---

## Como ler este diagnóstico

Cada resposta separa três planos:

- **FATO VERIFICADO** — número calculado diretamente do arquivo nesta sessão.
- **INFERÊNCIA TÉCNICA** — interpretação/classificação a partir dos fatos.
- **RECOMENDAÇÃO** — proposta de uso na governança de honorários.

Onde a base não permite confirmar, está escrito literalmente **"Informação insuficiente para verificar"**.

**Mensagem central deste diagnóstico (FATO VERIFICADO):** o campo `valor_contrato` é o valor da **ART inteira**, replicado em cada linha de atividade — **não** é o valor de cada atividade isolada. Somar as linhas de uma ART multiplica o valor indevidamente.

---

## Estrutura do arquivo (referência para as respostas)

**FATO VERIFICADO** — Campos do CSV (separador `;`): `id`; `tipo_art`; `formaderegistro`; `emissao`; `cidade_obra`; `uf`; `titulos`; `entidade`; `codigo`; `atividade`; `quantidade`; `unidade`; `valor_contrato`; `ano_registro_profissional` (+4 colunas vazias de exportação).

**FATO VERIFICADO** — Volume: 726.028 linhas de atividade; 230.928 ARTs distintas (por `id`).

**Observação técnica de parsing (FATO VERIFICADO):** o campo `atividade` contém `;` internos; o parsing exige ancoragem pela direita para não desalinhar colunas.

---

## As 15 perguntas

### (1) Quais campos representam a ATIVIDADE?

**FATO VERIFICADO.** A atividade está em dois campos combinados:
- `atividade` — texto livre, padrão `"Nivel - X  Atividade - Y - DESCRICAO"`.
- `codigo` — código da atividade.

**INFERÊNCIA TÉCNICA.** O `codigo` é a chave estável para agrupar/contar atividades; o texto livre de `atividade` serve para rotulagem e para detectar vocabulário de serviços novos (ver pergunta 7 e o tópico de serviços ausentes na tabela).

---

### (2) Quais campos representam a MODALIDADE?

**FATO VERIFICADO.** A modalidade/título profissional do responsável está no campo `titulos` (ex.: "Engenheiro Civil"). É o título profissional do responsável pela ART.

---

### (3) Quais campos representam a FORMAÇÃO?

**FATO VERIFICADO.** Não há campo específico e separado de "formação acadêmica" distinto da modalidade. O campo que carrega a formação/título profissional é o mesmo `titulos` (ex.: "Engenheiro Civil", "Agrônomo", "Engenheiro Eletricista").

**INFERÊNCIA TÉCNICA.** Nesta base, formação e modalidade colapsam no mesmo campo `titulos`. Distinguir "formação" de "modalidade de atuação" como atributos independentes: **Informação insuficiente para verificar** (a base não traz os dois separadamente).

---

### (4) Quais campos representam o VALOR?

**FATO VERIFICADO.** O valor está em `valor_contrato`. Há ainda `quantidade` e `unidade`, que descrevem a dimensão física do serviço (ver pergunta 11), mas o valor monetário é `valor_contrato`.

---

### (5) Há identificador único de ART?

**FATO VERIFICADO.** Sim. O campo `id` identifica unicamente a ART. São 230.928 `id` distintos no arquivo.

---

### (6) Uma ART pode aparecer em mais de uma linha?

**FATO VERIFICADO.** Sim.
- 62,6% das ARTs são multi-linha (144.541 de 230.928).
- 37,4% são de linha única (86.387).

**INFERÊNCIA TÉCNICA.** A unidade analítica correta para qualquer cálculo monetário é a **ART (`id`)**, não a linha. Trabalhar por linha, sem deduplicar por `id`, contamina maioria da base (a maior parte das ARTs é multi-linha).

---

### (7) Uma ART pode ter mais de uma atividade?

**FATO VERIFICADO.** Sim. 26,5% das ARTs (61.284) têm mais de um `codigo` de atividade distinto — ou seja, escopo composto.

**INFERÊNCIA TÉCNICA.** Em mais de um quarto das ARTs, o registro reúne serviços diferentes sob um mesmo `id` e um mesmo valor. Esse é o núcleo do problema de "mistura": não se sabe quanto do valor cabe a cada serviço (ver perguntas 11 e 12).

---

### (8) Uma ART pode ter mais de uma modalidade?

**FATO VERIFICADO.** Não nesta base. Cada ART carrega exatamente um título/modalidade no campo `titulos` (multi-modality = 0%).

**INFERÊNCIA TÉCNICA.** A mistura entre modalidades **não** aparece no campo `titulos`. Quando há mistura, ela se manifesta de duas formas: (a) por múltiplos `codigo` de atividade dentro da mesma ART (escopo composto, pergunta 7); e (b) no nível do catálogo — o mesmo serviço figurando em catálogos de modalidades diferentes. Não se deve inferir interdisciplinaridade a partir de `titulos`.

---

### (9) Uma ART pode ter mais de uma formação?

**INFERÊNCIA TÉCNICA.** Como formação e modalidade colapsam no mesmo campo `titulos` (pergunta 3) e este traz exatamente um valor por ART (multi-modality = 0%, pergunta 8), a base atribui **uma única** formação/título por ART. Multiplicidade de formação por ART: **Informação insuficiente para verificar** — a base não registra mais de uma formação por `id`.

---

### (10) O valor se repete em várias linhas da mesma ART?

**FATO VERIFICADO.** Sim, predominantemente. Entre as ARTs multi-linha:
- 99.982 têm valor **constante** em todas as linhas (o mesmo valor repetido);
- apenas 2.080 variam o valor entre linhas.

**Exemplo real verificado:** ART `id` 2399866 tem 2 linhas (Laudo e Vistoria), ambas com `valor_contrato` 433.795,00 replicado.

---

### (11) O valor parece ser da ART inteira ou da linha/atividade?

**FATO VERIFICADO / CONCLUSÃO.** O `valor_contrato` é o valor da **ART inteira**, replicado em cada linha de atividade — **não** é o valor por atividade. A evidência:
- a replicação do mesmo valor em 99.982 ARTs multi-linha (pergunta 10);
- o exemplo da ART 2399866 (mesmo 433.795,00 em "Laudo" e "Vistoria");
- a mediana **por linha** (~R$ 1.570) difere da mediana **por ART** (R$ 1.800), justamente porque a replicação infla a contagem das linhas das ARTs multi-linha.

**RECOMENDAÇÃO.** Somar linhas multiplica o valor indevidamente. Todo cálculo monetário deve ser feito após deduplicar por `id`.

---

### (12) Dá para saber quanto do valor é de cada serviço?

**FATO VERIFICADO.** Não, no caso geral. Quando a ART tem múltiplos `codigo` de atividade e um único valor replicado (26,5% das ARTs têm mais de um código, pergunta 7), o valor é da ART e não há campo que reparta o montante por serviço.

**INFERÊNCIA TÉCNICA.** A atribuição de valor a um serviço específico só é direta quando a ART tem **um único** código de atividade. Repartir o valor de ARTs compostas exigiria critério de rateio que a base **não** fornece. Rateio por serviço em ARTs compostas: **Informação insuficiente para verificar**.

---

### (13) Quais casos são SEGUROS para cálculo monetário?

**INFERÊNCIA TÉCNICA / operacional** (computada sobre os 230.928 `id`):

- **Classe A — linha única, 1 código, 1 valor plausível: 53.190 ARTs (23,0%).**
  Distribuição de valor da Classe A: mediana R$ 2.000; P25 R$ 800; P75 R$ 8.000; P90 R$ 145.363.
  É a base **primária** para serviços frequentes: nela o valor da ART corresponde, sem ambiguidade, a uma única atividade.

- **Classe B homogênea — multi-linha, mesmo código de atividade, valor constante: 38.631 ARTs (16,7%).**
  É a mesma atividade repetida. Serve como base **secundária / de simulação**, com regra explícita (o valor é da ART, atribuível à atividade única que se repete).

**RECOMENDAÇÃO.** Para serviços **frequentes**, usar Classe A como base primária e Classe B como apoio. Para serviços **raros**, aplicar supressão estatística (n < 5) e escrever "Informação insuficiente para verificar" em vez de divulgar parâmetro instável.

---

### (14) Quais casos são AMBÍGUOS?

**INFERÊNCIA TÉCNICA / operacional:**

- **Classe C — composta ambígua: multi-linha, múltiplos códigos, valor único replicado: 60.247 ARTs (26,1%).**
  Não dá para atribuir o valor a um serviço específico (pergunta 12).
  **Uso permitido:** apenas frequência e detecção de serviços novos. **Uso vedado:** cálculo monetário por serviço.

- **Valor que varia entre linhas: multi-linha com valor diferente entre linhas: 2.080 ARTs (0,9%).**
  Caso minoritário e de leitura incerta (não se sabe se a variação é por atividade, por etapa ou por erro de digitação).
  Natureza exata da variação por linha: **Informação insuficiente para verificar**. Tratar como ambíguo, fora do cálculo monetário direto.

---

### (15) Quais casos devem ser EXCLUÍDOS do cálculo?

**INFERÊNCIA TÉCNICA / operacional:**

- **Classe D — sem valor utilizável: 76.751 ARTs (33,2%).**
  Excluir do cálculo monetário; documentar volume e motivo (ausência de valor).
  Observação correlata (FATO VERIFICADO): ARTs sem valor utilizável = 74.026 (32%) na contagem direta de valor ausente; a Classe D (33,2%) incorpora também registros sem valor plausível.

- **Valores implausíveis (> R$ 1 bilhão): 29 ARTs.** Excluir como outliers/erros extremos (o máximo observado por ART chega a ~7,9×10¹¹).

**RECOMENDAÇÃO.** A exclusão de Classe D e dos implausíveis deve ser **documentada** (quantos e por quê), nunca silenciosa, para preservar a rastreabilidade do subsídio metodológico.

---

## Síntese das classes (dimensionamento — INFERÊNCIA operacional sobre 230.928 ARTs)

| Classe | Critério | ARTs | % | Uso na governança de honorários |
|---|---|---:|---:|---|
| A | Linha única, 1 código, 1 valor plausível | 53.190 | 23,0% | Base **primária** (cálculo monetário) |
| B homogênea | Multi-linha, mesmo código, valor constante | 38.631 | 16,7% | Base **secundária / simulação** (regra explícita) |
| Valor varia entre linhas | Multi-linha, valor diferente entre linhas | 2.080 | 0,9% | **Ambíguo** — fora do cálculo direto |
| C composta | Multi-linha, múltiplos códigos, valor único replicado | 60.247 | 26,1% | Só **frequência / detecção** de serviços novos |
| D sem valor | Sem valor utilizável | 76.751 | 33,2% | **Excluir**, documentar volume/motivo |
| Implausível | Valor > R$ 1 bilhão | 29 | — | **Excluir** (outlier/erro) |

---

## Regras operacionais decorrentes (RECOMENDAÇÃO)

1. **Unidade de análise = ART (`id`), nunca linha.** Deduplicar por `id` antes de qualquer agregação de valor (justificativa: 62,6% multi-linha; valor replicado em 99.982 ARTs).
2. **Nunca somar linhas para obter valor.** O `valor_contrato` é da ART inteira (perguntas 10–11; exemplo ART 2399866).
3. **Cálculo monetário por serviço só nas Classes A e B.** Classe C entra apenas para contagem/detecção; Classes D e implausíveis ficam fora, com registro do volume excluído.
4. **Supressão n < 5** para serviços raros — escrever "Informação insuficiente para verificar".
5. **Modalidade não indica interdisciplinaridade** (`titulos` traz uma única modalidade por ART, pergunta 8). A composição de escopo é vista por múltiplos `codigo`, não por `titulos`.
6. **Caráter orientativo.** Os parâmetros derivados são referência técnica / parâmetro orientativo, não preço obrigatório.

---

*Documento de subsídio metodológico. Todos os números provêm do bloco de fatos verificados desta sessão, calculados sobre "ARTs 2022 01022024.csv". Onde a base não sustenta conclusão, registrou-se "Informação insuficiente para verificar".*
