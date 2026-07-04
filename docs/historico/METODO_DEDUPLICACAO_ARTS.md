# Método de Deduplicação das ARTs

Subsídio metodológico para tratamento da base de Anotações de Responsabilidade Técnica (ARTs) como referência técnica orientativa para a tabela de honorários do SENGE-BA / CREA-BA.

Base analisada: arquivo `ARTs 2022 01022024.csv` (pasta ARTS Adinailson), referência 2022.

Este documento separa explicitamente, em cada ponto, **FATO VERIFICADO**, **INFERÊNCIA TÉCNICA** e **RECOMENDAÇÃO**. Onde algo não pôde ser verificado na base, registra-se literalmente: "Informação insuficiente para verificar".

---

## 0. Regra central

**FATO VERIFICADO.** O campo `valor_contrato` é o valor da ART **inteira**, replicado em cada linha de atividade — não é o valor por atividade. Entre as ARTs multi-linha, 99.982 têm valor constante em todas as linhas (mesmo valor repetido) e apenas 2.080 variam. Exemplo real verificado: ART id 2399866 tem 2 linhas (Laudo e Vistoria), ambas com valor 433.795,00 replicado.

**Consequência metodológica obrigatória:** deduplicar o **VALOR** por `id` de ART (um valor por ART). Somar as linhas de atividade multiplica o valor indevidamente.

**FATO VERIFICADO.** É indispensável distinguir três contadores distintos, que **não** são intercambiáveis:

| Contador | Definição | Volume (base 2022) |
|---|---|---|
| Nº de ARTs | `id` distintos | **230.928** |
| Nº de linhas de atividade | registros (linhas) no CSV | **726.028** |
| Nº de serviços | atividades distintas / escopo técnico | (derivado — ver ponto 8) |

---

## 1. Duplicidade de ART

**FATO VERIFICADO.** Existe identificador único de ART: o campo `id`. A base tem 726.028 linhas de atividade, mas apenas 230.928 ARTs distintas (`id`). Portanto a contagem de linhas **não** equivale à contagem de ARTs.

**FATO VERIFICADO.** 62,6% das ARTs são multi-linha (144.541 de 230.928); 37,4% são linha única (86.387).

**INFERÊNCIA TÉCNICA.** A "duplicidade" de ART nesta base não é erro de cadastro, e sim a expansão natural de uma ART em múltiplas linhas de atividade. Tratar cada linha como uma ART distinta inflaria a contagem de ARTs em até ~3,1x (726.028 / 230.928).

**RECOMENDAÇÃO.** Para qualquer contagem de "quantas ARTs", agregar primeiro por `id` (deduplicação por chave). Nunca contar linhas como ARTs.

---

## 2. Duplicidade de linha de atividade

**FATO VERIFICADO.** Uma mesma ART pode aparecer em várias linhas: 62,6% das ARTs são multi-linha. Dentro de uma ART, a mesma atividade (mesmo `codigo`) pode repetir-se em mais de uma linha.

**INFERÊNCIA TÉCNICA.** Há dois casos de multiplicidade de linha que precisam ser separados:
- repetição da **mesma** atividade (mesmo `codigo`) em várias linhas — redundância de escopo homogêneo;
- linhas com **codigos diferentes** — escopo composto (ver ponto 6).

**RECOMENDAÇÃO.** Para contagem de serviços, deduplicar pares (`id`, `codigo`) antes de contar atividades distintas. Para análise de frequência de serviços no mercado, contar `codigo` distinto por ART (presença), não o número bruto de linhas, evitando que ARTs muito fragmentadas pesem mais que ARTs simples.

---

## 3. Repetição de valor por múltiplas linhas da mesma ART

**FATO VERIFICADO.** Entre as ARTs multi-linha, 99.982 têm `valor_contrato` constante em todas as linhas; apenas 2.080 variam. O valor é da ART inteira, replicado por linha.

**FATO VERIFICADO.** A mediana por LINHA (~R$ 1.570) difere da mediana por ART (R$ 1.800) justamente por causa da replicação — evidência direta do efeito de mistura ao não deduplicar.

**RECOMENDAÇÃO.** Calcular qualquer estatística monetária (mediana, P25, P75, P90, máximo) sempre no nível ART, deduplicado por `id`, usando um único valor por ART. Distribuição de referência no nível ART (deduplicado, valores positivos): mediana R$ 1.800; P25 800; P75 7.272; P90 200.000.

---

## 4. Mesmo serviço em múltiplas modalidades

