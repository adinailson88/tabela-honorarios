# -*- coding: utf-8 -*-
"""
Pipeline metodologia por servico + classe de confiabilidade (SENGE/BA).
Le ARTs 2022, classifica A/B/C/D no nivel da ART (deduplicando valor),
mapeia atividade->servico, e gera CSVs agregados + dashboard HTML.
Nao soma valor de linhas da mesma ART. Nao expoe dados pessoais. Nao faz ranking.
"""
from __future__ import annotations
import csv, json, re, unicodedata, statistics, datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
ART_CSV = Path(r"C:\Users\adina\Meu Drive\ARTS Adinailson\ARTs 2022 01022024.csv")
PLAUS_MAX = 1_000_000_000.0  # descartar valores implausiveis (> R$ 1 bilhao)

def strip_accents(s: str) -> str:
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

def norm_key(s: str) -> str:
    s = strip_accents("" if s is None else str(s)).upper()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s*[-/]\s*BA$", "", s)
    return s.strip()

# ---- Mapeamento atividade -> (servico_padronizado, grupo_servico) ----
# INFERENCIA por palavra-chave (ordem importa: especifico antes de generico).
SVC_RULES = [
    (("RECEITUARIO",), "Receituario Agronomico", "Servico novo - Agronomia"),
    (("FOTOVOLTAIC", "MICROGERA", "GERACAO DE ENERGIA", "GERACAO DISTRIBUIDA", " SOLAR"),
        "Microgeracao / Fotovoltaica", "Servico novo - Energia"),
    (("ALVENARIA",), "Edificacao em Alvenaria", "Projetos Civis"),
    (("CONCRETO", "ESTRUTURA"), "Estrutura / Calculo Estrutural", "Calculo Estrutural"),
    (("BAIXA TENSAO", "INST.ELETR", "INSTALACAO ELETR", "INSTALACOES ELETR", "ELETR"),
        "Instalacoes Eletricas", "Instalacoes Eletricas e de Comunicacao"),
    (("HIDRO-SAN", "HIDROSSAN", "HIDRO SAN", "REDE HIDRO", "SANITARI", "ESGOTO", "DRENAGEM", "AGUA"),
        "Rede Hidrossanitaria / Saneamento", "Saneamento e Instalacoes Hidraulicas"),
    (("PAVIMENTA", "ESTRADA", "RODOVI"), "Pavimentacao / Estradas", "Estradas e Ruas"),
    (("TOPOGRAF", "GEORREF", "AGRIMENS"), "Topografia / Agrimensura", "Servico novo - Agrimensura"),
    (("AR CONDICIONADO", "CLIMATIZ", "VENTILA", "REFRIGERA"), "Climatizacao / Ventilacao", "Instalacoes Mecanicas"),
    (("INCENDIO",), "Prevencao de Incendio", "Instalacoes"),
    (("AMBIENT", "LICENCIAMENTO"), "Meio Ambiente / Licenciamento", "Servico novo - Ambiental"),
    (("SEGURANCA",), "Seguranca do Trabalho", "Servico novo - Seguranca"),
    (("LAUDO",), "Laudo Tecnico", "Pericias e Laudos"),
    (("VISTORIA", "PERICIA", "AVALIACAO"), "Vistoria / Pericia", "Pericias e Laudos"),
    (("DESEMPENHO DE CARGO", "CARGO TECNICO", "CARGO/FUNCAO", "CARGO-FUNCAO"),
        "Desempenho de Cargo / Funcao", "Cargo-Funcao"),
    (("CONSULTORIA", "ASSISTENCIA TECNICA"), "Consultoria Tecnica", "Consultoria"),
]
NAO_MAPEADO = ("Nao mapeado", "Informacao insuficiente para verificar")

def map_servico(atividade_norm: str, tipo_norm: str):
    if "RECEITUARIO" in tipo_norm:
        return "Receituario Agronomico", "Servico novo - Agronomia"
    if "CARGO" in tipo_norm:
        return "Desempenho de Cargo / Funcao", "Cargo-Funcao"
    for kws, svc, grp in SVC_RULES:
        for kw in kws:
            if kw in atividade_norm:
                return svc, grp
    return NAO_MAPEADO

