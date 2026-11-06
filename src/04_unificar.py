"""Paso 4: unifica todas las fuentes en una tabla con las columnas acordadas. No se modifica ningún crudo."""
import json, glob, pathlib, datetime, pandas as pd
from reglas import *
man = {}
for f in glob.glob("data/raw/*/manifiesto_*.json"):
    for m in json.load(open(f)): man[pathlib.Path(m["archivo"]).name] = m
filas = []
def add(fuente, archivo, idv, consulta, url, pub, titulo, empresa, ubic, modal, nivel, texto, solo_humano=False):
    m = man.get(archivo, {})
    filas.append(dict(id_unico=f"{fuente}:{idv}", fuente=fuente, metodo_captura="API pública", consulta=consulta,
        fecha_captura=m.get("fecha_captura_utc"), sha256_origen=m.get("sha256"), url=url, fecha_publicacion=pub,
        titulo=titulo, empresa=empresa, ubicacion=ubic, modalidad=modal, nivel_declarado=nivel,
        texto=texto, codificacion_solo_humana=solo_humano))
def ms(x):
    try: return datetime.datetime.fromtimestamp((int(x)/1000 if int(x)>1e11 else int(x)), datetime.timezone.utc).date().isoformat()
    except: return None
for f in sorted(glob.glob("data/raw/boards/*.json")):
    n = pathlib.Path(f).name
    if n.startswith("manifiesto"): continue
    tipo, slug = n[:-5].split("__", 1); j = json.load(open(f))
    if tipo == "greenhouse":
        for x in j.get("jobs", []):
            add(tipo, n, x["id"], slug, x.get("absolute_url"), (x.get("updated_at") or "")[:10], x.get("title"), slug,
                (x.get("location") or {}).get("name"), None, None, texto_plano(x.get("content")))
    elif tipo == "lever":
        for x in j if isinstance(j, list) else []:
            c = x.get("categories") or {}
            t = x.get("descriptionPlain") or ""; t += "\n" + "\n".join(f"{l.get('text','')} {texto_plano(l.get('content'))}" for l in x.get("lists", []))
            add(tipo, n, x["id"], slug, x.get("hostedUrl"), ms(x.get("createdAt")), x.get("text"), slug,
                c.get("location"), x.get("workplaceType"), None, t + "\n" + (x.get("additionalPlain") or ""))
    elif tipo == "ashby":
        for x in j.get("jobs", []):
            add(tipo, n, x["id"], slug, x.get("jobUrl"), (x.get("publishedAt") or "")[:10], x.get("title"), slug,
                x.get("location"), "remote" if x.get("isRemote") else None, None, x.get("descriptionPlain") or texto_plano(x.get("descriptionHtml")))
for f in sorted(glob.glob("data/raw/agregadores/*.json")):
    n = pathlib.Path(f).name
    if n.startswith("manifiesto"): continue
    fuente, *resto = n[:-5].split("__"); consulta = resto[0].replace("_", " ") if resto else "todo"; j = json.load(open(f))
    if fuente == "himalayas":
        for x in j.get("jobs", []):
            add(fuente, n, x.get("guid"), consulta, x.get("applicationLink"), ms(x.get("pubDate")) if str(x.get("pubDate","")).isdigit() else str(x.get("pubDate",""))[:10],
                x.get("title"), x.get("companyName"), ", ".join(x.get("locationRestrictions") or []) or "Worldwide", "remote",
                ", ".join(x.get("seniority") or []) or None, texto_plano(x.get("description")))
    elif fuente == "jobicy":
        for x in j.get("jobs", []):
            lv = x.get("jobLevel"); lv = ", ".join(lv) if isinstance(lv, list) else lv
            add(fuente, n, x.get("id"), consulta, x.get("url"), (x.get("pubDate") or "")[:10], x.get("jobTitle"), x.get("companyName"),
                x.get("jobGeo") if isinstance(x.get("jobGeo"), str) else ", ".join(x.get("jobGeo") or []), "remote", lv, texto_plano(x.get("jobDescription")))
    elif fuente == "remotive":
        for x in j.get("jobs", []):
            add(fuente, n, x.get("id"), consulta, x.get("url"), (x.get("publication_date") or "")[:10], x.get("title"), x.get("company_name"),
                x.get("candidate_required_location"), "remote", None, texto_plano(x.get("description")))
    elif fuente == "remoteok":
        for x in j if isinstance(j, list) else []:
            if "position" not in x: continue
            add(fuente, n, x.get("id"), consulta, x.get("url"), (x.get("date") or "")[:10], x.get("position"), x.get("company"),
                x.get("location"), "remote", None, texto_plano(x.get("description")))
    elif fuente == "getonboard":
        for x in j.get("data", []):
            a = x["attributes"]; sen = ((a.get("seniority") or {}).get("data") or {}).get("attributes", {}).get("name")
            comp = (((a.get("company") or {}).get("data") or {}).get("attributes") or {}).get("name")
            pais = ", ".join(a.get("countries") or []) if isinstance(a.get("countries"), list) else a.get("countries")
            add(fuente, n, x["id"], consulta, (x.get("links") or {}).get("public_url"), ms(a.get("published_at")) if isinstance(a.get("published_at"), (int, float)) else str(a.get("published_at") or "")[:10],
                a.get("title"), comp, pais, a.get("remote_modality"), sen, texto_plano(a.get("description")), solo_humano=True)
d = pd.DataFrame(filas)
d.to_pickle("data/processed/api_unificado_bruto.pkl")
print(d.groupby("fuente").size().to_string(), "\nTOTAL filas", len(d), "| ids únicos", d.id_unico.nunique())
