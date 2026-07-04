# -*- coding: utf-8 -*-
"""
Agrega a base de ARTs 2022 (CSV ~146MB) em tabelas SOMENTE agregadas (LGPD).
- Parsing robusto: o campo 'atividade' tem ';' interno -> ancora colunas pela direita.
- Metricas: contagem, mediana, IQR (P25/P75). Suprime celulas com n<5.
- Winsorizacao leve para mediana: descarta valor<=0 e valor>1e9 (implausivel).
NAO altera o arquivo original. Saida apenas em PROPOSTA CLAUDE/dados.
"""
import csv, os, math, json, collections, datetime

SRC = r'C:\Users\adina\Meu Drive\ARTS Adinailson\ARTs 2022 01022024.csv'
OUT = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'dados')
MIN_N = 5
VAL_MAX = 1e9  # acima disso = implausivel/erro de digitacao

def norm_modalidade(t):
    t = (t or '').strip()
    if not t: return 'Não informado'
    # remove genero
    t = t.replace('Engenheira', 'Engenheiro').replace('Engenheiro(a)', 'Engenheiro')
    t = t.replace('Arquiteta', 'Arquiteto').replace('Técnica', 'Técnico')
    # agrupamentos amplos
    low = t.lower()
    if 'eletric' in low: return 'Engenheiro Eletricista'
    if 'agrôn' in low or 'agron' in low: return 'Engenheiro Agrônomo'
    if 'civil' in low: return 'Engenheiro Civil'
    if 'segurança' in low or 'seguranca' in low: return 'Engenheiro de Segurança do Trabalho'
    if 'mecân' in low or 'mecan' in low: return 'Engenheiro Mecânico'
    if 'ambient' in low: return 'Engenheiro Ambiental'
    if 'agrimens' in low: return 'Engenheiro Agrimensor'
    if 'minas' in low: return 'Engenheiro de Minas'
    if 'geólog' in low or 'geolog' in low: return 'Geólogo'
    if 'produção' in low or 'producao' in low: return 'Engenheiro de Produção'
    if 'automa' in low or 'controle' in low: return 'Eng. de Controle e Automação'
    if 'químic' in low or 'quimic' in low: return 'Engenheiro Químico'
    if 'sanit' in low: return 'Engenheiro Sanitarista'
    if 'florest' in low: return 'Engenheiro Florestal'
    if 'pesca' in low or 'aquic' in low: return 'Engenheiro de Pesca/Aquicultura'
    return t

def pct(a, p):
    if not a: return None
    a = sorted(a); k = (len(a)-1)*p; f = math.floor(k); c = math.ceil(k)
    return a[f] if f == c else a[f]+(a[c]-a[f])*(k-f)

# acumuladores
mun_vals = collections.defaultdict(list); mun_n = collections.Counter()
mod_vals = collections.defaultdict(list); mod_n = collections.Counter()
uni_vals = collections.defaultdict(list); uni_n = collections.Counter()
tipo_n = collections.Counter()
ativ_n = collections.Counter()
all_vals = []
n_total = 0; n_complete = 0; ids = set()

with open(SRC, encoding='utf-8', errors='replace') as fh:
    fh.readline()
    for line in fh:
        parts = line.rstrip('\n').split(';')
        while parts and parts[-1].strip() == '': parts.pop()
        if not parts: continue
        n_total += 1
        ids.add(parts[0])
        tipo = parts[1].strip() if len(parts) > 1 else ''
        mun  = parts[4].strip().upper() if len(parts) > 4 else ''
        uf   = parts[5].strip().upper() if len(parts) > 5 else ''
        mod  = norm_modalidade(parts[6]) if len(parts) > 6 else 'Não informado'
        if tipo: tipo_n[tipo] += 1
        # so BA para agregados geograficos/valor
        if uf and uf != 'BA':
            continue
        if mun: mun_n[mun] += 1
        mod_n[mod] += 1
        if len(parts) >= 13:
            n_complete += 1
            valor = parts[-2]; unid = parts[-3].strip().lower()
            ativ = ' '.join(parts[9:len(parts)-4]).strip()
            if unid: uni_n[unid] += 1
            if ativ: ativ_n[ativ[:70]] += 1
            try:
                v = float(valor.replace(',', '.'))
            except:
                v = None
            if v is not None and 0 < v <= VAL_MAX:
                all_vals.append(v)
                if mun: mun_vals[mun].append(v)
                mod_vals[mod].append(v)
                if unid: uni_vals[unid].append(v)

def write_group(fname, counter, vals, keyname, topn=None):
    rows = []
    for k, n in counter.most_common():
        vs = vals.get(k, [])
        if len(vs) >= MIN_N:
            med = round(pct(vs, .5), 2); p25 = round(pct(vs, .25), 2); p75 = round(pct(vs, .75), 2); nv = len(vs)
        else:
            med = p25 = p75 = ''; nv = len(vs)
        rows.append([k, n, nv, med, p25, p75])
    if topn: rows = rows[:topn]
    with open(os.path.join(OUT, fname), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f); w.writerow([keyname, 'n_registros', 'n_valores', 'mediana_valor', 'p25_valor', 'p75_valor']); w.writerows(rows)
    return rows

mun_rows = write_group('por_municipio.csv', mun_n, mun_vals, 'municipio')
mod_rows = write_group('por_modalidade.csv', mod_n, mod_vals, 'modalidade')
uni_rows = write_group('por_unidade.csv', uni_n, uni_vals, 'unidade', topn=30)

with open(os.path.join(OUT, 'por_tipo_art.csv'), 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f); w.writerow(['tipo_art', 'n_registros']); w.writerows(tipo_n.most_common())

with open(os.path.join(OUT, 'top_atividades.csv'), 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f); w.writerow(['atividade_texto_trunc70', 'n_registros']); w.writerows(ativ_n.most_common(40))

faixas = [['estatistica', 'valor_R$']]
for lbl, p in [('min', 0), ('p10', .1), ('p25', .25), ('mediana', .5), ('p75', .75), ('p90', .9), ('p99', .99), ('max', 1)]:
    faixas.append([lbl, round(pct(all_vals, p), 2)])
with open(os.path.join(OUT, 'faixas_valor.csv'), 'w', newline='', encoding='utf-8-sig') as f:
    csv.writer(f).writerows(faixas)

# JSON para o dashboard (apenas agregados)
def med(vs): return round(pct(vs, .5), 2) if len(vs) >= MIN_N else None
data = {
    'gerado_em': datetime.date.today().isoformat(),
    'fonte': 'ARTs CREA-BA 2022 (ARTs 2022 01022024.csv)',
    'totais': {'linhas_atividade': n_total, 'arts_distintas': len(ids), 'linhas_completas': n_complete, 'valores_validos': len(all_vals)},
    'faixas': {k: v for k, v in faixas[1:]},
    'municipios': [{'nome': k, 'n': n, 'mediana': med(mun_vals.get(k, []))} for k, n in mun_n.most_common(60)],
    'modalidades': [{'nome': k, 'n': n, 'mediana': med(mod_vals.get(k, []))} for k, n in mod_n.most_common(15)],
    'unidades': [{'nome': k, 'n': n, 'mediana': med(uni_vals.get(k, []))} for k, n in uni_n.most_common(12)],
    'tipos': [{'nome': k, 'n': n} for k, n in tipo_n.most_common(8)],
}
with open(os.path.join(OUT, 'data.json'), 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=1)

print('OK. linhas=%d arts=%d valores=%d municipios=%d modalidades=%d' % (n_total, len(ids), len(all_vals), len(mun_n), len(mod_n)))
print('mediana geral R$', med(all_vals))

