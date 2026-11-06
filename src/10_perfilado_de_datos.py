"""Perfilado de los datos (comprension de datos) y metricas de la edicion.
Entradas : data/processed/avisos_poblacion_unificada.csv, avisos_muestra_analisis.csv,
           resultados_cobertura_planes.csv, config/parametros.json
Salidas  : reports/perfilado_*.csv, reports/metricas.json, reports/figuras/perfil_*.png
No necesita red ni texto de avisos."""
import json, hashlib, platform, sys
from pathlib import Path
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt

PAR = json.load(open("config/parametros.json"))
R = Path("reports"); (R / "figuras").mkdir(parents=True, exist_ok=True)
tablas = {"poblacion": "data/processed/avisos_poblacion_unificada.csv",
          "muestra": "data/processed/avisos_muestra_analisis.csv"}
resumen = {}
for nombre, ruta in tablas.items():
    d = pd.read_csv(ruta)
    col = pd.DataFrame({"tipo": d.dtypes.astype(str), "nulos": d.isna().sum(),
                        "pct_nulos": (100 * d.isna().mean()).round(1), "valores_unicos": d.nunique()})
    col.index.name = "columna"; col.to_csv(R / f"perfilado_columnas_{nombre}.csv")
    d.describe().T.round(2).to_csv(R / f"perfilado_numericas_{nombre}.csv")
    resumen[nombre] = {"filas": int(len(d)), "columnas": int(d.shape[1]),
                       "duplicados_id_unico": int(d.id_unico.duplicated().sum()),
                       "duplicados_empresa_titulo": int(d.duplicated(["empresa", "titulo"]).sum())}
    fig, ax = plt.subplots(figsize=(7, 4)); col.pct_nulos.sort_values().plot.barh(ax=ax, color="#1f4e79")
    ax.set_xlabel("% de valores vacíos"); ax.set_title(f"Valores vacíos por columna ({nombre})")
    fig.tight_layout(); fig.savefig(R / "figuras" / f"perfil_nulos_{nombre}.png", dpi=150); plt.close()

p, m = pd.read_csv(tablas["poblacion"]), pd.read_csv(tablas["muestra"])
for nombre, serie in {"poblacion_fuente": p.fuente, "poblacion_nivel_regla": p.nivel_regla,
                      "muestra_fuente": m.fuente, "muestra_acceso": m.acceso, "muestra_idioma": m.idioma}.items():
    serie.value_counts().rename_axis("valor").rename("avisos").to_csv(R / f"perfilado_frecuencias_{nombre}.csv")
fig, ax = plt.subplots(1, 3, figsize=(11, 3.4))
m.palabras.plot.hist(ax=ax[0], bins=15, color="#1f4e79"); ax[0].set_xlabel("palabras por aviso")
m.anios_req.value_counts().sort_index().plot.bar(ax=ax[1], color="#1f4e79"); ax[1].set_xlabel("años pedidos")
pd.to_datetime(m.fecha_publicacion).dt.to_period("M").value_counts().sort_index().plot.bar(ax=ax[2], color="#1f4e79"); ax[2].set_xlabel("mes de publicación")
for a in ax: a.set_ylabel("avisos")
fig.suptitle("Distribuciones de la muestra de análisis (97 avisos)"); fig.tight_layout()
fig.savefig(R / "figuras" / "perfil_distribuciones_muestra.png", dpi=150); plt.close()

# metricas de la edicion (equivalente a metrics.json del proceso end to end)
c = pd.read_csv("data/processed/resultados_cobertura_planes.csv")
por_inst = c.groupby("institucion").delta.mean()
rng = np.random.default_rng(PAR["semilla"])
boot = [rng.choice(por_inst.values, len(por_inst), replace=True).mean() for _ in range(PAR["remuestreos"])]
lo, hi = np.percentile(boot, [2.5, 97.5])
veredicto = "sostenida" if lo > 0 else "refutada" if hi < 0 else "sin resolver"
huella = lambda f: hashlib.sha256(open(f, "rb").read()).hexdigest()
metricas = {"protocolo": PAR["version_protocolo"], "fecha_corte": PAR["fecha_corte"],
            "avisos_poblacion": int(len(p)), "avisos_muestra": int(len(m)), "empresas_muestra": int(m.empresa.nunique()),
            "carreras_codificadas": int(len(c)), "instituciones": int(len(por_inst)),
            "delta_media": round(float(por_inst.mean()), 3), "delta_ic95": [round(float(lo), 3), round(float(hi), 3)],
            "h1": veredicto, "semilla": PAR["semilla"], "remuestreos": PAR["remuestreos"],
            "huellas_sha256": {k: huella(v) for k, v in tablas.items()},
            "entorno": {"python": platform.python_version(), "pandas": pd.__version__, "numpy": np.__version__, "matplotlib": matplotlib.__version__}}
json.dump(metricas, open(R / "metricas.json", "w"), indent=2, ensure_ascii=False)
json.dump(resumen, open(R / "perfilado_resumen.json", "w"), indent=2, ensure_ascii=False)
print(json.dumps(resumen, indent=1)); print("Delta", metricas["delta_media"], metricas["delta_ic95"], metricas["h1"])
