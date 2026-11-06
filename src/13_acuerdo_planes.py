"""Paso 13: acuerdo entre dos codificadores de los planes (kappa de Cohen).
Uso: python src/13_acuerdo_planes.py data/lectura_humana/codificacion_planes_lector2.csv
El segundo lector parte de plantilla_codificacion_planes_lector2.csv (valor vacio) y llena 1 o NA sin ver config/codificacion_planes.csv.
Se compara celda por celda (carrera x habilidad). Umbral del equipo: kappa >= 0,6."""
import sys, pandas as pd
a = pd.read_csv("config/codificacion_planes.csv"); b = pd.read_csv(sys.argv[1])
k = ["carrera", "habilidad"]
m = a.merge(b[k + ["valor"]], on=k, suffixes=("_1", "_2"))
x = (pd.to_numeric(m.valor_1, errors="coerce") == 1).astype(int); y = (pd.to_numeric(m.valor_2, errors="coerce") == 1).astype(int)
po = (x == y).mean(); p1, p2 = x.mean(), y.mean(); pe = p1 * p2 + (1 - p1) * (1 - p2)
kap = float("nan") if pe == 1 else (po - pe) / (1 - pe)
print(f"celdas: {len(m)} | acuerdo simple: {po:.3f} | kappa: {kap:.3f} | cumple 0,6: {kap >= 0.6}")
print("Desacuerdos:"); print(m[x != y][k + ["valor_1", "valor_2"]].to_string(index=False))
