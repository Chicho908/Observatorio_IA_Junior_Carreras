"""Paso 3: agregadores remotos y Get on Board, con las mismas palabras clave que la captura de LinkedIn."""
import json, pathlib, urllib.parse
from comun import *

cfg = json.load(open("config/busquedas.json"))
manif, log = [], {}
def pedir(nombre, fuente, url):
    ruta = pathlib.Path("data/raw/agregadores") / nombre
    if ruta.exists(): return
    crudo, st = get_json(url, pausa=2.0)               # pausa mayor: son servicios chicos
    log[nombre] = st
    if crudo is not None: guardar_crudo("data/raw/agregadores", nombre, crudo, manif, fuente, url, st)

for kw in cfg["palabras_clave"]:
    q = urllib.parse.quote_plus(kw); k = kw.replace(" ", "_")
    for pag in range(cfg["paginas_max_por_busqueda"]):
        pedir(f"himalayas__{k}__{pag}.json", "himalayas",
              f"https://himalayas.app/jobs/api/search?q={q}&page={pag+1}")
    pedir(f"jobicy__{k}.json", "jobicy", f"https://jobicy.com/api/v2/remote-jobs?count=50&tag={q}")
    pedir(f"remotive__{k}.json", "remotive", f"https://remotive.com/api/remote-jobs?search={q}&limit=100")
pedir("remoteok__todo.json", "remoteok", "https://remoteok.com/api")

for cat in cfg["gob_categorias"]:
    for pag in range(1, 11):
        n = f"getonboard__{cat}__{pag}.json"
        pedir(n, "getonboard",
              f"https://www.getonbrd.com/api/v0/categories/{cat}/jobs?per_page=100&page={pag}&expand[]=seniority&expand[]=company")
        p = pathlib.Path("data/raw/agregadores")/n
        if not p.exists(): break
        meta = json.loads(p.read_bytes()).get("meta", {})
        if pag >= meta.get("total_pages", 1): break
json.dump(manif, open("data/raw/agregadores/manifiesto_agregadores.json", "w"), indent=1)
print(json.dumps(log))
