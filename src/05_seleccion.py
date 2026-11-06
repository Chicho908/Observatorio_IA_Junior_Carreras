"""Paso 5: une LinkedIn + API, deduplica, aplica reglas v1 (rol de IA por título, nivel de entrada v2)
y perfila el embudo. NO se examinan habilidades en este paso."""
import hashlib, pandas as pd
from reglas import *
a = pd.read_pickle("data/processed/avisos_api_bruto.pkl")
# --- consultas por aviso (un aviso puede salir en varias búsquedas) y deduplicación por id
cons = a.groupby("id_unico")["consulta"].agg(lambda s: " | ".join(sorted(set(map(str, s)))))
a = a.drop_duplicates("id_unico").copy(); a["consulta"] = a.id_unico.map(cons)
# --- LinkedIn (captura automatizada con servicio de terceros, declarada como tal)
p = "data/raw/linkedin/avisos_IA_AR_limpio_2026-11-06.csv"
h = hashlib.sha256(open(p, "rb").read()).hexdigest()
l = pd.read_csv(p)
li = pd.DataFrame(dict(id_unico="linkedin:" + l.jobId.astype(str), fuente="linkedin",
    metodo_captura="Scraping automatizado (Apify, actor dataji/apify-linkdin-jobs v0.0.7)", consulta=l.palabras_clave,
    fecha_captura=l.scrapedAt, sha256_origen=h, url=l.jobUrl, fecha_publicacion=l.postedAt.astype(str).str[:10], titulo=l.title,
    empresa=l.companyName, ubicacion=l.location, modalidad=None, nivel_declarado=l.seniorityLevel, texto=l.description,
    codificacion_solo_humana=False))
d = pd.concat([a, li], ignore_index=True)
# --- reglas (idénticas para todas las fuentes)
d["rol_ia_titulo"] = d.titulo.apply(rol_ia)
d["anios_req"] = [None if s else anios_requeridos(t) for s, t in zip(d.codificacion_solo_humana, d.texto)]   # Get on Board: no se procesa el texto
def nivel(r):
    if r.fuente == "getonboard":                      # nivel declarado por la propia plataforma (campo estructurado)
        return "entrada (declarada)" if r.nivel_declarado in ("No experience required", "Junior") else "no entrada (declarada)"
    return nivel_v2(r.anios_req)
d["nivel_regla"] = d.apply(nivel, axis=1)
d["acceso"] = d.ubicacion.apply(grupo_acceso)
d.to_pickle("data/processed/avisos_poblacion_unificada.pkl")
d.drop(columns=["texto"]).to_csv("data/processed/avisos_poblacion_unificada.csv", index=False)
print("SHA-256 LinkedIn limpio:", h)
e = d.nivel_regla.str.startswith("entrada")
t = pd.DataFrame({"avisos": d.groupby("fuente").size(),
                  "rol_IA(título)": d[d.rol_ia_titulo].groupby("fuente").size(),
                  "entrada": d[e].groupby("fuente").size(),
                  "entrada&IA": d[e & d.rol_ia_titulo].groupby("fuente").size(),
                  "IA sin dato de nivel": d[(d.nivel_regla == "sin dato") & d.rol_ia_titulo].groupby("fuente").size(),
                  "empresas": d.groupby("fuente").empresa.nunique()}).fillna(0).astype(int)
t.loc["TOTAL"] = t.sum(); t.loc["TOTAL", "empresas"] = d.empresa.nunique()
print(t.to_string())
print("\nTOTAL únicos:", d.id_unico.nunique())
print("\nentrada&IA por grupo de acceso:"); print(d[e & d.rol_ia_titulo].groupby(["fuente", "acceso"]).size().to_string())
