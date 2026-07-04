# MODELO TERRITORIAL DO DASHBOARD
## Como o painel deve tratar as dimensões geográficas e a associação município → unidade CREA-BA

> Modelo conceitual para as dimensões territoriais do dashboard de honorários do SENGE/BA.
> Princípio inegociável: **toda associação município → unidade CREA deve carregar fonte e nível de
> confiabilidade**; sem isso, o campo recebe "Informação insuficiente para verificar".
> Data: 2026-06-23. Conceitual — não altera o dashboard.

---

## 1. Dimensões territoriais (modelo de dados)

Cada município da base deve ser descrito por uma linha com os campos abaixo. Os três primeiros vêm da
ART/IBGE; os demais, da associação institucional CREA-BA.

| Campo | Descrição | Origem | Estado atual |
|---|---|---|---|
| `municipio_art` | Município como aparece na ART (texto bruto) | ART (`cidade_obra`) | Disponível |
| `codigo_ibge` | Código IBGE do município (7 dígitos) | IBGE (oficial) | **Pendente** |
| `municipio_key` | Município normalizado (sem acento, maiúsculas, sem sufixo BA) | Derivado (`normalizeKey`) | Disponível |
| `unidade_crea_referencia` | Inspetoria/escritório/sede de referência | CREA-BA (Regulamento) | **Pendente** |
| `tipo_unidade` | sede · inspetoria · escritório regional · supervisão | CREA-BA | **Pendente** |
| `supervisao_regional` | Supervisão/SUREG (se existir no CREA-BA) | CREA-BA | **A verificar** |
| `fonte_associacao` | Documento/URL que sustenta a associação | Curadoria | Obrigatório |
| `confiabilidade` | alta · média · baixa | Curadoria | Obrigatório |
| `observacao` | Notas, ressalvas, divergências | Curadoria | Livre |

## 2. As nove dimensões pedidas — como o painel deve trabalhar cada uma

1. **Município da ART** — chave bruta de entrada; preservar o texto original para auditoria.
2. **Código IBGE do município** — chave estável para cruzamento cartográfico e com a malha do IBGE;
   obter da tabela oficial de 417 municípios. Hoje: *Informação insuficiente para verificar*.
3. **Município normalizado** (`municipio_key`) — usado pelos filtros e pelo casamento com a malha do mapa.
4. **Unidade CREA-BA de referência** — inspetoria/escritório/sede que jurisdiciona o município. **Só
   preencher com fonte oficial.** Hoje: *Informação insuficiente para verificar*.
5. **Tipo da unidade** — domínio fechado: `sede`, `inspetoria`, `escritório regional`, `supervisão`.
6. **Supervisão regional/SUREG** — agrupamento de inspetorias, **se existir** no CREA-BA (não confirmado).
   Tratar como camada opcional, ativada apenas após confirmação institucional.
7. **Fonte da associação** — todo vínculo município→unidade aponta para o documento que o sustenta
   (ex.: "Regulamento das Inspetorias Regionais, art. X"). Sem fonte, não há vínculo.
8. **Nível de confiabilidade** — escala explícita:
   - **alta** = norma/documento oficial do CREA-BA;
   - **média** = inferência geográfica documentada (ex.: proximidade), revisável;
   - **baixa** = não confirmada / provisória.
9. **Observação** — divergências (ex.: 24 vs. 27 inspetorias), pendências, casos de fronteira.

## 3. Regra de ouro (anti-invenção)
> Nenhuma célula de `unidade_crea_referencia`, `tipo_unidade` ou `supervisao_regional` pode ser preenchida
> por suposição. Enquanto não houver fonte oficial verificável, o valor é **"Informação insuficiente para
> verificar"** e a `confiabilidade` é **baixa**. Isto está coerente com o estado atual dos CSVs do Codex
> (`dim_municipio_crea.csv`, `dim_crea_unidades.csv`, `dim_municipios_bahia.csv`), que já adotam essa postura.

## 4. Como o painel usa essas dimensões
- **Filtro territorial em camadas:** Município → Unidade CREA → Tipo de unidade → Supervisão. Cada nível
  só fica ativo quando a coluna correspondente tiver dados confiáveis.
- **Indicador de confiabilidade visível:** ao filtrar por inspetoria/SUREG, o painel deve exibir um aviso
  quando a associação for de confiabilidade `média`/`baixa`.
- **Mapa:** casa `municipio_key`/`codigo_ibge` com a malha do IBGE; o destaque por inspetoria só deve
  aparecer quando a jurisdição estiver confirmada.
- **Degradação graciosa:** sem dados territoriais confiáveis, o painel continua funcionando por município
  (camada já disponível) e simplesmente não oferece os recortes por inspetoria/SUREG.

## 5. Roteiro de preenchimento (quando houver fonte)
1. Obter a lista oficial de 417 municípios + `codigo_ibge` (IBGE).
2. Obter a jurisdição município→inspetoria (Regulamento das Inspetorias do CREA-BA).
3. Casar por `municipio_key`; registrar `fonte_associacao` e `confiabilidade=alta`.
4. Municípios sem correspondência explícita → `baixa` + observação.
5. Revisar com o CREA-BA; só então habilitar os filtros territoriais avançados no painel.

---
*Modelo conceitual. A implementação depende de fonte oficial confirmada.*
