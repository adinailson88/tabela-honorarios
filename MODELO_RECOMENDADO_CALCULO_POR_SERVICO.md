# MODELO RECOMENDADO DE CÁLCULO POR SERVIÇO

**Subsídio metodológico — Tabela de Honorários (SENGE-BA / CREA-BA)**
**Caráter:** referência técnica orientativa, nunca impositiva. Documento de governança de honorários.

> **Como ler este documento.** Cada item separa três níveis de afirmação:
> - **FATO VERIFICADO** — número apurado diretamente dos arquivos desta sessão (tabela de honorários e base de ARTs 2022). Não recalcular nem rearredondar.
> - **INFERÊNCIA TÉCNICA** — interpretação/classificação construída sobre os fatos.
> - **RECOMENDAÇÃO** — proposta de ação metodológica.
>
> Onde não houver base apurável, lê-se literalmente: **"Informação insuficiente para verificar"**.

---

## Princípio reitor: a base PRINCIPAL é a Classe A

**FATO VERIFICADO.** A tipologia de confiabilidade, computada sobre as 230.928 ARTs distintas (campo `id`) da base "ARTs 2022 01022024.csv":
- **Classe A** (linha única, 1 código de atividade, 1 valor plausível): **53.190 ARTs = 23,0%**. Distribuição de valor da Classe A: mediana **R$ 2.000**; P25 **800**; P75 **8.000**; P90 **145.363**.
- Classe B homogênea (multi-linha, mesmo código, valor constante = mesma atividade repetida): 38.631 = 16,7%.
- Caso de valor que varia entre linhas: 2.080 = 0,9%.
- Classe C composta ambígua (multi-linha, múltiplos códigos, valor único replicado): 60.247 = 26,1%.
- Classe D sem valor: 76.751 = 33,2%; implausível (> R$ 1 bilhão): 29.

**INFERÊNCIA TÉCNICA.** A Classe A é a única em que o valor da ART pode ser atribuído, sem ambiguidade, a um único serviço. Por isso é a base PRIMÁRIA do cálculo. A Classe B é base secundária/simulação (regra explícita). A Classe C serve apenas para frequência e detecção de serviços novos, **nunca** para cálculo monetário. A Classe D é excluída do cálculo, com volume e motivo documentados.

**RECOMENDAÇÃO.** Todo valor orientativo por serviço deve nascer da Classe A. Onde a Classe A não reunir **n ≥ 5** ARTs para um dado serviço, registrar **"Informação insuficiente para verificar"** e não publicar valor.

---

## Os 15 itens do modelo

### (1) Variável-alvo

- **FATO VERIFICADO.** O campo de valor na base é `valor_contrato`. Entre as ARTs multi-linha, 99.982 têm valor **constante** em todas as linhas e apenas 2.080 variam; conclusão de fato: `valor_contrato` é o valor da **ART inteira**, replicado em cada linha de atividade — **não** é o valor por atividade. Exemplo real: ART `id` 2399866 tem 2 linhas (Laudo e Vistoria), ambas com valor 433.795,00 replicado.
- **INFERÊNCIA TÉCNICA.** A variável-alvo do modelo é o **valor do contrato no nível da ART** (`valor_contrato` deduplicado por `id`), tratado como honorário do escopo declarado na ART.
- **RECOMENDAÇÃO.** Nunca somar linhas de uma mesma ART (multiplica o valor indevidamente). Deduplicar sempre por `id` antes de qualquer estatística monetária.

### (2) Unidade de análise

- **FATO VERIFICADO.** Identificador único de ART: `id` (existe). Volume: 726.028 linhas de atividade; **230.928 ARTs distintas**. 62,6% das ARTs são multi-linha (144.541); 37,4% são linha única (86.387).
- **INFERÊNCIA TÉCNICA.** A unidade de análise monetária é a **ART (`id`)**, não a linha de atividade. A linha de atividade serve para descrever o escopo e classificar o serviço, não para somar dinheiro.
- **RECOMENDAÇÃO.** Toda estatística de valor é calculada sobre o conjunto deduplicado por `id`.

### (3) Quando usar a ART (nível ART) como base de valor

- **INFERÊNCIA TÉCNICA / RECOMENDAÇÃO.** Usar o valor no nível ART quando a ART for **Classe A** (linha única, 1 código, 1 valor plausível): nesse caso o valor da ART corresponde a um único serviço e pode entrar no cálculo orientativo daquele serviço.
- **FATO VERIFICADO de suporte.** Classe A = 53.190 ARTs (23,0%); mediana R$ 2.000; IQR de 800 (P25) a 8.000 (P75).

### (4) Quando usar a atividade (linha) como referência

- **FATO VERIFICADO.** O escopo do serviço está no campo `atividade` (texto livre, padrão "Nível - X  Atividade - Y - DESCRIÇÃO") somado ao campo `codigo`. O campo `atividade` contém `;` internos (o parsing exige ancoragem pela direita).
- **INFERÊNCIA TÉCNICA / RECOMENDAÇÃO.** Usar a **atividade/código** para: (a) rotular o serviço de cada ART Classe A; (b) medir **frequência** de serviços (inclusive em ARTs Classe C); (c) **detectar serviços novos** ausentes da tabela atual. Não usar a linha como portadora de valor monetário próprio (o valor é da ART).

