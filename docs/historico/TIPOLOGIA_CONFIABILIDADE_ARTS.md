# Tipologia de Confiabilidade das ARTs

**Subsídio metodológico para a tabela de honorários — SENGE-BA / CREA-BA**
Base: pasta "ARTS Adinailson", arquivo "ARTs 2022 01022024.csv" (base 2022).

---

## 0. Natureza deste documento e como ler os rótulos

Este documento separa três planos, conforme exigido pela governança institucional:

- **FATO VERIFICADO** — número calculado diretamente do arquivo de ARTs nesta sessão. Não é recalculado nem rearredondado aqui.
- **INFERÊNCIA TÉCNICA** — interpretação/classificação construída a partir dos fatos (a própria tipologia A/B/C/D é inferência operacional).
- **RECOMENDAÇÃO** — proposta de uso, de caráter **orientativo**, nunca impositivo.

> **Status global da tipologia:** a divisão em quatro classes (A, B, C, D) é **INFERÊNCIA operacional** aplicada sobre **FATOS verificados**. Os tamanhos e percentuais de cada classe são FATO VERIFICADO; o enquadramento conceitual e os usos permitidos são INFERÊNCIA/RECOMENDAÇÃO.

### Por que esta tipologia é necessária (FATO VERIFICADO que a motiva)

- A base tem **726.028 linhas de atividade** correspondentes a **230.928 ARTs distintas** (campo `id`).
- **62,6%** das ARTs são multi-linha (144.541 de 230.928); **37,4%** são linha única (86.387).
- **26,5%** das ARTs (61.284) têm mais de um código de atividade distinto (escopo composto).
- Entre as ARTs multi-linha, **99.982** têm o **mesmo valor repetido em todas as linhas** e apenas **2.080** variam.

> **INFERÊNCIA TÉCNICA (decisiva):** `valor_contrato` é o valor da **ART inteira**, replicado em cada linha de atividade — **não** é o valor por atividade. Somar linhas multiplica o valor indevidamente. Exemplo real verificado: ART `id` 2399866 tem 2 linhas (Laudo e Vistoria), ambas com valor 433.795,00 replicado.

Como o valor não é atribuível por atividade em parte expressiva da base, é indispensável separar os registros que **permitem** estimativa monetária confiável daqueles que servem apenas para **frequência/demanda** ou que devem ser **excluídos** do cálculo. Essa é a função da tipologia.

---

## 1. As quatro classes

Universo de classificação: os **230.928** `id` distintos (nível ART, deduplicado).

### Classe A — ART de leitura direta (linha única, 1 código, 1 valor plausível)

- **Definição:** ART com uma única linha de atividade, um único código de atividade e um único valor de contrato plausível. O valor pode ser atribuído sem ambiguidade ao serviço descrito.
- **Critérios de enquadramento:** linha única **E** um código de atividade **E** valor positivo dentro de faixa plausível (descarte de implausíveis).
- **Tamanho (FATO VERIFICADO):** **53.190 ARTs = 23,0%.**
- **Distribuição de valor da Classe A (FATO VERIFICADO):** mediana **R$ 2.000**; P25 **800**; P75 **8.000**; P90 **145.363**.
- **USO PERMITIDO (RECOMENDAÇÃO):** **base PRIMÁRIA** para o cálculo de **referência técnica** de honorários, **com ressalvas**:
  - usar apenas para serviços **frequentes**; para serviços raros, aplicar supressão por baixa contagem (**n < 5**) e marcar **"Informação insuficiente para verificar"**;
  - reportar sempre como faixa (P25–P75) e mediana, nunca um único número impositivo;
  - tratar valores extremos como outliers a serem inspecionados, não somados.

### Classe B — multi-linha homogênea (mesmo código, valor constante)

- **Definição:** ART com várias linhas, porém **todas com o mesmo código de atividade** e **valor constante** entre as linhas — ou seja, a mesma atividade repetida. O valor da ART é interpretável, mas há repetição da atividade.
- **Critérios de enquadramento:** multi-linha **E** um único código de atividade distinto **E** valor constante em todas as linhas.
- **Tamanho (FATO VERIFICADO):** **38.631 ARTs = 16,7%.**
- **USO PERMITIDO (RECOMENDAÇÃO):** **base SECUNDÁRIA** para **cálculo de apoio/simulação**, com **ponderação explícita**:
  - o valor é da ART inteira (replicado), portanto **não** dividir nem multiplicar pelo número de linhas sem regra documentada;
  - empregar para corroborar/estabilizar a estimativa da Classe A, sempre declarando que se trata de simulação com regra explícita;
  - registrar a regra de ponderação adotada junto ao resultado.

