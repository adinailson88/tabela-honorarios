# NOTA TÉCNICA — Subsídio à Nova Metodologia da Tabela de Honorários do SENGE/BA

**Assunto:** Fundamentação metodológica para atualização da Tabela de Honorários dos Profissionais
de Engenharia da Bahia, com uso responsável dos dados de ART como evidência indireta de mercado.
**Data-base dos dados:** 2022 (ARTs CREA-BA). **Emissão:** 2026-06-22.
**Natureza:** documento técnico de subsídio (orientativo); não constitui fixação de preços.

---

## 1. Objeto
Apresentar base técnica para evoluir a metodologia atual da tabela — hoje reajustada exclusivamente
pelo CUB — rumo a um **modelo de governança de honorários em três camadas com calibração empírica**.

## 2. Diagnóstico resumido
1. A atualização atual usa a razão CUB-atual/CUB-anterior. O CUB mede custo de **construção civil por
   m²** e não reflete o esforço profissional de modalidades como elétrica, agronomia, segurança e mecânica.
2. Não há modelo explícito de formação do valor-base por item.
3. Há uma base empírica subutilizada: as ARTs do CREA-BA.

## 3. Evidência empírica (verificável)
A partir do arquivo `ARTs 2022 01022024.csv`, agregado e anonimizado:
- **726.028** linhas de atividade; **230.928** ARTs distintas; **97% na Bahia**; ano 2022.
- Valor declarado: **mediana R$ 1.570**; **IQR R$ 540–8.000**; máximo > R$ 800 milhões (outliers/erros).
- **111 unidades de medida**; predominam m² e "unidade", com volume relevante de **kWp (≈40 mil)** e
  **kVA (≈11 mil)** — confirmando a necessidade de unidades específicas por serviço.
- Modalidades (padronizadas): Civil (324.741) > Eletricista (118.365) > Agrônomo (92.344) >
  Segurança do Trabalho (49.443) > Ambiental (35.828) > Mecânico (24.762).
- Concentração geográfica em Salvador, Feira de Santana, Vitória da Conquista, e no oeste agrícola
  (Barreiras, Luís Eduardo Magalhães, São Desidério).
- **1.047 combinações Atividade × Unidade** com amostra suficiente (n≥5) para faixas robustas.

> **Ressalva central:** o campo `valor_contrato` da ART pode refletir valor de obra, de contrato ou
> declarado — **não necessariamente o honorário**. Portanto, a evidência é **indireta** e usada apenas
> para **calibrar faixas** (mediana/IQR), nunca como prova de preço. Por isso não se utiliza a média.

## 4. Metodologia proposta (síntese)
Modelo em três camadas + calibração (detalhe nos docs 04 e 05 do pacote):
1. **Catálogo de atividades** (Nível + Atividade do CREA).
2. **Valor-base por esforço técnico** = tempo técnico × valor-hora de referência + custos, ancorado no
   piso profissional *(Lei 4.950-A/66 — a confirmar em fonte oficial)*.
3. **Ajuste regional** (modelo de pesos já iniciado em `CidadessCalculo`).
4. **Calibração/validação** contra mediana e IQR observados nas ARTs.
Saída em **faixas**: piso técnico (P25) / referência (mediana) / teto orientativo (P75).

## 5. Tratamento de dados e LGPD
Limpeza, padronização de rótulos e unidades; winsorização de outliers; **supressão de células com n<5**;
publicação **apenas agregada**; **vedação a ranking individual** e a exposição de dados pessoais.

## 6. Cuidados jurídico-concorrenciais
A tabela é **referência técnica orientativa** e instrumento de **valorização profissional e combate ao
aviltamento** — não fixação obrigatória de preços nem restrição concorrencial. Recomenda-se parecer
jurídico (doc. 10, item D2) e confirmação, em fonte oficial, das normas citadas (Lei 4.591/64,
NBR 12.721, Lei 4.950-A/66 e atos Confea/Crea). Onde não verificável: **"Informação insuficiente para verificar"**.

## 7. Conclusão e encaminhamentos
A evidência disponível é suficiente para **fundamentar a arquitetura metodológica e faixas iniciais
de referência**, mas **não** para fixar honorários definitivos — estes dependem da definição de
valor-hora/tempo técnico e da pesquisa de preços com as entidades. Encaminha-se:
1. aprovação da arquitetura (3 camadas + calibração);
2. definição de parâmetros pela comissão;
3. pesquisa de preços (≥5 por item);
4. validação jurídica;
5. publicação da v1 com o painel de evidências (`dashboard/`) e a `PLANILHA_MODELO_HONORARIOS.xlsx`.

---
*Documento de subsídio. Nenhum valor de honorário foi fixado ou inventado.*