### (5) Quando usar o "serviço" (agregado) como unidade de reporte

- **INFERÊNCIA TÉCNICA.** O "serviço" é o agrupamento de ARTs Classe A que compartilham o mesmo código/atividade (eventualmente harmonizado por família temática equivalente às abas da tabela: Consultoria, Projetos Civis, Cálculo Estrutural, Instalações Elétricas, Saneamento etc.).
- **RECOMENDAÇÃO.** Publicar a faixa orientativa **por serviço** apenas quando o agregado de Classe A daquele serviço tiver **n ≥ 5**. Abaixo disso: "Informação insuficiente para verificar".

### (6) Quando excluir

- **FATO VERIFICADO.** Classe D sem valor: 76.751 (33,2%); ARTs sem valor utilizável: 74.026 (32%); implausíveis (> R$ 1 bilhão): 29; máximo observado ~7,9×10¹¹ (outliers/erros extremos).
- **RECOMENDAÇÃO.** Excluir do cálculo monetário: (a) **Classe D** (sem valor); (b) registros **> R$ 1 bilhão** (erro de digitação/exportação); (c) **Classe C** para qualquer uso monetário (mantida só para frequência/detecção). Sempre documentar volume e motivo da exclusão.

### (7) Modalidade

- **FATO VERIFICADO.** A modalidade/formação está no campo `titulos` (título profissional do responsável, ex.: "Engenheiro Civil"). Nesta base, cada ART carrega **exatamente um** título/modalidade (multi-modalidade = 0%). Medianas de valor por modalidade: Eng. Civil 324.741 reg. (mediana R$ 2.800); Eletricista 118.365 (1.500); Agrônomo 92.344 (186,55); Segurança do Trabalho 49.443 (500); Ambiental 35.828 (2.470); Mecânico 24.762 (1.200); Agrimensor 9.092 (2.000); Minas 5.949 (2.000); Geólogo 5.932 (3.000); Controle/Automação 5.729 (5.000).
- **INFERÊNCIA TÉCNICA.** A modalidade é eixo de **estratificação** das faixas orientativas (há diferença material de mediana entre modalidades). Como cada ART tem uma só modalidade, o cruzamento serviço × modalidade é limpo.
- **RECOMENDAÇÃO.** Calcular faixas por serviço **dentro de cada modalidade**, respeitando o piso n ≥ 5.

### (8) Formação

- **FATO VERIFICADO.** Não há, nesta base, campo distinto de "formação" além de `titulos`. O título profissional é a única informação de formação disponível.
- **INFERÊNCIA TÉCNICA.** "Formação" e "modalidade" coincidem operacionalmente no campo `titulos`.
- Distinção entre formação acadêmica e modalidade de registro além do `titulos`: **Informação insuficiente para verificar.**

### (9) Serviço comum a várias modalidades

- **FATO VERIFICADO.** A mistura entre modalidades **não** aparece no campo `titulos` (multi-modalidade = 0%); quando ocorre, aparece via múltiplos códigos de atividade e no nível do catálogo (mesmo serviço listado em catálogos de modalidades diferentes).
- **INFERÊNCIA TÉCNICA.** Um mesmo serviço (ex.: instalações elétricas) pode ser executado por mais de uma modalidade; isso se reflete em ARTs distintas (uma por modalidade), não numa única ART multi-modal.
- **RECOMENDAÇÃO.** Para serviço comum a várias modalidades, reportar a faixa **por modalidade separadamente** (e, opcionalmente, uma faixa consolidada do serviço com nota de que agrega modalidades distintas). Nunca fundir modalidades de mediana muito divergente sem rótulo.

### (10) Valores compostos

- **FATO VERIFICADO.** 26,5% das ARTs (61.284) têm mais de um código de atividade distinto (escopo composto). A Classe C composta ambígua (multi-linha, múltiplos códigos, valor único replicado) = 60.247 (26,1%): não é possível atribuir o valor a um único serviço.
- **INFERÊNCIA TÉCNICA.** ARTs de escopo composto carregam um valor único para um pacote de serviços; decompor esse valor por serviço seria arbitrário.
- **RECOMENDAÇÃO.** ARTs compostas (Classe C) **não entram** no cálculo monetário por serviço. São usadas apenas para frequência e para sinalizar serviços que costumam ser contratados em conjunto.

### (11) Estatísticas

- **RECOMENDAÇÃO (estatística obrigatória por serviço × modalidade).** Reportar: **mediana**, **IQR** (P25–P75), **n** (número de ARTs Classe A) e, quando útil, P90. **Nunca usar a média** (sensível aos outliers extremos verificados). Aplicar **supressão para n < 5** (publicar "Informação insuficiente para verificar").
- **FATO VERIFICADO de suporte.** A mediana por LINHA (~R$ 1.570) difere da mediana por ART (R$ 1.800) por causa da replicação de valor — evidência de que a estatística deve ser por ART, não por linha. Distribuição no nível ART (deduplicado, valores positivos): mediana 1.800; P25 800; P75 7.272; P90 200.000.

