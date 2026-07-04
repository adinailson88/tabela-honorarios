# Método de Ponderação para Serviços Compostos em ARTs Multi-Atividade

Subsídio metodológico — SENGE-BA / CREA-BA
Documento de caráter ORIENTATIVO. Os parâmetros aqui discutidos são referência técnica e estimativa de esforço, nunca preço obrigatório ou tabela vinculante.

---

## 1. Pergunta de trabalho

É possível estimar um valor PONDERADO por serviço quando uma ART registra MÚLTIPLAS atividades? Em outras palavras: dado que uma ART traz, por exemplo, "Projeto + Execução + Laudo", podemos atribuir a cada serviço uma fração defensável do `valor_contrato` da ART?

Este documento avalia sete alternativas de ponderação, indica quando usar cada uma, suas vantagens, riscos, necessidade de validação e se são defensáveis institucionalmente. Ao final, apresenta a conclusão obrigatória sobre fragilidade da ponderação e recomendação de base principal.

---

## 2. Restrição estrutural dos dados (FATO VERIFICADO)

Antes de discutir métodos, é preciso fixar o que os dados PERMITEM e o que NÃO permitem. Os números abaixo foram calculados diretamente da base "ARTs 2022 01022024.csv" (base 2022) nesta sessão.

- FATO VERIFICADO — O `valor_contrato` é o valor da ART INTEIRA, replicado em cada linha de atividade; NÃO é o valor por atividade. Entre as ARTs multi-linha, 99.982 têm valor constante em todas as linhas e apenas 2.080 variam. Somar linhas multiplica o valor indevidamente.
- FATO VERIFICADO — Exemplo real: ART id 2399866 tem 2 linhas (Laudo e Vistoria), ambas com valor 433.795,00 replicado.
- FATO VERIFICADO — 26,5% das ARTs (61.284) têm mais de um código de atividade distinto (escopo composto).
- FATO VERIFICADO — 62,6% das ARTs são multi-linha (144.541 de 230.928); 37,4% são linha única (86.387).
- FATO VERIFICADO — Cada ART carrega EXATAMENTE UM título/modalidade no campo `titulos` (multi-modalidade = 0% nesta base). A mistura entre modalidades não aparece no campo `titulos`; quando aparece, é via múltiplos códigos de atividade.

INFERÊNCIA TÉCNICA — A consequência central é que, para ARTs com múltiplos códigos e valor único replicado, NÃO existe nos dados nenhuma informação que decomponha o valor entre as atividades. Qualquer fração atribuída a um serviço individual é uma SUPOSIÇÃO imposta externamente, não uma medição. Os 2.080 casos com valor variando entre linhas (0,9%) são exceção e, ainda assim, a variação não é necessariamente o "valor por serviço".

### 2.1. A camada de confiabilidade já dimensionada (INFERÊNCIA operacional sobre 230.928 ids)

- Classe A (linha única, 1 código, 1 valor plausível): 53.190 ARTs = 23,0%. Valor: mediana R$ 2.000; P25 800; P75 8.000; P90 145.363.
- Classe B homogênea (multi-linha, MESMO código, valor constante = mesma atividade repetida): 38.631 = 16,7%.
- Caso de valor que varia entre linhas: 2.080 = 0,9%.
- Classe C composta ambígua (multi-linha, MÚLTIPLOS códigos, valor único replicado): 60.247 = 26,1%.
- Classe D sem valor: 76.751 = 33,2%; implausível (>R$ 1 bilhão): 29.

INFERÊNCIA TÉCNICA — A ponderação só faz sentido discutir sobre a Classe C (60.247 ARTs, 26,1%), porque é nela que há múltiplos códigos disputando um único valor. A Classe A não precisa de ponderação (1 serviço = 1 valor). A Classe B é o mesmo serviço repetido (não há o que repartir). A Classe D não tem valor a repartir.

---

## 3. As sete alternativas de ponderação

Para todas as alternativas abaixo, o objeto é a Classe C: como repartir um único `valor_contrato` entre os N códigos de atividade distintos da ART.

### Alternativa 1 — Ponderação igualitária (valor / N atividades)

- Descrição: divide o valor da ART em partes iguais entre os N códigos distintos.
- Quando usar: apenas como referência exploratória de teto/piso grosseiro, ou como linha de base ("baseline") contra a qual comparar métodos mais elaborados.
- Vantagens: simples, transparente, reprodutível, sem parâmetros arbitrários adicionais; fácil de explicar ao colegiado.
- Riscos: assume que todos os serviços de uma ART valem o mesmo, o que contraria a realidade técnica (um projeto estrutural e uma vistoria não têm o mesmo esforço). Distorce sistematicamente para baixo os serviços complexos e para cima os triviais.
- Necessidade de validação: ALTA. Exige confronto com casos Classe A do mesmo serviço para medir o viés.
- Defensável institucionalmente? Apenas como baseline declarado. NÃO defensável como valor de referência publicado, porque embute hipótese falsa de equivalência.

### Alternativa 2 — Ponderação por complexidade (matriz de complexidade)

