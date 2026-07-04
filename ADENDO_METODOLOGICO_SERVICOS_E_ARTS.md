# ADENDO METODOLÓGICO — SERVIÇOS E ARTs
## Por que a tabela deve seguir organizada por serviço e como usar as ARTs com rigor

> Adendo institucional à proposta de nova metodologia da tabela de honorários do SENGE/BA. Linguagem
> técnica e orientativa, para CREA-BA, SENGE-BA e câmaras especializadas. Separa **fato verificado**,
> **inferência técnica** e **recomendação**. Data: 2026-06-23.

---

## 1. Por que a tabela deve continuar organizada por serviço
**Recomendação.** A organização **por serviço** (catálogo de famílias → serviços → natureza/subtipo) é a
que melhor dialoga com a prática profissional, com o catálogo de atividades do CREA e com a tabela vigente
(13 famílias, de 29/07/2024). Mantê-la preserva o investimento já feito e a legibilidade para o
profissional. **O que muda não é a lógica por serviço, e sim a forma de mantê-la atualizada e de
fundamentar as faixas de referência.**

## 2. Por que a base de ARTs ajuda a identificar novos serviços
**Fato verificado.** As ARTs registram o vocabulário real de atividades exercidas. Nos dados de 2022
aparecem, em alto volume, serviços **ausentes na tabela atual** — com destaque para **energia solar
fotovoltaica / microgeração distribuída** (unidade **kWp**) e **receituário agronômico**.
**Recomendação.** Usar as ARTs como **radar de novos serviços**: o que surge com frequência relevante nas
ARTs e não consta da tabela deve ser candidato a **novo item do catálogo**.

## 3. Por que nem toda ART serve para cálculo de valor
**Fato verificado.** O campo `valor_contrato` é o valor **da ART inteira**, não da atividade: entre as ARTs
com mais de uma linha, **99.982 repetem o mesmo valor em todas as linhas**. Somar linhas multiplica o valor
indevidamente. Além disso, **32% das ARTs não têm valor utilizável**. **Inferência.** Tratar todo valor de
ART como honorário de um serviço específico **contamina** a referência. **Recomendação.** Só registros em
que o valor possa ser associado a um serviço com baixo risco de mistura entram no cálculo monetário.

## 4. Por que casos compostos precisam de tratamento
**Fato verificado.** **26,5% das ARTs** contêm **mais de um código de atividade** (escopo composto), e
**62,6%** têm mais de uma linha. Nesses casos, o valor único cobre vários serviços ao mesmo tempo.
**Recomendação.** Casos compostos heterogêneos **não** devem alimentar diretamente o valor por serviço;
servem para **frequência, demanda e identificação de novos serviços**.

## 5. Por que separar a base de alta confiabilidade (Classe A)
**Fato/Inferência.** É possível isolar uma base limpa — **Classe A: ARTs de atividade única, com um valor
plausível** — que soma **53.190 ARTs (23,0%)**, com mediana de R$ 2.000. **Recomendação.** Essa base deve
ser a **fonte primária** das faixas de referência por serviço, porque nela o risco de mistura é baixo.

## 6. Por que valores ponderados, se usados, devem ser secundários
**Inferência.** Para os casos compostos (Classe C), o valor é **único e replicado**, sem qualquer
informação que permita repartir quanto coube a cada serviço. Qualquer ponderação (igualitária, por
complexidade, por unidade etc.) seria uma **suposição**. **Recomendação.** Ponderação apenas como
**análise exploratória secundária**, claramente separada da base principal, e nunca como fundamento único
de um valor de referência (detalhe em `METODO_PONDERACAO_SERVICOS_COMPOSTOS.md`).

## 7. Por que classes de confiabilidade tornam a proposta mais robusta
**Recomendação.** Classificar cada registro em **A (alta confiabilidade) / B (composto homogêneo,
ponderável) / C (composto ambíguo) / D (inválido)** torna explícito **o que entra e o que não entra** no
cálculo. Isso transforma uma fragilidade (a mistura) em um **critério auditável e defensável**, em vez de
um problema oculto.

## 8. Como isso melhora a atualização dinâmica da tabela
**Recomendação.** Com a base classificada, a atualização deixa de depender só do CUB: a cada ciclo,
reprocessam-se as ARTs mais recentes, recalculam-se as faixas (mediana/IQR) **por serviço** sobre a Classe
A e revisita-se o catálogo para **incorporar novos serviços**. A tabela passa a ter um **mecanismo vivo**,
documentado e reprodutível.

## 9. Como isso reduz risco metodológico
**Inferência.** A separação por classes evita os três erros mais graves: (a) **dupla contagem** do valor
replicado; (b) **atribuição indevida** de um valor composto a um único serviço; (c) **uso de registros
inválidos**. Reduz também o risco **interpretativo** (a tabela permanece **orientativa**) e o risco
**LGPD** (apenas agregados, supressão de células com n<5, sem ranking individual).

## 10. Como apresentar ao CREA-BA / SENGE-BA
**Recomendação.** Apresentar em três mensagens: (i) **a tabela segue por serviço** — nada se perde;
(ii) **as ARTs entram como evidência auxiliar, indireta e agregada**, não como prova de honorário; (iii)
**só a base de alta confiabilidade calcula valor**, o resto serve de radar de demanda e de novos serviços.
Reforçar o caráter de **referência técnica e parâmetro orientativo de valorização profissional**, com
cuidados jurídicos e concorrenciais.

---

## Síntese institucional
> A nova metodologia **preserva a organização por serviço** e adiciona um **processo técnico de
> classificação de confiabilidade dos dados de ART**. Apenas a base de alta confiabilidade (Classe A,
> 53.190 ARTs) fundamenta valores; casos compostos e inválidos servem para frequência, demanda e
> identificação de novos serviços. O resultado é uma tabela **mais robusta, atualizável e juridicamente
> segura**, de caráter **orientativo**.

*Documento derivado. Não altera arquivos originais. Nenhum valor, norma ou conclusão foi inventado.*
