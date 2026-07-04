# CHECKLIST — DASHBOARD METODOLOGIA POR SERVIÇO
## Testes do `dashboard_senge_honorarios_metodologia_servicos.html`

> Abra o arquivo (duplo clique; não requer internet). Marque cada item: ✅ aprovado · ❌ reprovado · 📝 obs.
> Números de referência (base 2022) já confirmados na verificação automatizada. Data: 2026-06-24.

---

| # | Teste | Resultado esperado | Ref. | ✅/❌ | Obs. |
|---|---|---|---|:--:|---|
| 1 | **Filtro Classe A** | KPIs monetários ativos; base de cálculo = ARTs filtradas | base A 53.190 | ☐ | |
| 2 | **Filtro Classe B** | conta ARTs B; monetário oculto/avisado (B não calcula) | B 38.631 | ☐ | |
| 3 | **Filtro Classe C** | só frequência; **sem** KPI monetário; aviso visível | C 62.327 | ☐ | |
| 4 | **Filtro Classe D** | só volume; **sem** KPI monetário; aviso visível | D 76.780 | ☐ | |
| 5 | **Filtro só C + D** | ARTs 139.107; base A = 0; mediana/IQR = "—"; aviso | 139.107 | ☐ | |
| 6 | **Filtro por serviço** (Fotovoltaica) | ARTs 31.811; base A 1.645; mediana R$ 1.000; IQR 100–1.500 | — | ☐ | |
| 7 | **Filtro por grupo** (ex.: "Serviço novo - Energia") | mostra só serviços do grupo | — | ☐ | |
| 8 | **Filtro por município** (busca + seleção) | recalcula ARTs/mediana para o município | — | ☐ | |
| 9 | **Filtro por ano** | só 2022 disponível (base atual) | 2022 | ☐ | |
| 10 | **ARTs ≠ atividades** | contadores distintos (não somam linhas) | 230.928 vs 320.551 | ☐ | |
| 11 | **Mediana só base confiável** | mediana/IQR calculados apenas sobre Classe A | mediana 2.000 (s/filtro) | ☐ | |
| 12 | **Serviço n < 5** | linha marcada "Informação insuficiente para verificar" + tag `n<5` | (acionável ao refinar serviços) | ☐ | |
| 13 | **Serviços novos/lacunas** | tag `novo` em fotovoltaica, receituário, ambiental, agrimensura, segurança | — | ☐ | |
| 14 | **Botão Limpar filtros** | restaura base completa (ARTs 230.928; mediana 2.000) | 230.928 | ☐ | |
| 15 | **Indicador de filtros ativos** | lista os filtros aplicados | — | ☐ | |
| 16 | **Barra de classes** | A 23,0% · B 16,7% · C 27,0% · D 33,2% | — | ☐ | |
| 17 | **Metodologia visível** | seção com a frase "evidência auxiliar, indireta e agregada" | — | ☐ | |
| 18 | **Sem dados pessoais** | nenhuma ART individual, nome, contratante ou ranking | — | ☐ | |

---

## Observações de uso
- **Selecionar vários itens** num filtro: segure **Ctrl** (ou **Shift**) e clique.
- **Município:** use a caixa "filtrar lista..." para reduzir as ~1.984 opções antes de selecionar.
- **Monetário só na Classe A:** ao excluir A do filtro, mediana/IQR e a tabela de serviços ficam
  indisponíveis e um aviso é exibido — comportamento **esperado** (apenas A fundamenta valor).
- **Mapa:** a visão geográfica permanece no painel anterior
  `dashboard_senge_honorarios_corrigido_codex.html` (preservado).

## Campo livre — problemas encontrados
1. _______________________________________________________________
2. _______________________________________________________________

**Navegador usado:** ______________  **Data do teste:** ____________
