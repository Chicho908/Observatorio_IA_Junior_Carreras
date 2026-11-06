"""Paso 12: acuerdo entre dos lectores (kappa de Cohen) por habilidad y global.
Uso: python src/12_acuerdo_lectura_humana.py data/lectura_humana/hoja_lectura_A.csv data/lectura_humana/hoja_lectura_B.csv
Umbral de la convencion del equipo: kappa >= 0,6 (Landis y Koch, 1977). Si no se alcanza, se ajusta el diccionario y se repite (nueva version)."""
import sys, pandas as pd
a, b = (pd.read_csv(f).set_index("id_unico") for f in sys.argv[1:3])
hab = [c for c in a.columns if c not in ("empresa", "titulo", "url", "observaciones")]
def kappa(x, y):
    po = (x == y).mean(); p1, p2 = x.mean(), y.mean(); pe = p1 * p2 + (1 - p1) * (1 - p2)
    return float("nan") if pe == 1 else (po - pe) / (1 - pe)
filas = [(h, round(kappa(a[h].astype(int), b.loc[a.index, h].astype(int)), 3)) for h in hab]
xa = a[hab].astype(int).values.ravel(); xb = b.loc[a.index, hab].astype(int).values.ravel()
filas.append(("GLOBAL", round(kappa(pd.Series(xa), pd.Series(xb)), 3)))
r = pd.DataFrame(filas, columns=["habilidad", "kappa"]); r["cumple_0.6"] = r.kappa >= 0.6
print(r.to_string(index=False)); r.to_csv("reports/acuerdo_lectura_humana.csv", index=False)
