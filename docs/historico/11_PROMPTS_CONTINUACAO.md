# 11 — Prompts de Continuação

> Prompts prontos para retomar o trabalho (nesta ou em outra ferramenta de IA).
> Copie e cole o bloco desejado. Todos preservam as regras de segurança (não inventar, LGPD, só agregados).

---

## 1. Melhorar a proposta institucional
```
Aja como consultor técnico-institucional do SENGE/BA. Leia 08_PROPOSTA_INSTITUCIONAL.md e
02_DIAGNOSTICO_METODOLOGIA_EXISTENTE.md na pasta PROPOSTA CLAUDE. Refine o texto para apresentação
formal ao CREA-BA, fortalecendo o enquadramento orientativo (anti-cartel), a fundamentação técnica
e a clareza. Não invente normas nem valores; marque o que não puder verificar como
"Informação insuficiente para verificar". Salve como 08_PROPOSTA_INSTITUCIONAL_v2.md.
```

## 2. Criar apresentação PowerPoint
```
Use 09_ROTEIRO_APRESENTACAO_CREA_SENGE.md e 07_INDICADORES_E_GRAFICOS_RECOMENDADOS.md para gerar
um deck .pptx (12–15 slides) para CREA-BA/SENGE-BA. Tom institucional e técnico. Inclua slides de
problema, dados de ART, limites dos dados, modelo de 3 camadas, faixas, governança e próximos passos.
Não inclua valores monetários (ainda não calculados). Salve em PROPOSTA CLAUDE.
```

## 3. Criar dashboard
```
Construa um dashboard HTML estático (arquivo único) com os blocos 1–11 do
07_INDICADORES_E_GRAFICOS_RECOMENDADOS.md, a partir de agregados da base de ARTs 2022. Use mediana/IQR,
suprima células com n<5, rotule fonte e a ressalva "valor de ART não é honorário". Nenhum dado pessoal.
Salve em PROPOSTA CLAUDE/dashboard.
```

## 4. Analisar planilhas de ART
```
Implemente a metodologia de 05_METODOLOGIA_ANALITICA_ARTS.md sobre 'ARTs 2022 01022024.csv'
(parsing robusto: campo atividade tem ';' interno; ancorar colunas pela direita). Gere agregados por
Atividade x Unidade x Município (mediana, IQR, n), com supressão n<5. Não exponha dados pessoais.
Salve apenas CSVs agregados em PROPOSTA CLAUDE. Não altere o arquivo original.
```

## 5. Transformar a metodologia em minuta de resolução/recomendação
```
Com base em 04, 05 e 08, redija uma minuta de RECOMENDAÇÃO TÉCNICA (não resolução impositiva) do
SENGE/BA sobre honorários de referência, com caráter orientativo e foco anti-aviltamento. Confirme
todas as normas citadas em fonte oficial; o que não verificar, marque como "Informação insuficiente
para verificar". Salve como MINUTA_RECOMENDACAO_TECNICA.md em PROPOSTA CLAUDE.
```

## 6. Preparar reunião com CREA-BA/SENGE
```
Prepare um briefing de 1 página + lista de perguntas/objeções prováveis (com respostas) para reunião
no CREA-BA sobre a nova metodologia de honorários, usando 09_ROTEIRO_APRESENTACAO_CREA_SENGE.md.
Salve como BRIEFING_REUNIAO.md em PROPOSTA CLAUDE.
```

## 7. Gerar planilha-modelo de honorários
```
Gere uma planilha-modelo (.xlsx) da tabela de honorários com a estrutura do doc. 08 §8 e os itens de
06_MATRIZ_ATIVIDADES_HONORARIOS.csv. Colunas de valor ficam vazias ou com "Informação insuficiente
para verificar" até a calibração. Não invente valores. Salve em PROPOSTA CLAUDE.
```

## 8. Gerar nota técnica
```
Redija uma NOTA TÉCNICA do SENGE/BA fundamentando a nova metodologia (3 camadas + calibração por ARTs),
citando os achados verificáveis do doc. 03 (n=726.028 registros 2022, mediana R$1.600, IQR 520–8.000,
ressalva de unidades). Confirme normas em fonte oficial; marque incertezas. Salve como NOTA_TECNICA.md.
```

---

*Documento derivado. Não altera os arquivos originais.*
