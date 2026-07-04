# PROMPT PARA O CODEX — PRÓXIMA RODADA DE CORREÇÃO
## Usar DEPOIS do teste visual do dashboard

> Copie o bloco abaixo e cole para o Codex. Preencha os campos editáveis com o que você observou no teste
> (`ROTEIRO_TESTE_VISUAL_USUARIO.md`). O objetivo é **corrigir pontos específicos**, **sem refazer tudo**.
> Data: 2026-06-23.

---

## BLOCO PARA COLAR NO CODEX

```
Você é o engenheiro que já corrigiu o dashboard SENGE de honorários. NÃO refaça do zero.
Trabalhe sobre a sua própria versão corrigida e aplique apenas os ajustes listados.

Pasta de trabalho:
C:\Users\adina\Meu Drive\SENGE\PROPOSTA CLAUDE

Arquivo HTML base (NÃO apagar, NÃO sobrescrever — gerar nova cópia com novo nome):
dashboard_senge_honorarios_corrigido_codex.html
Nova saída sugerida: dashboard_senge_honorarios_corrigido_codex_v2.html

Regras de segurança (iguais às anteriores):
- Não apagar nem mover arquivos originais.
- Não sobrescrever o HTML anterior; criar nova cópia versionada.
- Não inventar valores, normas, municípios, inspetorias, SUREG ou códigos IBGE.
- Apenas dados agregados; sem dados pessoais; sem ranking individual.
- Onde faltar fonte, escrever exatamente: "Informação insuficiente para verificar".
- Não trabalhar fora da pasta PROPOSTA CLAUDE.

CORREÇÕES PRIORITÁRIAS (de revisão técnica já feita):
1. PERÍODO DA BASE: a base agregada (dados/flat_counts.json) cobre 2015–2022, mas o metadado
   dados/data.json -> "fonte" diz só "2022" e "totais.linhas_atividade" = 726028 (só 2022).
   Padronizar: exibir no cabeçalho e na Metodologia "Base agregada de ARTs — Bahia — 2015 a 2022"
   e ajustar/explicar os metadados de fonte e totais para refletir 2015–2022.
2. METODOLOGIA x FILTROS REAIS: o texto da Metodologia cita filtros de inspetoria, supervisão
   regional, situação, grupo de atividade e faixa de valor que NÃO existem na base. Corrigir a
   redação para listar só os 5 filtros reais (ano, município, modalidade, unidade, tipo de ART) e
   marcar os demais como "previstos para versões futuras".
3. AVISO DE ZERO POR ANO INEXISTENTE: quando o recorte resultar em 0 só por causa de ano fora de
   2015–2022, exibir a mensagem "Informação insuficiente para verificar — a base cobre 2015 a 2022".
4. KPIs DE VALOR: deixar explícito no painel que mediana/IQR exibidos são GLOBAIS e ainda NÃO
   respondem aos filtros (a base interativa só tem contagens).
5. (SE HOUVER DADO) DISTRIBUIÇÃO ESTATÍSTICA FILTRÁVEL: se for possível gerar um agregado de
   mediana/P25/P75/n por (atividade×unidade), por (modalidade) e por (município), com supressão de
   células n<5, criar uma seção "Distribuição estatística" que responda aos filtros. Se não houver
   microdados monetários disponíveis na pasta, NÃO inventar: registrar como pendência.

PROBLEMAS OBSERVADOS NO TESTE VISUAL (preencher):
- Problema observado 1: ______________________________________________
- Problema observado 2: ______________________________________________
- Problema observado 3: ______________________________________________
- Navegador usado: ______________________
- Filtro testado: ______________________
- Resultado esperado: ______________________
- Resultado observado: ______________________
- Print disponível? (sim/não): ______________________
- Arquivo HTML usado no teste: ______________________

ENTREGÁVEIS DESTA RODADA:
- Nova cópia versionada do dashboard (não sobrescrever a anterior).
- Atualizar RELATORIO_CODEX_CORRECAO_DASHBOARD.md (anexar seção "Rodada 2").
- Atualizar LOG_CODEX_DASHBOARD.md.
- Reexecutar teste_filtros_codex.py e registrar resultados.
- Validar node --check do JS extraído.
- Listar limitações e pendências remanescentes.
```

---

## Notas para você (Adinailson)
- Só envie ao Codex **depois** de rodar o `ROTEIRO_TESTE_VISUAL_USUARIO.md`.
- Se o teste visual passar sem problemas, ainda assim vale aplicar as correções 1–4 (são de redação/UX e
  de metadados, independem de bug).
- A correção 5 (distribuição filtrável) é a de maior valor analítico, mas depende de existir microdado
  monetário agregável na pasta. Se não existir, não force.
