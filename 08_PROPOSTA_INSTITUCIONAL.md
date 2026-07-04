# 08 — Proposta Institucional
## Nova Metodologia para a Tabela de Honorários dos Profissionais de Engenharia da Bahia

> Documento institucional para apresentação ao CREA-BA, SENGE-BA e entidades de classe.
> Onde há dependência de fonte oficial ainda não verificada, consta **"Informação insuficiente para verificar"**.

---

### 1. Apresentação

O Sindicato dos Engenheiros da Bahia (SENGE/BA) elabora e mantém a Tabela de Honorários dos
Profissionais de Engenharia da Bahia. A presente proposta apresenta uma **evolução metodológica**:
sair de uma lista de preços reajustada apenas pelo CUB e avançar para um **modelo de governança
de honorários** — tecnicamente fundamentado, regionalizado, baseado em evidências e juridicamente seguro.

### 2. Justificativa

A metodologia atual reajusta os valores pela razão entre o CUB atual e o anterior. O próprio
projeto interno reconhece que esse índice "não acompanha mais fielmente a evolução dos preços" e
que faltam serviços novos (ex.: energia fotovoltaica) e unidades adequadas (kVA, kWp, m³, hectare).
Há, simultaneamente, um ativo subutilizado: **uma base de mais de 726 mil registros de atividade
de ART de 2022 na Bahia**, que pode servir como evidência indireta de mercado.

### 3. Problema

1. Índice único (CUB de construção) aplicado a todas as modalidades.
2. Valor de referência sem modelo de cálculo rastreável.
3. Cobertura desatualizada (serviços e unidades).
4. Evidência empírica disponível, porém não utilizada.
5. Risco de leitura concorrencial indevida (tabelamento).

### 4. Objetivos

- **Geral:** propor metodologia defensável, transparente e atualizável para a tabela de honorários.
- **Específicos:** (a) integrar os artefatos já existentes (catálogo TOS, regionalização, tabela atual);
  (b) usar ARTs como calibração; (c) substituir preço único por faixas; (d) instituir governança anual;
  (e) blindar juridicamente o caráter orientativo.

### 5. Fundamentos técnicos

Modelo em três camadas + calibração (detalhe no doc. 04):

1. **Catálogo de atividades** (códigos CREA Nível+Atividade — base da `TABELA TOS`).
2. **Valor-base por esforço técnico** (tempo técnico × valor-hora de referência + custos),
   ancorado no piso profissional *(Lei 4.950-A/66 — a confirmar por fonte oficial)*.
3. **Ajuste regional** (modelo de pesos já iniciado em `CidadessCalculo`).
4. **Calibração empírica** contra mediana e IQR das ARTs (doc. 05).

### 6. Uso responsável dos dados de ART

- A ART é **evidência indireta**: `valor_contrato` pode refletir obra/contrato/declaração, **não
  necessariamente o honorário**. Usada para **calibrar/validar faixas**, com ressalva explícita.
- Tratamento **exclusivamente agregado e anonimizado**; supressão de recortes com n < 5;
  **sem ranking individual**; sem exposição de profissionais, contratantes ou ARTs específicas (LGPD).

### 7. Critérios metodológicos

- **Mediana e IQR** (não média), por atividade × unidade homogênea.
- **Winsorização** de outliers; descarte de valores implausíveis.
- **Padronização** de modalidades, unidades e cidades.
- **Faixas** (piso técnico – referência – teto) em vez de valor único.
- **Atualização** por índice aderente a cada modalidade (CUB para construção; alternativa fundamentada para as demais).

### 8. Proposta de estrutura da tabela

Para cada item: grupo · atividade (código CREA) · modalidade · unidade · faixa (piso/ref/teto) ·
fator regional · fonte/data-base · nota de confiabilidade. (Esqueleto em `06_MATRIZ_ATIVIDADES_HONORARIOS.csv`.)
**Valores monetários só após a pesquisa de preços e a calibração** — não inventados.

### 9. Governança de atualização

- Comissão multidisciplinar presidida pelo SENGE (já prevista no projeto).
- Ciclo **anual**: manter / atualizar / inserir (Proporção de 1/3).
- **Nota técnica + versionamento + changelog** a cada revisão.
- Recalibração com a base de ARTs mais recente.
- Curadoria permanente do SENGE/BA.

### 10. Cuidados jurídicos, éticos e de LGPD

- **Caráter orientativo**, não impositivo: a tabela é **referência técnica e instrumento de
  valorização profissional e combate ao aviltamento**, não fixação obrigatória de preços.
  Evitar qualquer redação que sugira tabelamento ou restrição concorrencial.
- Conformidade LGPD: apenas agregados; sem dados pessoais; sem ranking individual.
- **Validade jurídica de normas citadas:** *Informação insuficiente para verificar* — confirmar a
  redação/vigência de Lei 4.591/64, NBR 12.721, Lei 4.950-A/66 e atos do sistema Confea/Crea
  em fonte oficial antes da versão final.

### 11. Encaminhamentos

1. Aprovar a arquitetura metodológica (3 camadas + calibração).
2. Constituir/ativar a comissão e definir parâmetros (tempo técnico, valor-hora, multiplicadores).
3. Executar a pesquisa de preços e a análise das ARTs.
4. Validar juridicamente o enquadramento orientativo.
5. Publicar a v1 com nota técnica e dashboard de evidências.

---

*Documento derivado. Não altera os arquivos originais. Nenhum valor, norma ou número foi inventado.*
