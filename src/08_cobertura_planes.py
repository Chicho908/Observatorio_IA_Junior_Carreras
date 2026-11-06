"""Cobertura publicada de habilidades en los planes (celda = 1 o NA, nunca 0).
Delta = media(base) - media(produccion) por carrera; bootstrap por institucion."""
import numpy as np, pandas as pd
import json
PAR = json.load(open("config/parametros.json"))
SEMILLA, B = PAR["semilla"], PAR["remuestreos"]
d = pd.read_csv("config/codificacion_planes.csv")
d["x"] = (pd.to_numeric(d["valor"], errors="coerce") == 1).astype(float)   # NA no es 0: queda como sin evidencia publicada
def delta(df):
    g = df.groupby(["institucion","carrera","grupo"])["x"].mean().unstack()
    g["delta"] = g["base"] - g["produccion"]
    return g
def boot(df, excluir=None):
    g = delta(df).reset_index().groupby("institucion")["delta"].mean()
    rng = np.random.default_rng(SEMILLA)
    v = g.values
    m = np.array([rng.choice(v, len(v), replace=True).mean() for _ in range(B)])
    return g, v.mean(), np.percentile(m,[2.5,97.5])
tab = delta(d); print(tab.round(2))
cob = d.groupby(["habilidad","grupo"])["x"].agg(["sum","count"]); print(cob)
g, media, ic = boot(d); print(g.round(2).to_dict(), round(media,3), ic.round(3))
# sensibilidad a casos limite: codificar 1 los casos limite (UNL Git, UTN Python y SQL)
d2 = d.copy()
for c,h in [("UNL Ing. en IA","Git"),("UTN-FRLP Lic. en IA","Python"),("UTN-FRLP Lic. en IA","SQL")]:
    d2.loc[(d2.carrera==c)&(d2.habilidad==h),"x"]=1
g2, m2, ic2 = boot(d2); print("limite a 1:", g2.round(2).to_dict(), round(m2,3), ic2.round(3))
# sensibilidad: sin la integracion de UADE (caso limite) y con Palermo contado como dos unidades
d3 = d.copy(); d3.loc[(d3.carrera.str.startswith("UADE"))&(d3.habilidad=="Integración"),"x"]=0
g3, m3, ic3 = boot(d3); print("UADE integracion=0:", g3.round(2).to_dict(), round(m3,3), ic3.round(3))
t = tab.reset_index(); print("Delta por carrera, media simple:", round(t.delta.mean(),3))
tab.round(3).to_csv("data/processed/resultados_cobertura_planes.csv")