- Descrição: atribui pesos a cada atividade conforme uma matriz de complexidade técnica (esforço relativo) e reparte o valor proporcionalmente aos pesos.
- Quando usar: quando existir uma matriz de complexidade construída e validada por especialistas para o conjunto de serviços envolvidos.
- Vantagens: conceitualmente alinhada à lógica de "estimativa de esforço" e "valorização profissional"; melhor que a igualitária por reconhecer diferenças técnicas.
- Riscos: os pesos de complexidade NÃO existem nos dados; precisam ser definidos externamente. Informação insuficiente para verificar quais pesos seriam corretos. Risco de circularidade (calibrar pesos para reproduzir um resultado desejado) e de aparência de objetividade sobre uma escolha subjetiva.
- Necessidade de validação: MUITO ALTA. Depende de painel técnico e de teste contra Classe A.
- Defensável institucionalmente? Condicionalmente, SE a matriz de complexidade for documentada, aprovada em instância colegiada e apresentada como parâmetro orientativo. Sem isso, não defensável.

### Alternativa 3 — Ponderação por família de serviço

- Descrição: usa as famílias de serviço (as 13 abas temáticas da tabela atual: Consultoria, Direção/Administração, Fiscalização, Projetos Civis, Cálculo Estrutural, Saneamento, Instalações, Geologia/Minas etc.) como base de peso, repartindo o valor conforme a participação típica de cada família.
- Quando usar: para análise agregada por família, não para o serviço individual; útil para entender a composição macro do mercado.
- Vantagens: conecta-se diretamente à estrutura da tabela existente (FATO VERIFICADO: 13 abas temáticas organizadas por família); facilita leitura institucional.
- Riscos: muitas ARTs compostas misturam atividades DENTRO da mesma família (ex.: vários itens de instalações), caso em que a ponderação por família não resolve nada. Além disso, a "participação típica por família" não está medida nos dados. Informação insuficiente para verificar.
- Necessidade de validação: ALTA.
- Defensável institucionalmente? Como camada de leitura agregada, sim. Como mecanismo de atribuição de valor a um serviço específico, não.

### Alternativa 4 — Ponderação por frequência histórica

- Descrição: repartir o valor conforme a frequência relativa de cada atividade na base (atividades mais comuns recebem maior peso, ou o inverso).
- Quando usar: nunca como repartição de valor; apenas para detecção de serviços novos e dimensionamento de volume.
- Vantagens: a frequência É um FATO VERIFICADO e robusto (existe vocabulário real de atividades com contagens, ex.: RECEITUÁRIO AGRO 60.378; EDF. ALVENARIA 10.913; itens de microgeração/fotovoltaica 4.500–7.700 cada).
- Riscos: frequência não tem relação causal com valor. Um serviço raro pode ser caro e um frequente pode ser barato. Usar frequência como peso de valor é um erro de inferência.
- Necessidade de validação: o uso para valor seria inválido por construção; não há validação que o salve.
- Defensável institucionalmente? Para frequência/detecção de novos serviços, SIM (e é recomendável). Para repartição de valor, NÃO.

### Alternativa 5 — Ponderação por peso de especialistas (Delphi/colegiado)

- Descrição: pesos definidos por consulta estruturada a especialistas (painel técnico, método tipo Delphi) sobre a participação de cada serviço no valor da ART.
- Quando usar: quando houver mandato institucional e tempo para conduzir consulta formal documentada.
- Vantagens: incorpora conhecimento técnico que os dados não contêm; é o caminho mais honesto quando o dado é insuficiente, pois assume explicitamente a natureza de juízo profissional.
- Riscos: subjetividade, custo, possível viés de quem participa; resultado não é reprodutível só a partir dos dados. Informação insuficiente para verificar os pesos antes da consulta.
- Necessidade de validação: o próprio processo Delphi é a validação; exige protocolo, registro de consenso e revisão periódica.
- Defensável institucionalmente? SIM, desde que tratado como parâmetro orientativo derivado de juízo colegiado, com governança de honorários documentada — e nunca apresentado como medição empírica dos dados.

### Alternativa 6 — Ponderação por unidade de medida

- Descrição: usar a unidade de cada atividade (m², m³, km, ha, kWp, kVA, kW, unidade, hora) e a respectiva mediana de valor por unidade para estimar a fração de cada serviço.
- Quando usar: somente quando a ART registrar a QUANTIDADE por atividade de forma consistente e a unidade for compatível com um parâmetro de valor por unidade.
- Vantagens: aproxima-se da lógica da tabela (FATO VERIFICADO: critério de valor heterogêneo — por m², m³, km, ha, hora, %CUB, R$ fixo) e usa medianas por unidade verificadas (ex.: metro quadrado mediana 2.000; quilowatt 1.500; kWp 1.000; hectare 2.000; kVA 5.000).
- Riscos: na Classe C o `valor_contrato` é único e replicado, sem decomposição de quantidade por atividade confiável; o campo `quantidade`/`unidade` existe por linha, mas combiná-lo com um valor único replicado não reconstrói o valor de cada serviço. Misturar unidades diferentes na mesma ART impede uma soma comparável. Informação insuficiente para verificar a consistência de quantidade por atividade na Classe C.
- Necessidade de validação: ALTA, item a item.
- Defensável institucionalmente? Como método para construir referências por unidade a partir da Classe A (onde há 1 serviço, 1 unidade, 1 valor), SIM. Como repartição interna da Classe C, NÃO.

