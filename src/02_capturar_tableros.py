"""Paso 2: capturar avisos de cada tablero por su API pública, con pausa y sin modificar la respuesta."""
import json, pathlib
from comun import *

tab = json.load(open("config/tableros_descubiertos.json"))
URL = {
 "greenhouse": "https://boards-api.greenhouse.io/v1/boards/{s}/jobs?content=true",
 "lever":      "https://api.lever.co/v0/postings/{s}?mode=json",
 "ashby":      "https://api.ashbyhq.com/posting-api/job-board/{s}",
}
manif, resumen = [], {k: {"ok": 0, "inexistente": 0, "error": 0} for k in URL}
for tipo, slugs in tab.items():
    for s in slugs:
        ruta = pathlib.Path("data/raw/boards") / f"{tipo}__{s}.json"
        if ruta.exists():               # idempotente: no se vuelve a pedir lo ya capturado
            resumen[tipo]["ok"] += 1; continue
        u = URL[tipo].format(s=s)
        crudo, st = get_json(u, pausa=PAUSA)
        if crudo is None:
            resumen[tipo]["inexistente" if st in (404, 410) else "error"] += 1
            continue
        guardar_crudo("data/raw/boards", ruta.name, crudo, manif, tipo, u, st)
        resumen[tipo]["ok"] += 1
json.dump(manif, open("data/raw/boards/manifiesto_boards.json", "w"), indent=1)
print(json.dumps(resumen))