**FATO VERIFICADO.** Nesta base, o campo `titulos` (modalidade/título profissional do responsável) traz **exatamente um** título por ART; a multi-modalidade no campo `titulos` é 0%. A mistura entre modalidades **não** aparece no campo `titulos`.

**INFERÊNCIA TÉCNICA.** Quando ocorre, a interface entre modalidades aparece de outra forma: (a) via múltiplos `codigos` de atividade dentro da mesma ART (escopo composto) e (b) no nível do catálogo — o mesmo serviço existindo em catálogos de modalidades diferentes. Exemplos de modalidades observadas (mediana de valor por ART): Eng. Civil 324.741 reg. (mediana 2.800); Eletricista 118.365 (1.500); Agrônomo 92.344 (186,55); Segurança do Trabalho 49.443 (500); Ambiental 35.828 (2.470); Mecânico 24.762 (1.200); Controle/Automação 5.729 (5.000).

**RECOMENDAÇÃO.** Ao mapear um serviço para a matriz de complexidade da tabela, não pressupor uma modalidade única a partir do `titulos`. Para serviços que naturalmente cruzam modalidades, registrar a modalidade declarada (`titulos`) como atributo da ART e o(s) `codigo`(s) de atividade como atributo de escopo, mantendo-os em colunas separadas. **Informação insuficiente para verificar** se um mesmo serviço foi anotado simultaneamente sob mais de uma modalidade no mesmo contrato — o campo `titulos` não suporta essa leitura nesta base.

---

## 5. Mesmo profissional com mais de uma formação

**Informação insuficiente para verificar.** A base não traz identificador único de profissional nem o conjunto de formações por pessoa; o campo `titulos` carrega um único título por ART. Não é possível, a partir desta base, afirmar que um mesmo profissional possui mais de uma formação nem cruzar formações por indivíduo.

**RECOMENDAÇÃO (governança e LGPD).** Não construir qualquer agregação ou ranking no nível de profissional. Caso o cruzamento de formações por profissional venha a ser necessário no futuro, exigirá fonte adicional (cadastro do CREA-BA) com tratamento dedicado de dados pessoais, fora do escopo desta base.

---

## 6. Mesma ART com mais de uma atividade

**FATO VERIFICADO.** Uma ART pode ter várias atividades: 26,5% das ARTs (61.284) têm mais de um `codigo` de atividade distinto (escopo composto).

**INFERÊNCIA TÉCNICA.** Nesses casos, com valor único replicado, **não** é possível atribuir o valor a um serviço específico — o valor cobre o conjunto do escopo. Esse é o núcleo da ambiguidade de atribuição monetária (Classe C, ponto 9).

**RECOMENDAÇÃO.** ARTs de escopo composto servem para **frequência e detecção de serviços** (quais atividades aparecem juntas, quais serviços novos surgem), nunca para cálculo de valor por serviço isolado.

---

## 7. Mesmo valor replicado em linhas diferentes

**FATO VERIFICADO.** É o mesmo fenômeno do ponto 3, observado no nível da linha: 99.982 ARTs replicam exatamente o mesmo valor em linhas diferentes; 2.080 apresentam valores diferentes entre linhas.

**INFERÊNCIA TÉCNICA.** O valor replicado é um marcador confiável de que o registro representa um único contrato. As 2.080 ARTs com valor variável entre linhas (0,9% do total) constituem caso atípico que merece tratamento próprio (não somar; ver ponto 9), pois a variação pode indicar parcelamento por atividade ou inconsistência de exportação.

**RECOMENDAÇÃO.** Regra de deduplicação de valor: para cada `id`, se o valor for constante entre linhas, adotar esse valor único; se variar (caso minoritário), não somar — sinalizar como caso especial e, por padrão de prudência, registrá-lo como ambíguo e excluí-lo do cálculo monetário enquanto não houver regra explícita documentada.

---

## 8. Separação entre contagem de ART, de atividades e de serviços

**FATO VERIFICADO (contadores base):**
- Nº de ARTs (`id` distintos): **230.928**
- Nº de linhas de atividade: **726.028**
- Nº de serviços: derivado de `codigo`/`atividade` distintos — **não** equivale a nenhum dos dois acima.

**INFERÊNCIA TÉCNICA.** Os três níveis respondem a perguntas diferentes:
- **ART** → quantos contratos/responsabilidades foram anotados (unidade jurídica/contratual);
- **linha de atividade** → granularidade bruta de exportação (não é unidade de análise);
- **serviço** → quantos tipos técnicos distintos existem (unidade de catálogo, para mapear na matriz da tabela de honorários).

