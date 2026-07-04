# Especificação de padronização municipal

**Frente:** SENGE-BA — Nova metodologia de tabela de honorários
**Data:** 2026-06-24
**Natureza:** especificação técnica. Não implementa, não roda pipeline.

> Convenção: **[FATO VERIFICADO]**, **[INFERÊNCIA TÉCNICA]**, **[RECOMENDAÇÃO]**.
> Onde não há base local: **"Informação insuficiente para verificar"**.

---

## 1. Situação atual

**[FATO VERIFICADO]**
- O campo `cidade_obra` tem **1.984 grafias distintas**.
- O pipeline já normaliza parcialmente: `norm_key()` em `gerar_metodologia_servicos.py` remove acentos, faz upper-case, colapsa espaços e remove sufixo `-BA`/`/BA`. O resultado é gravado como `municipio_key`.
- Já existem dimensões municipais: `dim_municipios_bahia.csv` (`codigo_ibge`, `municipio_label`, `municipio_key`, `uf`) e `dim_municipio_crea.csv` — porém com `codigo_ibge` = **"Informação insuficiente para verificar"** e jurisdição CREA também não preenchida.

**[INFERÊNCIA TÉCNICA]** Há um esqueleto de padronização, mas **sem chave IBGE validada** e sem lista oficial de municípios como referência de validação. As 1.984 grafias provavelmente colapsam para muito menos municípios reais (a Bahia tem 417 municípios — **número a confirmar contra fonte IBGE oficial**, hoje "Informação insuficiente para verificar" nos arquivos locais).

---

## 2. Campos alvo

**[RECOMENDAÇÃO]** Padronizar para 4 campos por registro:

| Campo | Conteúdo | Regra |
|---|---|---|
| `municipio_original` | grafia bruta de `cidade_obra` | preservada para auditoria |
| `municipio_key` | chave normalizada | upper, sem acento, sem UF, espaços colapsados (regra já existente em `norm_key`) |
| `municipio_label` | nome oficial do município | obtido da lista IBGE oficial após match |
| `codigo_ibge` | código IBGE de 7 dígitos | da lista IBGE oficial; se não validado → "Informação insuficiente para verificar" |

---

## 3. Tratamento de acentos

**[FATO VERIFICADO]** `strip_accents()` (NFD + remoção de marcas) já está implementado.
**[RECOMENDAÇÃO]** Reusar a mesma função para garantir que `municipio_key` da base e da lista IBGE usem a **mesma normalização** — match só é confiável se os dois lados forem normalizados pela mesma regra.

## 4. Tratamento de abreviações

**[INFERÊNCIA TÉCNICA]** Grafias como "STO ANT DE JESUS", "S.A. DE JESUS", "STA CRUZ CABRALIA" são fonte de duplicação.
**[RECOMENDAÇÃO]**
- Manter um **dicionário de expansão de abreviações** explícito e auditável (`STO`→`SANTO`, `STA`→`SANTA`, `S.`→`SAO`, `N. SRA`→`NOSSA SENHORA`, etc.).
- Aplicar a expansão **antes** do match contra a lista IBGE.
- **Não inventar** município ao expandir: se a expansão não casar com a lista IBGE, marcar como não identificado (item 8), não forçar.

## 5. Remoção de UF

**[FATO VERIFICADO]** A regra atual já remove sufixo `-BA`/`/BA` no fim da string.
**[RECOMENDAÇÃO]** Ampliar para remover `" BA"`, `"(BA)"`, `"- BAHIA"` e variantes, sempre **só como sufixo de UF**, nunca no miolo do nome (evitar mutilar nomes que contenham "BA").

## 6. Validação contra lista IBGE

**[FATO VERIFICADO]** Não há lista IBGE oficial validada na pasta (codigo_ibge = "Informação insuficiente para verificar").
**[RECOMENDAÇÃO]**
1. Obter/receber a **lista oficial de municípios da Bahia (IBGE)** com código de 7 dígitos.
2. Match em 2 etapas:
   - **exato**: `municipio_key` (após expansão) == `municipio_key` da lista IBGE → confiança alta.
   - **aproximado**: similaridade de string (ex.: distância de edição) acima de limiar → **proposta** de match para revisão humana, nunca aplicada automaticamente como verdade.
3. Registrar `nivel_confianca_municipio` = exato / aproximado / nao_identificado.
4. Enquanto a lista oficial não existir: `codigo_ibge` permanece "Informação insuficiente para verificar".

## 7. Agregação por município

**[RECOMENDAÇÃO]** Agregar **por `codigo_ibge`** quando validado; na ausência, por `municipio_key`. Toda agregação territorial deve respeitar as mesmas regras de cautela monetária (só Classe A para valor; gate C/D; `n < 5` por município-serviço).

**[INFERÊNCIA TÉCNICA]** Recortes município×serviço fragmentam muito a amostra — a maioria das células município×serviço cairá em `n < 5`. Por isso, no recorte territorial, priorizar **frequência/demanda** e suprimir valor por padrão, exceto onde `n ≥ 5`.

## 8. Marcação de município não identificado

**[RECOMENDAÇÃO]** Quando não houver match validado:
- `municipio_label` = "Informação insuficiente para verificar";
- `codigo_ibge` = "Informação insuficiente para verificar";
- `nivel_confianca_municipio` = `nao_identificado`;
- manter `municipio_original` e `municipio_key` para reprocessamento futuro.
Nunca atribuir um município "mais provável" sem evidência.

## 9. Futura agregação por inspetoria / SUREG

**[FATO VERIFICADO]** `dim_municipio_crea.csv` e `dim_crea_unidades.csv` têm jurisdição (inspetoria, supervisão regional, SUREG) **toda** em "Informação insuficiente para verificar" — a pasta local não contém fonte segura município→inspetoria.

**[RECOMENDAÇÃO]**
- **Não criar jurisdição agora.** Recorte por inspetoria/SUREG só após obter a fonte oficial CREA-BA que mapeie município→unidade.
- Quando a fonte existir, o de-para será `codigo_ibge` → `unidade_crea` → `supervisao_regional/SUREG`, com `confiabilidade` e `fonte` registradas em cada linha.
- Até lá, qualquer mapa por inspetoria seria **invenção de jurisdição** — proibido pelas regras da frente.

---

## 10. Sequência recomendada (sem rodar nada agora)
1. Reusar `norm_key`/`strip_accents` existentes (não reinventar).
2. Construir dicionário de abreviações auditável.
3. Obter lista IBGE oficial → preencher `codigo_ibge`/`municipio_label`.
4. Marcar confiança; suprimir valor em células esparsas (`n < 5`).
5. SUREG/inspetoria **só** com fonte oficial CREA.

---

## Síntese
A padronização municipal já tem normalização de chave, mas falta a **âncora IBGE oficial**. O caminho é: expandir abreviações → casar contra lista IBGE → marcar confiança → suprimir valor onde a amostra é esparsa. Jurisdição CREA (inspetoria/SUREG) fica para uma segunda etapa, condicionada a fonte oficial — não pode ser inventada.
