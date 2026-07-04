# ROTEIRO DE TESTE VISUAL DO DASHBOARD (PASSO A PASSO)
## Para Adinailson validar o `dashboard_senge_honorarios_corrigido_codex.html` no navegador

> Use este roteiro com o dashboard aberto. **Ligue a internet** (o mapa depende dela). Marque cada item.
> Onde houver número de referência, ele vem do teste do Codex sobre a base **2015–2022** (não 2022).
> Data: 2026-06-23.

**Como abrir:** dê duplo clique em `dashboard_senge_honorarios_corrigido_codex.html` (ou abra pelo
`_ABRIR_AQUI.html`). Navegador recomendado: Chrome ou Edge atualizados.
**Como selecionar vários itens num filtro:** segure **Ctrl** e clique em cada opção (ou **Shift** para
intervalo).

---

| # | Passo | O que observar | Referência esperada | Aprovado | Reprovado | Observação |
|---|---|---|---|:---:|:---:|---|
| 1 | Filtrar **Município = Itabuna** | Contador, KPIs, gráficos e tabela mudam | ~**18.973** atividades | ☐ | ☐ | |
| 2 | Filtrar **Município = Ilhéus** | Idem | ~**22.000** atividades | ☐ | ☐ | |
| 3 | Filtrar **Município = Salvador** | Idem | ~**184.099** atividades | ☐ | ☐ | |
| 4 | **Itabuna + Ilhéus** (Ctrl-clique) | Soma os dois (regra OU) | ~**40.973** atividades | ☐ | ☐ | |
| 5 | **Ano = 2015 + 2022** | Combina os dois anos | >0 (ambos existem) | ☐ | ☐ | |
| 6 | **Ano = 2024 + 2026** | Deve dar **zero** | **0** — "base cobre 2015–2022" | ☐ | ☐ | |
| 7 | Indicador de **filtros ativos** | Mostra os filtros aplicados | Aparece e lista corretamente | ☐ | ☐ | |
| 8 | Botão **Limpar filtros** | Zera tudo | Volta ao total geral | ☐ | ☐ | |
| 9 | **Contador total/filtrado** | Muda a cada filtro | Filtrado ≤ total | ☐ | ☐ | |
| 10 | **KPIs** (contagens) | Mudam com o filtro | Sim para contagens | ☐ | ☐ | |
| 11 | **KPIs de valor** (mediana/IQR) | *Podem NÃO mudar* | Esperado: globais (não filtram) | ☐ | ☐ | |
| 12 | **Gráficos** | Mudam com o filtro | Barras/linhas refletem recorte | ☐ | ☐ | |
| 13 | **Tabela agregada** | Muda com o filtro | Linhas refletem recorte | ☐ | ☐ | |
| 14 | **Mapa carrega** | Aparece o mapa da Bahia | Sim (com internet) | ☐ | ☐ | |
| 15 | **Município destacado** | Ao filtrar um município | Destaque visual na malha | ☐ | ☐ | |
| 16 | Seção **Metodologia** | Está visível e legível | Sim | ☐ | ☐ | |
| 17 | **Erros visuais/textos confusos** | Layout, acentuação, sobreposição | Sem erros graves | ☐ | ☐ | |

---

## Notas importantes para a interpretação do teste
- **Item 3 e 4 (números altos):** os valores são de **2015–2022**, não de 2022. Não estranhe Salvador com
  184 mil — é a soma de 8 anos. Se quiser o número de 2022, filtre **Ano = 2022** junto com o município.
- **Item 6 (zero):** zero aqui é **correto** — não é bug. A base não tem 2024/2026. O ideal (melhoria
  futura) é o painel exibir a frase "Informação insuficiente para verificar".
- **Item 11 (KPIs de valor):** se mediana/IQR **não** mudarem ao filtrar município/modalidade, isso é
  **esperado** nesta versão (a base interativa só tem contagens). Anote como "comportamento conhecido",
  não como reprovação.
- **Itens 14–15 (mapa):** se o mapa **não** carregar, primeiro confirme a internet. Sem internet, marque
  "Reprovado por ausência de rede" — não é defeito do painel.

## Campo livre — problemas encontrados (resumo para a próxima rodada do Codex)
> Preencha e depois copie para `PROMPT_CODEX_PROXIMA_RODADA.md`.

1. _______________________________________________________________
2. _______________________________________________________________
3. _______________________________________________________________

**Navegador usado:** ______________  **Internet ligada?** (S/N) ______  **Data do teste:** __________