**RECOMENDAÇÃO.** Definir e fixar, em qualquer relatório ou dashboard, qual dos três contadores está sendo exibido, rotulando-o explicitamente. Para valor monetário: sempre nível ART. Para frequência de tipos de serviço: contar `codigo` distinto (presença por ART). Para volume operacional bruto: linhas. Nunca misturar denominadores entre indicadores.

---

## 9. Critérios para manter / agrupar / excluir

**INFERÊNCIA TÉCNICA (tipologia de confiabilidade, computada sobre os 230.928 ids):**

| Classe | Definição | Volume | % | Uso |
|---|---|---|---|---|
| **A** | linha única, 1 código, 1 valor plausível | 53.190 | 23,0% | **Manter** — base PRIMÁRIA de cálculo |
| **B homogênea** | multi-linha, MESMO código, valor constante (mesma atividade repetida) | 38.631 | 16,7% | **Agrupar** por `id` — base secundária/simulação com regra explícita |
| Valor variável entre linhas | multi-linha, valor diferente entre linhas | 2.080 | 0,9% | Caso especial — não somar; tratar à parte |
| **C composta ambígua** | multi-linha, MÚLTIPLOS códigos, valor único replicado | 60.247 | 26,1% | Apenas **frequência/detecção** de serviços — NUNCA cálculo monetário |
| **D sem valor** | sem valor utilizável | 76.751 | 33,2% | **Excluir** do cálculo; documentar volume/motivo |
| Implausível (>R$ 1 bilhão) | outlier/erro extremo | 29 | — | Excluir; documentar |

**Critérios operacionais (RECOMENDAÇÃO):**
- **Manter** para cálculo de valor: Classe A (primária). Para serviços frequentes, é suficiente.
- **Agrupar** por `id` (1 valor por ART): Classe B homogênea, como base secundária com regra documentada.
- **Excluir** do cálculo monetário: Classe D (sem valor) e implausíveis (>R$ 1 bilhão); documentar quantos e por quê.
- **Usar só para frequência/detecção**, nunca para valor: Classe C composta ambígua.
- **Supressão por baixa contagem (n<5):** para serviços raros, marcar literalmente "Informação insuficiente para verificar" em vez de publicar valor.
- ARTs sem valor utilizável totalizam 74.026 (32%); ARTs sem valor na tipologia (Classe D) 76.751 (33,2%) — registrar o volume excluído junto a qualquer estatística.

---

## 10. Impacto no dashboard

**RECOMENDAÇÃO (especificação para o painel):**

1. **Três contadores separados e rotulados.** Cards distintos para Nº de ARTs (230.928), Nº de linhas de atividade (726.028) e Nº de serviços (derivado). Nunca exibir um número sem dizer qual nível ele representa.
2. **Valor sempre no nível ART deduplicado.** Toda métrica monetária deve consumir a tabela já deduplicada por `id` (um valor por ART). Bloquear, na camada de dados, qualquer soma de `valor_contrato` por linha.
3. **Filtro por classe de confiabilidade.** Permitir restringir o painel a Classe A (e opcionalmente A+B), com Classe C disponível apenas em visões de frequência (contagem de serviços), nunca de valor, e Classe D/implausíveis fora do cálculo, mas exibidos como "volume excluído".
4. **Estatísticas de referência por mediana e percentis**, não média (sensível a outliers): mediana R$ 1.800; P25 800; P75 7.272; P90 200.000 (nível ART). Para Classe A: mediana R$ 2.000; P25 800; P75 8.000; P90 145.363.
5. **Supressão n<5.** Para qualquer recorte (serviço, modalidade, unidade) com menos de 5 ARTs, exibir "Informação insuficiente para verificar" em lugar do valor.
6. **Rótulo permanente de natureza orientativa.** Os valores são referência técnica / parâmetro orientativo, jamais preço obrigatório. Nada de ranking de profissionais, empresas ou contratantes — apenas agregados (LGPD e cuidado concorrencial).
7. **Nota de cobertura.** Exibir, junto às métricas, o percentual da base efetivamente usado no cálculo (Classe A, ou A+B) e o percentual excluído (Classe D + implausíveis), para transparência metodológica.

---

*Caráter ORIENTATIVO. Documento de subsídio metodológico — referência técnica e parâmetro orientativo para a governança de honorários, sem caráter impositivo.*
