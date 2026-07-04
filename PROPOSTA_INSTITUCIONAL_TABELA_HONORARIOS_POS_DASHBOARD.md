# PROPOSTA INSTITUCIONAL — NOVA METODOLOGIA DA TABELA DE HONORÁRIOS
## SENGE/BA · CREA-BA · Entidades de Classe da Engenharia da Bahia

> Documento institucional. Usa o dashboard de evidências como **instrumento de apoio**, sem dele depender
> exclusivamente. Onde houver dependência de fonte oficial ainda não confirmada, consta
> **"Informação insuficiente para verificar"**. Nenhum valor, norma ou número foi inventado.
> Data: 2026-06-23. Versão pós-revisão do dashboard.

---

## 1. Apresentação
O Sindicato dos Engenheiros no Estado da Bahia (SENGE/BA) mantém a Tabela de Honorários dos profissionais
de engenharia. Esta proposta apresenta uma **evolução metodológica**: substituir a lógica de "lista de
preços reajustada por um único índice" por um **modelo de governança de honorários** — tecnicamente
fundamentado, regionalizado, baseado em evidências agregadas e juridicamente seguro, de caráter
**orientativo**. O instrumento de apoio empírico é um painel de evidências construído a partir de dados
agregados de ART do CREA-BA (período 2015–2022).

## 2. Contexto
A tabela atual reajusta valores pela razão entre o CUB corrente e o anterior. O próprio projeto interno
reconhece que esse índice não acompanha mais fielmente a evolução de preços e que faltam serviços novos
(p. ex. energia fotovoltaica) e unidades de medida adequadas (kVA, kWp, m³, hectare). Em paralelo, existe
um ativo subutilizado: uma base de centenas de milhares de registros de atividade de ART na Bahia, capaz
de servir como **evidência indireta de mercado**.

## 3. Problema
1. Índice único (CUB da construção) aplicado a todas as modalidades.
2. Valor de referência sem modelo de cálculo rastreável.
3. Cobertura desatualizada de serviços e de unidades de medida.
4. Evidência empírica disponível, porém pouco utilizada.
5. Risco de leitura concorrencial indevida (interpretação como tabelamento obrigatório).

## 4. Justificativa
Uma metodologia defensável precisa ser **transparente, atualizável e fundamentada em evidências**, sem
incorrer em fixação compulsória de preços. O uso **cauteloso e agregado** dos dados de ART permite
calibrar faixas de referência por atividade, modalidade, unidade e região, fortalecendo a função de
**valorização profissional e combate ao aviltamento** — sem caráter impositivo.

## 5. Objetivos
- **Geral:** propor metodologia defensável, transparente e atualizável para a tabela de honorários.
- **Específicos:** (a) integrar artefatos existentes (catálogo de atividades/TOS, regionalização, tabela
  atual); (b) usar ARTs como **calibração e validação**; (c) substituir preço único por **faixas**;
  (d) instituir **governança anual** documentada; (e) assegurar o **enquadramento orientativo**.

## 6. Base empírica disponível
- Base agregada de ART do CREA-BA, período **2015–2022** (8 anos), tratada de forma anonimizada.
- Indicadores robustos de **frequência** por atividade, modalidade, município, unidade e tipo de ART.
- Faixas de valor por atividade × unidade (mediana/IQR), com indicador de confiabilidade.
- Painel interativo de evidências e planilha-modelo estruturada (sem valores inventados).
- Cobertura geográfica: 161 dos 417 municípios da Bahia (municípios com ART na base).

## 7. Papel dos dados de ART
> **"Os dados de ART são utilizados como evidência auxiliar, indireta e agregada de escopo, atividade,
> localidade, responsabilidade técnica e valor declarado, não como prova isolada do honorário profissional
> efetivamente contratado."**

Os dados de ART **calibram e validam** as faixas de referência; **não** substituem a pesquisa de preços
nem definem, isoladamente, o honorário praticado.

## 8. Limitações dos dados de ART
1. O valor declarado pode refletir valor de obra, de contrato ou mera declaração — não necessariamente o
   honorário.
2. Há outliers e erros de digitação (até ordens de grandeza implausíveis) → exigem mediana/IQR e
   winsorização; **a média é inadequada**.
3. Alta heterogeneidade de unidades de medida e de texto de atividade → exigem padronização/dicionário.
4. Possível sub ou sobredeclaração de valores.
5. Confiabilidade variável por atividade × unidade (sinalizar quando o teto se afasta muito da mediana).

## 9. Critérios metodológicos propostos
- **Estatística robusta:** mediana e IQR por **atividade × unidade homogênea** (nunca média; nunca misturar
  unidades).
- **Faixas:** piso técnico – referência – teto, em vez de valor único.
- **Padronização:** modalidades, unidades e municípios normalizados.
- **Regionalização:** fator regional calibrado por dados (camada já iniciada em artefatos existentes).
- **Atualização por índice aderente** a cada modalidade (CUB para construção; alternativa fundamentada
  para as demais).
- **Não invenção:** itens sem base recebem "Informação insuficiente para verificar".

## 10. Modelo de governança da tabela
- **Comissão multidisciplinar** presidida pelo SENGE/BA, com participação das câmaras especializadas.
- **Ciclo anual:** manter / atualizar / inserir itens, com recalibração pela base de ARTs mais recente.
- **Documentação:** nota técnica + versionamento + changelog a cada revisão.
- **Curadoria permanente** e trilha de auditoria das fontes.

## 11. Possíveis indicadores de apoio
Mediana e IQR por atividade×unidade; n por célula (com supressão n<5); coeficiente de variação;
frequência por modalidade/município; fator regional; aderência modelo × ART. (Detalhe na metodologia
analítica e na versão institucional da metodologia do painel.)

## 12. Proposta de validação junto às entidades
1. Aprovação da **arquitetura metodológica** (faixas + calibração + governança) pelo SENGE/BA e CREA-BA.
2. **Pesquisa de preços** com entidades (mínimo recomendado de respondentes por item) para ancorar valores.
3. Validação das **dimensões territoriais** (município → unidade CREA) em fonte oficial.
4. Apreciação pelas **câmaras especializadas** por modalidade.
5. Publicação da **v1** com nota técnica, painel de evidências e changelog.

## 13. Cuidados LGPD
- Tratamento **exclusivamente agregado e anonimizado**; supressão de células com n < 5.
- **Sem ranking individual** de profissionais, empresas, contratantes ou proprietários.
- Nenhum identificador (id de ART, nome, endereço) em artefatos publicados.

## 14. Cuidados concorrenciais
- A tabela é **referência técnica e parâmetro orientativo** de valorização profissional e combate ao
  aviltamento — **não** fixação obrigatória de preços.
- Evitar qualquer redação que sugira tabelamento, preço mínimo compulsório ou restrição concorrencial.
- Recomenda-se **parecer jurídico** confirmando o enquadramento orientativo antes da publicação.

## 15. Encaminhamentos
1. Aprovar a arquitetura metodológica (faixas + calibração + governança).
2. Constituir/ativar a comissão e definir parâmetros (tempo técnico, valor-hora, multiplicadores).
3. Executar a pesquisa de preços e a análise das ARTs (mediana/IQR).
4. Confirmar a base legal e o enquadramento orientativo em fonte/parecer oficial.
5. Consolidar as dimensões territoriais com o CREA-BA.
6. Publicar a v1 com nota técnica e dashboard de evidências.

---
*Documento institucional derivado. Não altera arquivos originais. Vocabulário: referência técnica,
parâmetro orientativo, subsídio metodológico, matriz de complexidade, estimativa de esforço, valorização
profissional, governança de honorários.*