### Alternativa 7 — Não ponderar; usar somente casos únicos (Classe A)

- Descrição: descartar a repartição de ARTs compostas para fins de valor e construir as referências exclusivamente sobre a Classe A (linha única, 1 código, 1 valor plausível), com supressão de células com n<5.
- Quando usar: como REGRA GERAL para qualquer referência de valor publicada.
- Vantagens: cada valor é atribuível, sem suposição de repartição; máxima defensabilidade; reprodutível; alinhado à separação fato/inferência. FATO VERIFICADO: Classe A tem 53.190 ARTs (23,0%), com mediana R$ 2.000, P25 800, P75 8.000, P90 145.363 — base suficiente para serviços frequentes.
- Riscos: cobertura menor — serviços raros podem não ter n suficiente na Classe A, exigindo marcar "Informação insuficiente para verificar". Não aproveita o volume das ARTs compostas para valor (mas as aproveita para frequência/detecção).
- Necessidade de validação: BAIXA quanto ao método de atribuição (é direto); aplicar apenas o controle de supressão n<5 e tratamento de outliers.
- Defensável institucionalmente? SIM. É a opção mais defensável.

---

## 4. Quadro-resumo

| # | Método | Uso recomendado | Para VALOR publicado? | Defensável |
|---|--------|-----------------|------------------------|------------|
| 1 | Igualitária | Baseline exploratório | Não | Só como baseline declarado |
| 2 | Complexidade | Exploratório c/ matriz validada | Não (sem matriz aprovada) | Condicional |
| 3 | Família de serviço | Leitura agregada | Não (serviço individual) | Parcial (agregado) |
| 4 | Frequência histórica | Detecção/volume de serviços | Não | Sim p/ frequência; não p/ valor |
| 5 | Peso de especialistas | Juízo colegiado documentado | Como orientativo | Sim, com governança |
| 6 | Unidade de medida | Referência por unidade via Classe A | Não (dentro da Classe C) | Sim p/ Classe A; não p/ C |
| 7 | Só Classe A (não ponderar) | Regra geral de referência | SIM | Sim (mais defensável) |

---

## 5. Conclusão e recomendação obrigatória

FATO VERIFICADO — A Classe C representa 26,1% das ARTs (60.247) e combina VALOR ÚNICO replicado com MÚLTIPLOS códigos de atividade. Não há, nos dados, qualquer informação que decomponha esse valor entre os serviços.

INFERÊNCIA TÉCNICA — Por isso, TODA ponderação aplicada à Classe C é estruturalmente FRÁGIL: ela impõe uma hipótese externa (pesos iguais, de complexidade, de família, de frequência, de especialistas ou de unidade) sobre um dado que não permite verificá-la. Os métodos 1 a 6 variam apenas na PLAUSIBILIDADE da hipótese, não na sua verificabilidade — nenhum deles reconstrói o valor real de cada serviço a partir dos dados.

RECOMENDAÇÃO —
1. Usar a base Classe A (53.190 ARTs) como base PRINCIPAL e única fonte de valores de referência publicados, com supressão n<5 e tratamento de outliers.
2. Tratar qualquer ponderação (métodos 1, 2, 5 ou 6) apenas como análise EXPLORATÓRIA/secundária, em seção claramente separada e rotulada como "estimativa exploratória — não verificável nos dados", jamais misturada às referências principais.
3. Usar a Classe B como base secundária/simulação com regra explícita; a Classe C apenas para FREQUÊNCIA e detecção de serviços novos (nunca para cálculo monetário); a Classe D excluída do cálculo, com volume e motivo documentados.
4. Reservar a ponderação por peso de especialistas (método 5) como o ÚNICO caminho institucionalmente aceitável para atribuir valor a serviços compostos, e ainda assim apenas como parâmetro orientativo de governança de honorários, documentado em instância colegiada — nunca como medição empírica.

Princípio-síntese: a defensabilidade vem de NÃO atribuir valor que os dados não sustentam. Onde a repartição não for verificável, escrever exatamente: "Informação insuficiente para verificar".

---

## 6. Pontos marcados como "Informação insuficiente para verificar"

- Pesos de complexidade por atividade (método 2): não existem nos dados.
- Participação típica de valor por família de serviço (método 3): não medida nos dados.
- Consistência de quantidade por atividade na Classe C para uso da unidade de medida (método 6): não verificável com valor único replicado.
- Pesos de especialistas antes da consulta formal (método 5): só existem após processo Delphi documentado.
- Valor individual de cada serviço dentro de qualquer ART da Classe C: não decomponível a partir dos dados.

---

Documento de caráter orientativo. Não constitui preço obrigatório, preço mínimo compulsório nem tabela vinculante. Base de dados: "ARTs 2022 01022024.csv" (base 2022). Os agregados não identificam profissionais, empresas ou contratantes.
