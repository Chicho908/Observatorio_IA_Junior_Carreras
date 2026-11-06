"""Paso 1: descubrir tableros públicos (Greenhouse, Lever, Ashby) en los hilos mensuales
'Ask HN: Who is hiring?' de los últimos N meses. Sesgo declarado: solo aparecen empresas que
publicaron en esos hilos."""
import json, re, sys, collections, html, pathlib
from comun import *

N_HILOS = json.load(open("config/parametros.json"))["n_hilos_hn"]
manif = []
q = f"https://hn.algolia.com/api/v1/search_by_date?tags=story,author_whoishiring&hitsPerPage=60"
crudo, st = get_json(q)
guardar_crudo("data/raw/hn", "indice_whoishiring.json", crudo, manif, "hn_algolia", q, st)
hilos = [h for h in json.loads(crudo)["hits"] if h["title"].startswith("Ask HN: Who is hiring?")][:N_HILOS]
print("hilos:", [(h["title"][-14:], h["objectID"]) for h in hilos])

RX = re.compile(r'(?:boards|job-boards)(?:\.eu)?\.greenhouse\.io/(?:embed/job_board\?for=)?([A-Za-z0-9_-]+)'
                r'|jobs\.lever\.co/([A-Za-z0-9_.-]+)|jobs\.ashbyhq\.com/([A-Za-z0-9_.%-]+)', re.I)
tableros = collections.defaultdict(set)
for h in hilos:
    u = f"https://hn.algolia.com/api/v1/items/{h['objectID']}"
    ruta = pathlib.Path("data/raw/hn") / f"hilo_{h['objectID']}.json"
    if ruta.exists():                      # si ya se descargó, se reutiliza (idempotente)
        crudo = ruta.read_bytes()
    else:
        crudo, st = get_json(u, pausa=1.5)
        if crudo is None: print("fallo hilo", h["objectID"], st); continue
        guardar_crudo("data/raw/hn", ruta.name, crudo, manif, "hn_algolia", u, st)
    # el texto de los comentarios viene con entidades HTML (&#x2F; = "/"): se decodifica antes de buscar
    texto = html.unescape(crudo.decode("utf-8", "ignore").replace("\\u002F", "/").replace("\\/", "/"))
    for m in RX.finditer(texto):
        for tipo, slug in zip(("greenhouse", "lever", "ashby"), m.groups()):
            if slug and slug.lower() not in ("embed", "jobs", "job_board"):
                tableros[tipo].add(slug.lower().rstrip("."))
res = {k: sorted(v) for k, v in tableros.items()}
json.dump(res, open("config/tableros_descubiertos.json", "w"), indent=1)
json.dump(manif, open("data/raw/hn/manifiesto_hn.json", "w"), indent=1)
print({k: len(v) for k, v in res.items()})
