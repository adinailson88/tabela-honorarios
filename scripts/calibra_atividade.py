# -*- coding: utf-8 -*-
"""A3/B2 — Calibracao de faixas por Atividade x Unidade (homogenea), COM PODA DE OUTLIERS.
- Extrai Nivel e Atividade-categoria do texto da ART (~ nomes da tabela TOS).
- Apara TRIM em cada cauda (default 20%) antes de calcular faixa -> remove valores extremos.
  Faixa = piso (P_TRIM) / referencia (mediana aparada) / teto (P_{1-TRIM}).
- Marca como NAO PRECIFICAVEL combinacoes sem unidade ('(nao informada)'/vazio).
- Suprime celulas com n<5 (LGPD/robustez).
Saidas: dados/calibracao_atividade_unidade.csv (todas precificaveis) +
        dados/atividades_nao_precificaveis.csv + injeta em data.json (calibracao, calibracao_full, nao_precificavel).
NAO altera o arquivo original.

Para usar poda de 30% nas caudas, altere TRIM=0.30.
"""
import csv, os, re, math, json, collections

SRC=r'C:\Users\adina\Meu Drive\ARTS Adinailson\ARTs 2022 01022024.csv'
OUT=os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'dados')
MIN_N=5; VAL_MAX=1e9
TRIM=0.20  # remove 20% maiores e 20% menores antes de calcular faixa

SEM_UNIDADE={'', '(nao informada)', '(não informada)', 'nao informada', 'não informada', 'n/d', '(n/d)'}

reN=re.compile(r'Nivel\s*-\s*([^;]+?)\s*(?:Atividade|$)')
reA=re.compile(r'Atividade\s*-\s*([^-]+?)\s*-')

def norm(s): return re.sub(r'\s+',' ',s.strip())
def disp(s): return s if (s.isupper() and len(s)<=14) else s.capitalize()

def pct(a,p):
    a=sorted(a); k=(len(a)-1)*p; f=math.floor(k); c=math.ceil(k)
    return a[f] if f==c else a[f]+(a[c]-a[f])*(k-f)