### Caso à parte — valor que varia entre linhas (multi-linha, valor diferente)

- **Definição:** ART multi-linha em que o valor **difere** entre linhas (não é a replicação típica).
- **Tamanho (FATO VERIFICADO):** **2.080 ARTs = 0,9%.**
- **USO PERMITIDO (RECOMENDAÇÃO):** tratar como **exceção a inspecionar caso a caso**; não incorporar a cálculo agregado automático. Por ser volume residual (0,9%), não altera as referências; documentar e, quando necessário, analisar manualmente.

### Classe C — composta ambígua (multi-linha, múltiplos códigos, valor único replicado)

- **Definição:** ART com várias linhas e **múltiplos códigos de atividade distintos**, com **valor único replicado**. Como o valor é o da ART inteira e o escopo é composto, **não há como atribuir o valor a um serviço específico**.
- **Critérios de enquadramento:** multi-linha **E** múltiplos códigos de atividade **E** valor único replicado nas linhas.
- **Tamanho (FATO VERIFICADO):** **60.247 ARTs = 26,1%.**
- **USO PERMITIDO (RECOMENDAÇÃO):** **apenas frequência / demanda / detecção de novos serviços**. **NUNCA** usar para cálculo monetário por serviço:
  - serve para medir quais atividades aparecem e com que frequência (inclusive serviços modernos ausentes na tabela);
  - serve para mapear escopos compostos típicos;
  - qualquer valor monetário extraído daqui é, por construção, não atribuível — vedado seu uso para precificar um serviço isolado.

### Classe D — sem valor utilizável (excluir do cálculo monetário)

- **Definição:** ART sem valor de contrato utilizável (ausente ou não positivo), acrescida dos registros com valor implausível.
- **Critérios de enquadramento:** valor ausente/não utilizável **OU** valor implausível (> R$ 1 bilhão).
- **Tamanho (FATO VERIFICADO):** **76.751 ARTs = 33,2%** sem valor; **+ 29** ARTs implausíveis (> R$ 1 bilhão).
- **USO PERMITIDO (RECOMENDAÇÃO):** **excluir do cálculo monetário**; **documentar volume e motivo** da exclusão. Pode, no máximo, integrar contagens de frequência/demanda (com a ressalva de que não tem valor associado). A transparência sobre o volume excluído é parte da governança de honorários.

---

## 2. Tabela-resumo

| Classe | Definição resumida | Critério-chave | ARTs | % | Uso permitido |
|---|---|---|---|---|---|
| **A** | Linha única, 1 código, 1 valor plausível | 1 linha · 1 código · valor plausível | **53.190** | **23,0%** | Cálculo de **referência** (PRIMÁRIA), **com ressalvas** (n<5 → suprimir) |
| **B** | Multi-linha homogênea (mesmo código, valor constante) | multi-linha · 1 código · valor constante | **38.631** | **16,7%** | Cálculo **secundário/simulação** com **ponderação explícita** |
| *(caso)* | Valor varia entre linhas | multi-linha · valor diferente | **2.080** | **0,9%** | Exceção a inspecionar caso a caso (fora do agregado automático) |
| **C** | Composta ambígua (múltiplos códigos, valor replicado) | multi-linha · múltiplos códigos · valor único | **60.247** | **26,1%** | **Apenas** frequência/demanda/novos serviços — **nunca** cálculo monetário |
| **D** | Sem valor utilizável (+ implausíveis) | sem valor / não positivo · ou > R$ 1 bi | **76.751** (+ **29** implausíveis) | **33,2%** | **Excluir** do cálculo monetário; **documentar** volume e motivo |

> Observação metodológica (FATO VERIFICADO que reforça a tipologia): a mediana por **linha** (~R$ 1.570) difere da mediana por **ART** (R$ 1.800) justamente pela replicação de valor — evidência direta do efeito de mistura que a tipologia controla.

---

## 3. Síntese de governança (RECOMENDAÇÃO)

- **Núcleo de cálculo:** Classe A como base primária e Classe B como apoio com ponderação explícita.
- **Sinal de demanda e de modernização do catálogo:** Classe C (e, com ressalva, D) para detectar serviços frequentes ausentes na tabela (ex.: fotovoltaica/microgeração, agronomia, kWp/kVA), sem precificá-los a partir de valores não atribuíveis.
- **Transparência:** sempre declarar o volume excluído (Classe D) e a regra de supressão por baixa contagem (n < 5).
- **Caráter:** parâmetro **orientativo** de **valorização profissional**, jamais preço obrigatório ou tabela vinculante.
