# AUDITORIA METODOLÓGICA DO DASHBOARD
## Proposta de nova metodologia da tabela de honorários — SENGE/BA

> Avalia se o dashboard corrigido (`dashboard_senge_honorarios_corrigido_codex.html`) comunica de forma
> clara e metodologicamente honesta o que mostra, o que NÃO prova e quais são seus limites.
> Data: 2026-06-23. Não altera o dashboard.

---

## Quadro-resumo da auditoria

| # | Critério exigido | Situação no painel | Veredito |
|---|---|---|---|
| 1 | Objetivo claro | Declarado na Metodologia | ✔ Atende |
| 2 | Quais dados são usados | ARTs CREA-BA (agregadas) | ✔ Parcial — falta precisão de fonte |
| 3 | Período da base | **Ambíguo**: dados 2015–2022, metadado diz "2022" | ✖ Corrigir |
| 4 | Quais filtros existem | 5 reais (ano, município, modalidade, unidade, tipo) | ✔ Atende |
| 5 | Filtros são multisseleção | Sim | ✔ Atende |
| 6 | Base vai de 2015 a 2022 | Verdadeiro nos dados; **não afirmado no painel** | ✖ Tornar explícito |
| 7 | 2024/2026 retornam zero por ausência | Retorna 0, mas **sem aviso** ao usuário | △ Melhorar UX |
| 8 | ART ≠ honorário | Dito na frase-chave | ✔ Atende |
| 9 | Valor declarado = evidência auxiliar/indireta/agregada | Frase-chave presente | ✔ Atende |
| 10 | Não é imposição obrigatória de preço | Dito ("sem tabela vinculante/preço obrigatório") | ✔ Atende |
| 11 | Resultado é subsídio orientativo/metodológico | Dito | ✔ Atende |
| 12 | Cuidados LGPD | Mencionado (agregação, sem identificação) | ✔ Parcial — reforçar n<5 |
| 13 | Cuidados concorrenciais | Mencionado ("sem imposição concorrencial") | ✔ Parcial — reforçar |
| 14 | Outliers/dispersão com mediana/quartis/IQR | Conceito existe nos agregados, **mas não filtrável** | ✖ Lacuna analítica |

---

## 1. Objetivo
**O painel deixa claro o objetivo?** Sim. A Metodologia declara que o dashboard "organiza evidências
agregadas de ARTs para subsidiar uma referência técnica e orientativa da nova metodologia de honorários
do SENGE/BA, sem produzir tabela vinculante, preço obrigatório ou imposição concorrencial de valores."
**Recomendação:** elevar essa frase para o topo visível do painel (cabeçalho), não só na seção final.

## 2. Quais dados são usados
Origem: dados de ART do CREA-BA, tratados de forma agregada. **Ponto a corrigir:** o metadado de fonte
(`data.json`) cita apenas o arquivo de 2022, mas a base efetivamente carregada agrega 2015–2022. A fonte
declarada deve refletir **todas** as bases usadas (CSV 2022 + bases .xls/.xlsx 2015–2021).