# ---- Parse ART CSV, agregando por id ----
# id -> dict
def parse():
    arts = {}
    with open(ART_CSV, "r", encoding="utf-8", errors="replace") as fh:
        fh.readline()  # header
        for line in fh:
            line = line.rstrip("\n").rstrip("\r")
            if not line:
                continue
            parts = line.split(";")
            while parts and parts[-1] == "":
                parts.pop()
            if len(parts) < 5:
                continue
            _id = parts[0]
            tipo = parts[1] if len(parts) > 1 else ""
            emissao = parts[3] if len(parts) > 3 else ""
            cidade = parts[4] if len(parts) > 4 else ""
            titulos = parts[6] if len(parts) > 6 else ""
            if len(parts) >= 14:
                codigo = parts[8]
                atividade = ";".join(parts[9:-4])
                valor_raw = parts[-2]
            else:
                codigo = ""
                atividade = ""
                valor_raw = ""
            # ano da emissao (dd/mm/aaaa ...)
            ano = ""
            m = re.search(r"/(\d{4})", emissao)
            if m:
                ano = m.group(1)
            try:
                v = round(float(valor_raw), 2) if valor_raw != "" else None
            except Exception:
                v = None
            svc, grp = map_servico(norm_key(atividade), norm_key(tipo))
            a = arts.get(_id)
            if a is None:
                arts[_id] = {
                    "n": 1, "val": v, "vary": 0,
                    "cods": ({codigo} if codigo else set()),
                    "svcs": {(svc, grp)},
                    "cidade": cidade, "ano": ano, "tipo": tipo, "titulo": titulos,
                }
            else:
                a["n"] += 1
                if v is not None:
                    if a["val"] is None:
                        a["val"] = v
                    elif abs((a["val"] or 0) - v) > 0.005:
                        a["vary"] = 1
                if codigo:
                    a["cods"].add(codigo)
                a["svcs"].add((svc, grp))
                if not a["ano"] and ano:
                    a["ano"] = ano
                if not a["titulo"] and titulos:
                    a["titulo"] = titulos
    return arts

def classify(a):
    n = a["n"]; v = a["val"]; vary = a["vary"]; ncods = max(1, len(a["cods"]))
    has_val = v is not None and v > 0
    plausible = has_val and v < PLAUS_MAX
    if not plausible:
        motivo = "valor ausente/zerado" if not has_val else "valor implausivel (> R$ 1 bilhao)"
        return "D", motivo
    if n == 1:
        return "A", ""
    if ncods <= 1 and vary == 0:
        return "B", "composto homogeneo (mesmo codigo, valor unico)"
    if ncods > 1 or vary == 1:
        return "C", "composto ambiguo (multiplas atividades/valor unico replicado)"
    return "C", "composto"

def quantiles(vals):
    vals = sorted(vals)
    n = len(vals)
    def pct(p):
        if n == 0: return None
        k = (n - 1) * p; f = int(k); c = min(f + 1, n - 1)
        return vals[f] + (vals[c] - vals[f]) * (k - f)
    return pct(0.5), pct(0.25), pct(0.75), vals[0], vals[-1]

