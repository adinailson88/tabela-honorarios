# -*- coding: utf-8 -*-
"""Constroi serie temporal anual (n, mediana, P25, P75 do valor) a partir das bases por semestre
2015-2021 (.xls/.xlsx) + 2022 do CSV consolidado. Robusto a formatos de valor.
NAO altera originais. Atualiza dados/serie_temporal.csv e injeta 'serie' em dados/data.json.
RESSALVA: arquivos .xls tem teto de 65.536 linhas -> 2015-2019 podem estar truncados (n e' minimo)."""
import os, glob, re, math, json, csv, collections, datetime
import openpyxl, xlrd

FOLDER=r'C:\Users\adina\Meu Drive\ARTS Adinailson'
OUT=os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'dados')
VAL_MAX=1e9

def parse_val(s):
    if s is None: return None
    if isinstance(s,(int,float)):
        v=float(s); return v if 0<v<=VAL_MAX else None
    t=str(s).strip().replace('R$','').replace(' ','')
    if not t: return None
    t=re.sub(r'[^0-9,.\-]','',t)
    if ',' in t and '.' in t:
        if t.rfind(',')>t.rfind('.'): t=t.replace('.','').replace(',','.')
        else: t=t.replace(',','')
    elif ',' in t:
        # virgula decimal se 1-2 digitos apos a ultima virgula
        if len(t)-t.rfind(',')-1 in (1,2): t=t.replace('.','')  # nao ha pontos aqui
        t=t.replace(',','.') if t.count(',')==1 else t.replace(',','',t.count(',')-1).replace(',','.')
    try:
        v=float(t); return v if 0<v<=VAL_MAX else None
    except: return None

def year_of(s):
    if isinstance(s,datetime.datetime): return s.year
    t=str(s).strip()
    m=re.search(r'(20\d{2})',t)
    return int(m.group(1)) if m else None

vals=collections.defaultdict(list)

def feed(year,val):
    v=parse_val(val)
    if v is not None and year: vals[year].append(v)

def read_xlsx(fp):
    wb=openpyxl.load_workbook(fp,read_only=True,data_only=True); ws=wb.worksheets[0]
    it=ws.iter_rows(values_only=True); hdr=next(it)
    idx={str(h).strip().lower():i for i,h in enumerate(hdr) if h}
    ie=idx.get('emissao'); iv=idx.get('valor_contrato')
    if ie is None or iv is None: wb.close(); return
    for row in it:
        if not row or len(row)<=max(ie,iv): continue
        feed(year_of(row[ie]), row[iv])
    wb.close()

def read_xls(fp):
    wb=xlrd.open_workbook(fp,on_demand=True); sh=wb.sheet_by_index(0)
    hdr=[str(sh.cell_value(0,c)).strip().lower() for c in range(sh.ncols)]
    idx={h:i for i,h in enumerate(hdr)}
    ie=idx.get('emissao'); iv=idx.get('valor_contrato')
    if ie is None or iv is None: return
    for r in range(1,sh.nrows):
        e=sh.cell_value(r,ie)
        if not e or str(e).startswith('---'): continue
        # datas .xls podem ser numero serial
        ct=sh.cell_type(r,ie)
        if ct==xlrd.XL_CELL_DATE:
            try: e=datetime.datetime(*xlrd.xldate_as_tuple(e,wb.datemode))
            except: pass
        feed(year_of(e), sh.cell_value(r,iv))

for fp in sorted(glob.glob(os.path.join(FOLDER,'arts 20*'))):
    fn=os.path.basename(fp)
    if fn.startswith('arts 2022'): continue  # 2022 vem do CSV consolidado
    try:
        (read_xls if fp.lower().endswith('.xls') else read_xlsx)(fp)
        print('lido', fn, '| acum anos', {k:len(v) for k,v in sorted(vals.items())})
    except Exception as ex:
        print('ERRO', fn, repr(ex))

def pct(a,p):
    a=sorted(a); k=(len(a)-1)*p; f=math.floor(k); c=math.ceil(k)
    return a[f] if f==c else a[f]+(a[c]-a[f])*(k-f)

# 2022 do CSV consolidado (ja agregado em data.json)
data=json.load(open(os.path.join(OUT,'data.json'),encoding='utf-8'))
serie=[]
for y in sorted(vals):
    vs=vals[y]
    if len(vs)<30: continue
    serie.append({'ano':y,'n':len(vs),'mediana':round(pct(vs,.5),2),'p25':round(pct(vs,.25),2),'p75':round(pct(vs,.75),2)})
serie.append({'ano':2022,'n':data['totais']['valores_validos'],'mediana':data['faixas']['mediana'],
              'p25':data['faixas']['p25'],'p75':data['faixas']['p75']})
serie.sort(key=lambda r:r['ano'])

with open(os.path.join(OUT,'serie_temporal.csv'),'w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f); w.writerow(['ano','n_valores','mediana_R$','p25_R$','p75_R$'])
    for r in serie: w.writerow([r['ano'],r['n'],r['mediana'],r['p25'],r['p75']])

data['serie']=serie
json.dump(data,open(os.path.join(OUT,'data.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('SERIE:'); [print('  ',r['ano'],'| n',r['n'],'| mediana R$',r['mediana']) for r in serie]

