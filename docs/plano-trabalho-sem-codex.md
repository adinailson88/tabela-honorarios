# Plano de trabalho sem Codex

Este plano organiza o que pode ser feito diretamente com ChatGPT, GitHub e PowerShell local, sem consumir tokens do Codex.

## 1. O que pode ser feito diretamente aqui

- Criar e revisar documentação metodológica.
- Criar checklists de auditoria.
- Criar scripts-base para execução local.
- Validar estrutura de arquivos publicados.
- Validar JSON agregado público.
- Preparar comandos PowerShell para execução local.
- Preparar prompts futuros para Codex, Claude ou execução manual.

## 2. O que exige execução local

As etapas abaixo dependem das planilhas completas de ARTs no computador ou Google Drive sincronizado:

- leitura das planilhas anuais;
- deduplicação por ART;
- aplicação de TOS ao universo completo;
- classificação linha a linha da natureza do valor;
- padronização municipal com base oficial;
- análise de outliers linha a linha;
- geração de agregados anuais;
- validação de que dados individualizados não foram publicados.

## 3. Comando local recomendado

A partir da raiz do repositório:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\rodar_validacoes_locais.ps1
```

Esse comando cria relatórios locais em `relatorios/`.

## 4. Como acrescentar planilhas de outros anos

Colocar as planilhas anuais em:

```text
data/local/entrada/
```

Essa pasta é local e protegida pelo `.gitignore`. Os arquivos reais não devem ser publicados.

Depois executar:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\rodar_validacoes_locais.ps1
```

O primeiro resultado esperado é apenas inventário técnico das planilhas, não ainda o tratamento completo.

## 5. Próximas tarefas possíveis sem Codex

1. Rodar inventário local das planilhas.
2. Enviar aqui o conteúdo de `relatorios/inventario_planilhas.md`.
3. Revisar colunas disponíveis por ano.
4. Definir quais campos permitem TOS, município, valor e serviço.
5. Criar o script seguinte de ingestão anual padronizada.
6. Criar o script de auditoria anual.
7. Só depois gerar base agregada pública.

## 6. Critério de segurança

Se o arquivo contiver linha individual de ART, identificador, profissional, empresa, contratante, município por registro ou valor individual, manter local.

Publicar somente agregados.

Quando faltar evidência, registrar:

`Informação insuficiente para verificar.`
