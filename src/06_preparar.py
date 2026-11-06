"""Paso 6 (Etapa 3): limpieza del texto, idioma, vigencia, duplicados, tope por empresa y congelado de la muestra."""
import json, re, html, hashlib, pandas as pd, numpy as np
PAR = json.load(open("config/parametros.json"))   # parametros de la edicion
SEMILLA, TOPE, VIGENCIA_DIAS, MIN_PAL = PAR["semilla"], PAR["tope_por_empresa"], PAR["vigencia_dias"], PAR["min_palabras"]
HOY = pd.Timestamp(PAR["fecha_corte"], tz="UTC")
d = pd.read_pickle("data/processed/avisos_unificado.pkl")
def limpiar(t):
    t = html.unescape(str(t)); t = re.sub(r"<[^>]+>", " ", t); t = html.unescape(t)
    return re.sub(r"\s+", " ", t).strip()
ES = set("de la el en y los las para con del una un por que se su al como más experiencia trabajo equipo requisitos".split())
EN = set("the and of to in for with a an is are you we our will be as on or your experience team work".split())
def idioma(t):
    w = re.findall(r"[a-záéíóúñ]+", t.lower())[:400]
    if not w: return "?"
    e, i = sum(x in ES for x in w), sum(x in EN for x in w)
    return "es" if e > i * 1.2 else "en" if i > e * 1.2 else "mixto"
e = d[d.nivel_regla.str.startswith("entrada") & d.rol_ia_titulo].copy()
e["texto_limpio"] = e.texto.apply(limpiar); e["idioma"] = e.texto_limpio.apply(idioma)
e["palabras"] = e.texto_limpio.str.split().str.len()
e["dias"] = (HOY - pd.to_datetime(e.fecha_publicacion, utc=True)).dt.days
e["clave"] = e.empresa.str.lower().str.strip() + "|" + e.titulo.str.lower().str.strip()
paso = {"entrada y rol IA": len(e)}
e = e[e.dias <= VIGENCIA_DIAS]; paso[f"vigentes (<={VIGENCIA_DIAS} días)"] = len(e)
e = e[e.palabras >= MIN_PAL]; paso[f"texto >={MIN_PAL} palabras"] = len(e)
e = e.sort_values("id_unico").drop_duplicates("clave"); paso["sin repetir empresa+título"] = len(e)
rng = np.random.default_rng(SEMILLA); e["_r"] = rng.random(len(e))
e = e.sort_values(["empresa", "_r"]).groupby("empresa").head(TOPE).drop(columns="_r")
paso[f"tope {TOPE} por empresa (muestra)"] = len(e)
for k, v in paso.items(): print(f"{k:38s}{v:5d}")
print("empresas:", e.empresa.nunique(), "| máx por empresa:", e.empresa.value_counts().max())
print("idioma:", e.idioma.value_counts().to_dict(), "| palabras mediana/min/max:", int(e.palabras.median()), e.palabras.min(), e.palabras.max())
print("fuente:", e.fuente.value_counts().to_dict()); print("acceso:", e.acceso.value_counts().to_dict())
print("años pedidos (entrada <=2):", e.anios_req.value_counts(dropna=False).sort_index().to_dict())
e.to_pickle("data/processed/muestra_entrada_IA.pkl")
c = e.drop(columns=["texto", "texto_limpio"]); c.to_csv("data/processed/muestra_entrada_IA_sin_texto.csv", index=False)
print("SHA-256 muestra:", hashlib.sha256(open("data/processed/muestra_entrada_IA_sin_texto.csv", "rb").read()).hexdigest())
# sensibilidades de población
for nombre, dias in [("vigencia 180 días", 180), ("vigencia 730 días", 730)]:
    print(nombre, ":", int(((d.nivel_regla.str.startswith('entrada') & d.rol_ia_titulo) & ((HOY - pd.to_datetime(d.fecha_publicacion, utc=True)).dt.days <= dias)).sum()))
