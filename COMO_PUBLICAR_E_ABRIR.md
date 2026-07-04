# Como abrir o painel (1 clique) e publicar no Google Sites

## ✅ Abrir agora, localmente (1 clique)
Vá em `dashboard/` e dê **duplo clique em `index.html`**. Abre no navegador padrão.
- Todos os dados já estão **embutidos** no arquivo (não precisa de servidor nem dos CSVs).
- Precisa de **internet** para o mapa (OpenStreetMap) e os gráficos (Chart.js/Leaflet via CDN).

> Se algum gráfico/mapa não aparecer, é bloqueio de internet/CDN — teste em outra rede.

---

## 🌐 Publicar no Google Sites

O Google Sites **não hospeda arquivos .html** diretamente e o bloco "Incorporar > Código"
tem limite de tamanho (este painel tem ~20 KB e usa scripts externos). Há dois caminhos:

### Opção A — Hospedar e incorporar por URL (recomendado)
1. Suba a pasta `dashboard/` para um host estático. Mais simples: **GitHub Pages**
   (você já usa no projeto Malha IA) ou Google Drive→site, Netlify, etc.
2. Pegue a URL pública do `index.html` (ex.: `https://SEU_USUARIO.github.io/painel/index.html`).
3. No Google Sites: **Inserir → Incorporar → Por URL** → cole o link → Inserir.
4. Redimensione o bloco (recomendo largura total e altura ~1600 px).

### Opção B — Incorporar o código (provavelmente NÃO cabe)
O `index.html` agora tem ~770 KB (dados de 8 anos + IBGE embutidos), acima do limite do bloco
"Código incorporado" do Google Sites. **Prefira a Opção A (por URL).** A Opção B só serve para
versões muito enxutas do painel.

### Dica de GitHub Pages (rápido)
```
# dentro de um repositório novo (ex.: painel-honorarios)
# copie a pasta dashboard/ para a raiz do repo e ative Pages (branch main, /root)
# a URL fica: https://SEU_USUARIO.github.io/painel-honorarios/
```

---

## Atualizar o painel quando houver novos dados
```
python scripts/agrega_arts.py        # recalcula agregados (não altera o CSV original)
python scripts/calibra_atividade.py  # recalcula faixas por atividade x unidade
python scripts/gera_dashboard.py     # reconstrói dashboard/index.html
python scripts/gera_planilha.py      # reconstrói PLANILHA_MODELO_HONORARIOS.xlsx
```