def main():
    print("Lendo ARTs...")
    arts = parse()
    print(f"ARTs distintas: {len(arts)}")

    # representante servico por ART
    def rep_service(a):
        if len(a["svcs"]) == 1:
            return next(iter(a["svcs"]))
        # composto: escolher servico nao-'Nao mapeado' se houver um unico mapeado
        mapped = [s for s in a["svcs"] if s[0] != "Nao mapeado"]
        if len(set(mapped)) == 1:
            return mapped[0]
        return ("Composto (multiplos servicos)", "Composto")

    base_rows = []
    classe_count = {"A": 0, "B": 0, "C": 0, "D": 0}
    for _id, a in arts.items():
        classe, motivo = classify(a)
        classe_count[classe] += 1
        svc, grp = rep_service(a)
        usar = "sim" if classe == "A" else ("secundario" if classe == "B" else "nao")
        if classe in ("C", "D"):
            mot_excl = motivo if motivo else ("classe C" if classe == "C" else "classe D")
        elif classe == "B":
            mot_excl = "uso secundario (composto homogeneo)"
        else:
            mot_excl = ""
        valor_replicado = 1 if (a["n"] > 1 and a["vary"] == 0 and a["val"] is not None) else 0
        base_rows.append({
            "id_art": _id, "ano": a["ano"] or "Informacao insuficiente para verificar",
            "municipio": a["cidade"], "municipio_key": norm_key(a["cidade"]),
            "atividade_original": "Informacao insuficiente para verificar",  # nao expor texto livre detalhado
            "atividade_key": svc,  # servico mapeado serve de chave de atividade padronizada
            "codigo_atividade": ";".join(sorted(a["cods"])) if a["cods"] else "",
            "servico_padronizado": svc, "grupo_servico": grp,
            "modalidade": a["titulo"], "formacao": a["titulo"],
            "valor_art": a["val"] if a["val"] is not None else "",
            "qtd_linhas_art": a["n"], "qtd_atividades_art": len(a["svcs"]),
            "qtd_codigos_atividade_art": len(a["cods"]),
            "valor_replicado_linhas": valor_replicado,
            "classe_confiabilidade": classe, "usar_calculo_monetario": usar,
            "motivo_exclusao_calculo": mot_excl,
        })

    total = len(base_rows)
    print("Classes:", classe_count)

    # ---------- 1) base_classe_a_servicos_metodologia.csv ----------
    a_fields = ["id_art","ano","municipio","municipio_key","atividade_key","codigo_atividade",
                "servico_padronizado","grupo_servico","modalidade","formacao","valor_art",
                "qtd_linhas_art","qtd_atividades_art","qtd_codigos_atividade_art",
                "valor_replicado_linhas","classe_confiabilidade","usar_calculo_monetario"]
    with open(BASE / "base_classe_a_servicos_metodologia.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=a_fields, extrasaction="ignore")
        w.writeheader()
        for r in base_rows:
            if r["classe_confiabilidade"] == "A":
                w.writerow(r)

    # ---------- 2) agregado_servicos_classe_a.csv ----------
    from collections import defaultdict
    aggA = defaultdict(lambda: {"vals": [], "anos": set(), "muns": set(), "mods": set()})
    for r in base_rows:
        if r["classe_confiabilidade"] != "A":
            continue
        if not isinstance(r["valor_art"], (int, float)):
            continue
        key = (r["servico_padronizado"], r["grupo_servico"])
        g = aggA[key]
        g["vals"].append(r["valor_art"]); g["anos"].add(r["ano"])
        g["muns"].add(r["municipio_key"]); g["mods"].add(r["modalidade"])
    serv_ok = serv_insuf = 0
    with open(BASE / "agregado_servicos_classe_a.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["servico_padronizado","grupo_servico","n_arts","mediana_valor","q1","q3","iqr",
                    "min","max","ano_min","ano_max","municipios_distintos","modalidades_distintas",
                    "confiabilidade","observacao"])
        for (svc, grp), g in sorted(aggA.items(), key=lambda kv: -len(kv[1]["vals"])):
            n = len(g["vals"])
            anos = sorted(x for x in g["anos"] if x and x[0].isdigit())
            if n < 5:
                serv_insuf += 1
                w.writerow([svc, grp, n, "Informacao insuficiente para verificar",
                            "Informacao insuficiente para verificar","Informacao insuficiente para verificar",
                            "Informacao insuficiente para verificar","Informacao insuficiente para verificar",
                            "Informacao insuficiente para verificar",
                            (anos[0] if anos else ""), (anos[-1] if anos else ""),
                            len(g["muns"]), len(g["mods"]), "insuficiente",
                            "n < 5: sem base estatistica para referencia monetaria"])
            else:
                serv_ok += 1
                med, q1, q3, mn, mx = quantiles(g["vals"])
                conf = "alta" if n >= 30 else "media"
                obs = "evidencia auxiliar/indireta; valor da ART, nao honorario liquido"
                if svc == "Nao mapeado" or grp.startswith("Informacao"):
                    conf = "baixa"; obs = "servico nao mapeado; usar apenas como diagnostico"
                w.writerow([svc, grp, n, round(med,2), round(q1,2), round(q3,2), round(q3-q1,2),
                            round(mn,2), round(mx,2), (anos[0] if anos else ""), (anos[-1] if anos else ""),
                            len(g["muns"]), len(g["mods"]), conf, obs])
    print(f"Servicos n>=5: {serv_ok} | n<5: {serv_insuf}")

    # ---------- 3) frequencia_total_servicos.csv ----------
    freq = defaultdict(lambda: {"A":0,"B":0,"C":0,"D":0})
    for r in base_rows:
        key = (r["servico_padronizado"], r["grupo_servico"])
        freq[key][r["classe_confiabilidade"]] += 1
    with open(BASE / "frequencia_total_servicos.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["servico_padronizado","grupo_servico","freq_total","freq_calculo_monetario_A",
                    "freq_secundaria_B","freq_apenas_diagnostico_CD","observacao"])
        for (svc, grp), c in sorted(freq.items(), key=lambda kv: -sum(kv[1].values())):
            tot = c["A"]+c["B"]+c["C"]+c["D"]
            obs = ""
            if grp.startswith("Servico novo"):
                obs = "servico novo / lacuna da tabela atual"
            elif svc == "Nao mapeado":
                obs = "atividade nao mapeada a servico da tabela"
            w.writerow([svc, grp, tot, c["A"], c["B"], c["C"]+c["D"]==0 and 0 or (c["C"]+c["D"]) and (c["C"]+c["D"]), c["C"]+c["D"], obs])
    # fix freq_secundaria column (written wrong above) -> rewrite cleanly
    with open(BASE / "frequencia_total_servicos.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["servico_padronizado","grupo_servico","freq_total","freq_calculo_monetario_A",
                    "freq_secundaria_B","freq_apenas_diagnostico_CD","observacao"])
        for (svc, grp), c in sorted(freq.items(), key=lambda kv: -sum(kv[1].values())):
            tot = c["A"]+c["B"]+c["C"]+c["D"]
            obs = "servico novo / lacuna da tabela atual" if grp.startswith("Servico novo") else (
                  "atividade nao mapeada a servico da tabela" if svc == "Nao mapeado" else "")
            w.writerow([svc, grp, tot, c["A"], c["B"], c["C"]+c["D"], obs])

    # ---------- 4) resumo_classes_confiabilidade.csv ----------
    usos = {
        "A": ("calculo monetario de referencia (base principal)", "ranking individual; uso de media simples"),
        "B": ("analise secundaria/simulacao com regra explicita", "base principal de valor sem ressalva"),
        "C": ("frequencia, demanda e deteccao de novos servicos", "calculo monetario por servico"),
        "D": ("apenas registro de volume e motivo de exclusao", "qualquer calculo monetario"),
    }
    obs_cls = {
        "A": "uma ART, atividade unica, valor associavel com baixo risco de mistura",
        "B": "multi-linha homogenea (mesmo codigo, valor unico replicado)",
        "C": "multi-linha com multiplas atividades/codigos e valor unico nao decomponivel",
        "D": "valor ausente, zerado ou implausivel; ou servico nao mapeavel",
    }
    with open(BASE / "resumo_classes_confiabilidade.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["classe","quantidade_ARTs","percentual","uso_permitido","uso_proibido","observacao"])
        for cl in ["A","B","C","D"]:
            q = classe_count[cl]
            w.writerow([cl, q, f"{round(100*q/total,1)}%", usos[cl][0], usos[cl][1], obs_cls[cl]])

    # ---------- 5) dados para o dashboard ----------
    svc_list, svc_idx = [], {}
    grp_of_svc = {}
    mun_list, mun_idx = [], {}
    ano_list, ano_idx = [], {}
    def gi(lst, idx, key):
        if key not in idx:
            idx[key] = len(lst); lst.append(key)
        return idx[key]
    classeA_s, classeA_m, classeA_a, classeA_v = [], [], [], []
    agg = defaultdict(lambda: [0,0])  # (classeIdx,svcIdx,anoIdx,munIdx)->[n_arts,n_ativ]
    CL = {"A":0,"B":1,"C":2,"D":3}
    for r in base_rows:
        s = gi(svc_list, svc_idx, r["servico_padronizado"]); grp_of_svc[s] = r["grupo_servico"]
        mk = r["municipio_key"] or "(nao informado)"
        m = gi(mun_list, mun_idx, mk)
        an = gi(ano_list, ano_idx, r["ano"])
        ci = CL[r["classe_confiabilidade"]]
        cell = agg[(ci,s,an,m)]; cell[0]+=1; cell[1]+=r["qtd_atividades_art"]
        if r["classe_confiabilidade"]=="A" and isinstance(r["valor_art"],(int,float)):
            classeA_s.append(s); classeA_m.append(m); classeA_a.append(an); classeA_v.append(round(r["valor_art"],2))
    agg_arr = [[k[0],k[1],k[2],k[3],v[0],v[1]] for k,v in agg.items()]
    data = {
        "gerado_em": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "fonte": "ARTs CREA-BA 2022 (ARTs 2022 01022024.csv) - base 2022",
        "total_arts": total, "total_linhas": 726028,
        "classe_count": classe_count,
        "servicos": svc_list, "grupo_de_servico": [grp_of_svc[i] for i in range(len(svc_list))],
        "municipios": mun_list, "anos": ano_list,
        "classeA": {"s": classeA_s, "m": classeA_m, "a": classeA_a, "v": classeA_v},
        "agg": agg_arr,
    }
    (BASE / "dados_metodologia_servicos.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    print("JSON dashboard pronto. Servicos:", len(svc_list), "Municipios:", len(mun_list),
          "Anos:", ano_list, "ClasseA recs:", len(classeA_v))
    # imprime stats para o relatorio
    print("STATS", json.dumps({"classe_count":classe_count,"serv_ok":serv_ok,"serv_insuf":serv_insuf,
          "n_servicos":len(svc_list),"n_municipios":len(mun_list)}, ensure_ascii=False))

if __name__ == "__main__":
    main()

