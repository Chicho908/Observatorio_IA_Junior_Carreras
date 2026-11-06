"""Paso 11: prepara la lectura humana de la muestra (97 avisos).
Salidas (data/lectura_humana/): avisos_muestra_con_texto.csv (texto limpio para leer) y
hoja_lectura_plantilla.csv (una fila por aviso, una columna por habilidad, para completar con 1 / 0).
Cada lector completa su copia: hoja_lectura_A.csv y hoja_lectura_B.csv. Regla: 1 = el aviso nombra o exige
la habilidad; 0 = no la nombra. Ver docs/GUIA_LECTURA_HUMANA.md."""
import json, pandas as pd
from pathlib import Path
m = pd.read_pickle("data/processed/avisos_muestra_analisis.pkl")
dic = json.load(open("config/diccionario_habilidades.json"))
hab = list(dic["base"]) + list(dic["produccion"])
Path("data/lectura_humana").mkdir(parents=True, exist_ok=True)
m[["id_unico", "fuente", "empresa", "titulo", "url", "idioma", "codificacion_solo_humana", "texto_limpio"]].to_csv(
    "data/lectura_humana/avisos_muestra_con_texto.csv", index=False)
t = m[["id_unico", "empresa", "titulo", "url"]].copy()
for h in hab: t[h] = ""
t["observaciones"] = ""
t.to_csv("data/lectura_humana/hoja_lectura_plantilla.csv", index=False)
print(len(t), "avisos;", len(hab), "habilidades:", hab)
