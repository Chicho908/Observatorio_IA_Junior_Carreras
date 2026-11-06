"""Paso 7 (Etapa 4): línea de base automática por diccionario. No procesa texto de Get on Board (solo codificación humana)."""
import json, re, numpy as np, pandas as pd
PAR = json.load(open("config/parametros.json"))
SEMILLA, B = PAR["semilla"], PAR["remuestreos"]
m = pd.read_pickle("data/processed/avisos_muestra_analisis.pkl")
m = m[~m.codificacion_solo_humana].reset_index(drop=True)
dic = json.load(open("config/diccionario_habilidades.json"))
cols, grupo = [], {}
for g in ("base", "produccion", "ia_actual"):
    for k, rx in dic[g].items():
        m[k] = m.texto_limpio.str.lower().str.contains(rx, regex=True).astype(int); cols.append(k); grupo[k] = g
m["alguna_base"] = (m[[c for c in cols if grupo[c]=="base"]].sum(axis=1) > 0).astype(int)
m["alguna_prod"] = (m[[c for c in cols if grupo[c]=="produccion"]].sum(axis=1) > 0).astype(int)
m["tres_prod"] = (m[["Integración","Despliegue","Monitoreo"]].sum(axis=1) == 3).astype(int)
todas = cols + ["alguna_base", "alguna_prod", "tres_prod"]
emp = m.groupby("empresa")[todas].agg(["sum"]); emp.columns = todas; emp["n"] = m.groupby("empresa").size()
rng = np.random.default_rng(SEMILLA); E = len(emp); idx = rng.integers(0, E, size=(B, E))
N = emp.n.values; out = []
for c in todas:
    S = emp[c].values; p = S.sum() / N.sum()
    bs = S[idx].sum(axis=1) / N[idx].sum(axis=1); lo, hi = np.percentile(bs, [2.5, 97.5])
    out.append((c, grupo.get(c, "resumen"), int(S.sum()), round(100*p, 1), round(100*lo, 1), round(100*hi, 1)))
r = pd.DataFrame(out, columns=["habilidad", "grupo", "avisos", "pct", "ic_inf", "ic_sup"])
print("n avisos:", len(m), "| empresas:", E); print(r.to_string(index=False))
r.to_csv("data/processed/resultados_demanda_linea_base.csv", index=False)
ar = m[m.acceso == "Argentina"]; print("\nArgentina n=", len(ar), "(solo conteos):"); print(ar[todas].sum().to_string())
# sensibilidad: sin tope (todas las empresas con todos sus avisos únicos de la muestra previa al tope se evalúan aparte en etapa 5); aquí: solo avisos con 2 años o menos de 1 año
print("\nSolo <=1 año (n=%d):" % (m.anios_req <= 1).sum()); print(m[m.anios_req <= 1][todas].mean().mul(100).round(1).to_string())
