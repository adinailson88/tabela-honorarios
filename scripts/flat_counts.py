# -*- coding: utf-8 -*-
"""Gera dados/flat_counts.json: contagens por (ano, municipio, modalidade, unidade, tipo) — TODOS os anos.
Contagens sao aditivas -> filtros cruzados ficam corretos. Dimensoes bucketizadas para tamanho controlado.
NAO altera originais."""
import os, glob, re, json, collections, datetime
import openpyxl, xlrd

FOLDER=r'C:\Users\adina\Meu Drive\ARTS Adinailson'
CSV=os.path.join(FOLDER,'ARTs 2022 01022024.csv')
OUT=os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'dados')

def norm_mod(t):
    low=(t or '').lower()
    for key,lab in [('eletric','Eng. Eletricista'),('agrôn','Eng. Agrônomo'),('agron','Eng. Agrônomo'),
        ('civil','Eng. Civil'),('seguran','Eng. Segurança Trabalho'),('mecân','Eng. Mecânico'),('mecan','Eng. Mecânico'),
        ('ambient','Eng. Ambiental'),('agrimens','Eng. Agrimensor'),('minas','Eng. de Minas'),('geólog','Geólogo'),
        ('geolog','Geólogo'),('produção','Eng. de Produção'),('producao','Eng. de Produção'),('automa','Eng. Controle/Automação'),
        ('químic','Eng. Químico'),('quimic','Eng. Químico'),('florest','Eng. Florestal'),('sanit','Eng. Sanitarista')]:
        if key in low: return lab
    return 'Outras modalidades'

def norm_uni(u):
    u=(u or '').strip().lower()
    return u if u else '(não informada)'

def year_of(s):
    if isinstance(s,datetime.datetime): return s.year
    m=re.search(r'(20\d{2})',str(s)); return int(m.group(1)) if m else None

# acumulador bruto
raw=collections.Counter()  # (ano,mun,mod,uni,tipo)->count

def add(ano,mun,mod,uni,tipo):
    if not ano: return
    raw[(str(ano),mun.upper().strip() if mun else '(N/D)',mod,norm_uni(uni),(tipo or '').strip() or '(N/D)')]+=1

# 2022 do CSV
with open(CSV,encoding='utf-8',errors='replace') as fh:
    fh.readline()
    for line in fh:
        p=line.rstrip('\n').split(';')
        while p and p[-1].strip()=='': p.pop()
        if len(p)<6: continue
        uf=p[5].strip().upper() if len(p)>5 else ''
        if uf and uf!='BA': continue
        tipo=p[1].strip() if len(p)>1 else ''
        mun=p[4] if len(p)>4 else ''
        mod=norm_mod(p[6] if len(p)>6 else '')
        uni=p[-3] if len(p)>=13 else ''
        add('2022',mun,mod,uni,tipo)

# historicos 2015-2021
def read_xlsx(fp):
    wb=openpyxl.load_workbook(fp,read_only=True,data_only=True); ws=wb.worksheets[0]
    it=ws.iter_rows(values_only=True); hdr=[str(h).strip().lower() if h else '' for h in next(it)]
    ix={h:i for i,h in enumerate(hdr)}
    for row in it:
        if not row: continue
        g=lambda k: row[ix[k]] if k in ix and ix[k]<len(row) else None
        uf=str(g('uf') or '').strip().upper()
        if uf and uf!='BA': continue
        add(year_of(g('emissao')), str(g('cidade_obra') or ''), norm_mod(str(g('titulos') or '')), str(g('unidade') or ''), str(g('tipo_art') or ''))
    wb.close()

def read_xls(fp):
    wb=xlrd.open_workbook(fp,on_demand=True); sh=wb.sheet_by_index(0)
    hdr=[str(sh.cell_value(0,c)).strip().lower() for c in range(sh.ncols)]; ix={h:i for i,h in enumerate(hdr)}
    for r in range(1,sh.nrows):
        e=sh.cell_value(r,ix.get('emissao',3))
        if not e or str(e).startswith('---'): continue
        if sh.cell_type(r,ix['emissao'])==xlrd.XL_CELL_DATE:
            try: e=datetime.datetime(*xlrd.xldate_as_tuple(e,wb.datemode))
            except: pass
        g=lambda k: sh.cell_value(r,ix[k]) if k in ix else ''
        uf=str(g('uf')).strip().upper()
        if uf and uf!='BA': continue
        add(year_of(e), str(g('cidade_obra')), norm_mod(str(g('titulos'))), str(g('unidade')), str(g('tipo_art')))  # usa 'e' convertido

for fp in sorted(glob.glob(os.path.join(FOLDER,'arts 20*'))):
    if os.path.basename(fp).lower().startswith('arts 2022'): continue
    try: (read_xls if fp.lower().endswith('.xls') else read_xlsx)(fp)
    except Exception as ex: print('ERRO',os.path.basename(fp),repr(ex))

# bucketizacao: top municipios/unidades; modalidades ja normalizadas
mun_tot=collections.Counter(); uni_tot=collections.Counter()
for (a,m,mo,u,t),c in raw.items(): mun_tot[m]+=c; uni_tot[u]+=c
TOPMUN=set([m for m,_ in mun_tot.most_common(160)])
TOPUNI=set([u for u,_ in uni_tot.most_common(12)])

agg=collections.Counter()
for (a,m,mo,u,t),c in raw.items():
    mm=m if m in TOPMUN else 'Outros municípios'
    uu=u if u in TOPUNI else 'outras unidades'
    agg[(a,mm,mo,uu,t)]+=c

anos=sorted({k[0] for k in agg}); muns=sorted({k[1] for k in agg}); mods=sorted({k[2] for k in agg})
unis=sorted({k[3] for k in agg}); tipos=sorted({k[4] for k in agg})
ia={v:i for i,v in enumerate(anos)}; im={v:i for i,v in enumerate(muns)}; imo={v:i for i,v in enumerate(mods)}
iu={v:i for i,v in enumerate(unis)}; it={v:i for i,v in enumerate(tipos)}
recs=[[ia[a],im[m],imo[mo],iu[u],it[t],c] for (a,m,mo,u,t),c in agg.items()]

out={'anos':anos,'municipios':muns,'modalidades':mods,'unidades':unis,'tipos':tipos,'recs':recs}
json.dump(out,open(os.path.join(OUT,'flat_counts.json'),'w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
sz=os.path.getsize(os.path.join(OUT,'flat_counts.json'))/1024
print('OK flat_counts | registros',len(recs),'| anos',len(anos),'mun',len(muns),'mod',len(mods),'uni',len(unis),'tipo',len(tipos),'| %.0f KB'%sz)
print('total contagens:',sum(c for *_,c in recs))