def stats_aparadas(vs):
    """Retorna (n, n_core, piso, mediana, teto) apos remover TRIM em cada cauda."""
    s=sorted(vs); nn=len(s)
    lo=math.floor(nn*TRIM); hi=nn-lo
    core=s[lo:hi] if hi>lo else s
    if not core: core=s
    mid=core[len(core)//2] if len(core)%2 else (core[len(core)//2-1]+core[len(core)//2])/2
    return nn, len(core), round(core[0],2), round(mid,2), round(core[-1],2)

vals=collections.defaultdict(list)          # (ativ_cf, unidade) -> [valores]
disp_name={}; niv_of=collections.defaultdict(collections.Counter)
ativ_sem_unidade=collections.Counter()      # atividade -> contagem de registros sem unidade
ativ_total=collections.Counter()
n_usados=0
# precificabilidade por tipo de ART (todos os registros)
tipo_total=collections.Counter(); tipo_precif=collections.Counter()

with open(SRC,encoding='utf-8',errors='replace') as fh:
    fh.readline()
    for line in fh:
        parts=line.rstrip('\n').split(';')
        while parts and parts[-1].strip()=='': parts.pop()
        uf=parts[5].strip().upper() if len(parts)>5 else ''
        if uf and uf!='BA': continue
        tipo_art=(parts[1].strip() if len(parts)>1 else '') or '(N/D)'
        tipo_total[tipo_art]+=1
        # precificavel = tem unidade valida E valor numerico
        precif=False
        if len(parts)>=13:
            u=parts[-3].strip().lower(); vtxt=parts[-2]
            if u not in SEM_UNIDADE:
                try:
                    vv=float(vtxt.replace(',','.')); precif = 0<vv<=VAL_MAX
                except: precif=False
        if precif: tipo_precif[tipo_art]+=1
        if len(parts)<13: continue
        ativ=' '.join(parts[9:len(parts)-4]).strip()
        unid=parts[-3].strip().lower(); valor=parts[-2]
        mA=reA.search(ativ); mN=reN.search(ativ)
        if not mA: continue
        cat=norm(mA.group(1)); ativ_total[cat.casefold()]+=1
        if unid in SEM_UNIDADE:
            ativ_sem_unidade[cat.casefold()]+=1
            disp_name.setdefault((cat.casefold(),'__semunidade__'),(disp(cat),'(sem unidade)'))
            continue
        key=(cat.casefold(), unid)
        disp_name.setdefault(key,(disp(cat),unid))
        if mN: niv_of[key][norm(mN.group(1))]+=1
        try: v=float(valor.replace(',','.'))
        except: continue
        if 0<v<=VAL_MAX:
            vals[key].append(v); n_usados+=1

# faixas precificaveis (aparadas)
rows=[]
for key,vs in vals.items():
    if len(vs)<MIN_N: continue
    cat,unid=disp_name[key]
    nn,ncore,piso,med,teto=stats_aparadas(vs)
    nivel=niv_of[key].most_common(1)[0][0] if niv_of[key] else ''
    ratio=(teto/med) if med>0 else 999
    conf='Alta' if (nn>=50 and ratio<=6) else ('Baixa (provável mistura valor unitário/total)' if ratio>20 else 'Média')
    rows.append([cat,unid,nivel,nn,ncore,piso,med,teto,conf])
rows.sort(key=lambda r:-r[3])

with open(os.path.join(OUT,'calibracao_atividade_unidade.csv'),'w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f)
    w.writerow(['atividade','unidade','nivel_predominante','n_total','n_apos_poda',
                f'piso_P{int(TRIM*100)}_R$','referencia_mediana_R$',f'teto_P{int(100-TRIM*100)}_R$','confiabilidade'])
    w.writerows(rows)

# atividades nao precificaveis (sem unidade na maioria dos registros)
nao=[]
for cf,semu in ativ_sem_unidade.most_common():
    tot=ativ_total[cf]; frac=semu/tot if tot else 0
    nome=disp_name.get((cf,'__semunidade__'),(cf,''))[0]
    nao.append([nome,semu,tot,round(frac*100,1)])
nao.sort(key=lambda r:-r[1])
with open(os.path.join(OUT,'atividades_nao_precificaveis.csv'),'w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f); w.writerow(['atividade','registros_sem_unidade','registros_total','pct_sem_unidade'])
    w.writerows(nao)

# precificabilidade por tipo de ART
prec=[]
for t,tot in tipo_total.most_common():
    p=tipo_precif[t]; prec.append([t,tot,p,tot-p,round(p/tot*100,1) if tot else 0])
with open(os.path.join(OUT,'precificabilidade_por_tipo.csv'),'w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f); w.writerow(['tipo_art','total','precificaveis','nao_precificaveis','pct_precificavel'])
    w.writerows(prec)

# injeta em data.json
data=json.load(open(os.path.join(OUT,'data.json'),encoding='utf-8'))
data['trim_pct']=int(TRIM*100)
data['precificabilidade']=[{'tipo':r[0],'total':r[1],'precif':r[2],'naoprecif':r[3],'pct':r[4]} for r in prec]
data['calibracao']=[{'rotulo':f'{r[0]} ({r[1]})','atividade':r[0],'unidade':r[1],'n':r[3],
                     'piso':r[5],'mediana':r[6],'teto':r[7],'conf':r[8]} for r in rows if r[3]>=50][:22]
# full para o seletor de atividade (todas precificaveis n>=5)
data['calibracao_full']=[{'atividade':r[0],'unidade':r[1],'nivel':r[2],'n':r[3],
                          'piso':r[5],'mediana':r[6],'teto':r[7],'conf':r[8]} for r in rows]
data['nao_precificavel']=[{'atividade':r[0],'sem_unidade':r[1],'total':r[2],'pct':r[3]} for r in nao[:40]]
json.dump(data,open(os.path.join(OUT,'data.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)

print(f'OK calibracao (poda {int(TRIM*100)}%/cauda) | combos precificaveis n>=5: {len(rows)} | valores usados: {n_usados}')
print(f'atividades com registros SEM unidade: {len(nao)} (top: {[x[0] for x in nao[:5]]})')
print('precificabilidade por tipo:'); [print(f'  {r[0]}: {r[4]}% precificavel ({r[2]}/{r[1]})') for r in prec]
print('exemplos (piso/ref/teto aparados):')
for r in rows[:8]: print(f'  {r[0]} | {r[1]} | n {r[3]} | {r[5]} / {r[6]} / {r[7]}')