## 3. Período da base — ACHADO CRÍTICO
A base agregada (`flat_counts.json`) contém os anos **2015 a 2022** (8 anos; 1.600.340 linhas de
atividade somadas). Entretanto, o metadado e o diagnóstico anterior descreviam apenas 2022. **Isso muda
a leitura de todos os números do painel.** Exemplo: Salvador = 184.099 atividades (2015–2022), e não
85.347 (que era o número só de 2022). **Os dois estão corretos; mudam apenas pelo período.**
**Recomendação obrigatória:** rotular o período em local visível ("Base agregada de ARTs — Bahia —
2015 a 2022") e padronizar os metadados.

## 4–6. Filtros, multisseleção e abrangência temporal
Existem 5 filtros reais e funcionais (ano, município, modalidade, unidade, tipo de ART), todos
multisseleção, com regra **OU dentro do filtro / E entre filtros**. A base cobre 2015–2022.
**Recomendação:** o seletor de Ano deve exibir explicitamente apenas 2015–2022, deixando claro que não
há anos posteriores. (A Metodologia menciona filtros adicionais — inspetoria, SUREG, situação, grupo,
faixa — que **ainda não existem** na base; a redação deve ser corrigida para não prometer o inexistente.)

## 7. Filtros para 2024 e 2026
Tecnicamente corretos: retornam 0 porque esses anos não existem na base. **Risco de UX:** o usuário pode
interpretar "0" como "nenhuma atividade" em vez de "ano inexistente na base". **Recomendação:** quando o
recorte resultar em 0 por ano fora de 2015–2022, exibir a mensagem padrão
**"Informação insuficiente para verificar — a base disponível cobre 2015 a 2022."**

## 8–9. ART não é honorário (formulação obrigatória)
O painel já traz a formulação exigida. Esta auditoria a **reafirma como cláusula metodológica central**:

> **"Os dados de ART são utilizados como evidência auxiliar, indireta e agregada de escopo, atividade,
> localidade, responsabilidade técnica e valor declarado, não como prova isolada do honorário
> profissional efetivamente contratado."**

Justificativa técnica (do diagnóstico de dados): o campo `valor_contrato` mistura valor de obra, valor de
contrato e valor declarado; apresenta outliers de até ~8,4×10¹¹ e salto da mediana (~R$1.570) para o P90
(~R$580 mil). Logo, **média é inútil**; só mediana e IQR, por atividade × unidade homogênea, são defensáveis.

## 10–11. Caráter orientativo, não impositivo
O painel afirma que não produz tabela vinculante nem preço obrigatório, e que serve de referência técnica
orientativa. **Recomendação de linguagem:** padronizar o vocabulário em todo o material — usar
"referência técnica", "parâmetro orientativo", "subsídio metodológico", "combate ao aviltamento"; **evitar**
"preço mínimo", "preço obrigatório", "tabela vinculante", "todos devem cobrar".

## 12. LGPD
O painel afirma tratamento apenas agregado, sem identificação de profissionais, empresas, contratantes ou
proprietários. **Recomendações de reforço:**
- Aplicar e declarar **supressão de células com n < 5** (anti-reidentificação).
- Declarar que **não há ranking individual** de profissionais/empresas/contratantes (regra do projeto).
- Confirmar que nenhum identificador (id de ART, nome, endereço) chega ao arquivo publicado.

## 13. Cuidados concorrenciais
O painel sinaliza que não há imposição concorrencial. **Recomendação:** incluir nota explícita de que a
tabela é instrumento de **valorização profissional e combate ao aviltamento**, não acordo de preços,
em conformidade com a defesa da concorrência. (Reforçar na proposta institucional e no roteiro.)

## 14. Outliers e dispersão — LACUNA ANALÍTICA
O conceito correto (mediana, quartis, IQR, winsorização) já consta da metodologia analítica documentada
(`05_METODOLOGIA_ANALITICA_ARTS.md`) e dos agregados de `data.json`. **Porém, o painel não recalcula
distribuição (mediana/IQR) sobre o recorte filtrado**, porque a base interativa (`flat_counts.json`) só
contém contagens, sem microdados monetários. **Recomendação:** próxima rodada deve incluir um agregado de
**mediana/P25/P75/n por (atividade × unidade) e por (modalidade) e por (município/região)**, com supressão
n<5, permitindo uma seção "Distribuição estatística" que responda aos filtros. (Ver
`PROMPT_CODEX_PROXIMA_RODADA.md`.)

---

## Conclusão da auditoria
O dashboard é **metodologicamente honesto** nos pontos centrais (ART como evidência auxiliar, caráter
orientativo, agregação, não invenção territorial). As **três correções prioritárias** são:
1. **Período da base** (tornar 2015–2022 explícito e padronizar metadados);
2. **Alinhar a Metodologia à base real** (não prometer filtros inexistentes);
3. **Distribuição estatística filtrável** (mediana/IQR por recorte) — maior ganho analítico futuro.

Enquanto essas correções não forem feitas, o painel pode ser usado **internamente** como instrumento de
trabalho, mas a apresentação externa deve vir acompanhada das ressalvas desta auditoria.

---
*Documento de auditoria. Não altera o dashboard nem os dados.*