### (12) Faixas orientativas (piso / referência / teto)

- **RECOMENDAÇÃO.** Para cada serviço × modalidade com n ≥ 5 (Classe A), publicar três parâmetros orientativos:
  - **Piso orientativo** = P25;
  - **Referência** = mediana;
  - **Teto orientativo** = P75.
  O P90 pode acompanhar como "limite superior observado" (informativo).
- **FATO VERIFICADO (exemplo, Classe A global, ilustrativo — não substitui o cálculo por serviço):** piso 800 (P25) | referência 2.000 (mediana) | teto 8.000 (P75) | limite superior observado 145.363 (P90).
- **NOTA institucional.** As faixas são **parâmetro orientativo / referência técnica**, de caráter não vinculante; evita-se qualquer leitura de "preço mínimo compulsório" ou "tabela obrigatória".

### (13) Outliers

- **FATO VERIFICADO.** Máximo observado ~7,9×10¹¹; 29 registros implausíveis (> R$ 1 bilhão).
- **RECOMENDAÇÃO.** (a) **Descartar** registros **> R$ 1 bilhão** (erro evidente). (b) Aplicar **winsorização** nas caudas (ex.: limitar aos percentis extremos antes de reportar) para conter distorção residual. (c) Como a estatística central é mediana/IQR, o efeito de outliers já é amortecido; a winsorização é camada adicional de robustez. Documentar o critério aplicado.

### (14) Atualização dinâmica

- **FATO VERIFICADO.** A tabela atual atualiza valores **apenas pela razão do CUB** (coluna 2017-11, CUB R$ 1.369,12 → coluna 2024-06, CUB R$ 1.929,04; ~+40,9%). A base de ARTs aqui é de 2022 (arquivo "ARTs 2022 01022024.csv").
- **INFERÊNCIA TÉCNICA.** O CUB reflete custo de construção civil e é pouco aderente a modalidades não-civis (ex.: fotovoltaica/kWp, agronomia/hectare, automação), que têm dinâmica de preço própria.
- **RECOMENDAÇÃO.** Adotar atualização dinâmica em duas frentes: (a) **reprocessar as ARTs a cada ano** (recalcular medianas/IQR por serviço × modalidade sobre a base mais recente); (b) usar **índice de atualização aderente por modalidade** (não apenas CUB) — p.ex. índice de construção para a faixa civil/estrutural e índice setorial pertinente para as demais modalidades.
- Definição numérica do índice aderente por modalidade (qual índice exato para cada modalidade): **Informação insuficiente para verificar** (requer fonte externa de índices, não presente nos arquivos).

### (15) Validação com especialistas / câmaras

- **RECOMENDAÇÃO.** Antes da publicação, submeter as faixas orientativas às **câmaras especializadas do CREA-BA** e a especialistas por modalidade, para: (a) validar a harmonização serviço↔aba da tabela; (b) revisar serviços sinalizados como novos (ver abaixo); (c) ratificar o caráter orientativo e a redação institucional (LGPD, concorrencial). Registrar pareceres das câmaras como camada de governança.

---

## Anexo — Serviços novos detectados (frequência, não valor)

**FATO VERIFICADO.** O vocabulário real das ARTs evidencia serviços de alto volume ausentes da tabela atual (fortemente civil/estrutural):
- ESPECIFICAÇÃO - RECEITUÁRIO AGRO (60.378) [agronomia, ausente na tabela];
- Microgeração / solar / geração de energia / microgeração fotovoltaica (vários itens 4.500–7.700 cada) [fotovoltaica, ausente];
- Inst. elétr. em baixa tensão (6.000+); rede hidro-sanitária (5.000+); pavimentação (3.224).
- Unidades presentes nas ARTs e ausentes na tabela: **kWp, kVA, kW, hectare** (agronomia). Medianas por unidade: m² 197.540 reg. (2.000); unidade 145.601 (980); quilowatt 46.174 (1.500); kWp 39.751 (1.000); hectare 17.259 (2.000); kVA 10.534 (5.000).

**RECOMENDAÇÃO.** Tratar esses serviços como candidatos prioritários à inclusão na tabela, calculando suas faixas **somente** com ARTs Classe A e n ≥ 5; abaixo disso, "Informação insuficiente para verificar".

---

## Resumo operacional (fluxo de cálculo)

1. Ler ARTs → deduplicar por `id` (unidade = ART).
2. Classificar em A/B/C/D.
3. **Filtrar Classe A**; descartar valores > R$ 1 bilhão; winsorizar caudas.
4. Rotular serviço pela `atividade`/`codigo`; estratificar por modalidade (`titulos`).
5. Para cada serviço × modalidade: se **n ≥ 5**, reportar mediana (referência), P25 (piso), P75 (teto), n; senão, **"Informação insuficiente para verificar"**.
6. Atualizar anualmente reprocessando ARTs + índice aderente por modalidade.
7. Validar com câmaras/especialistas antes de publicar.

*Caráter do documento: subsídio metodológico orientativo para valorização profissional e governança de honorários. Não constitui preço obrigatório nem tabela vinculante.*
