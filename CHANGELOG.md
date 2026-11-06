# Registro de cambios
Formato: versión · fecha · qué cambió · por qué · quién decidió.

## 1.0 (edición 1, corte 06/11/2026) — 06/11/2026
- Captura de 18.206 avisos únicos de 9 fuentes y selección de 97 avisos (equipo; reglas fijadas antes de mirar habilidades).
- Línea de base de demanda con diccionario v1.0 (fijado antes de ver resultados).
- Codificación de 5 carreras con contenidos y cálculo de Δ = 0,55 (IC 0,30–0,80).
- Corrección: años `NaN` clasificados como «no entrada» → «sin dato» (5.329). Por qué: evitar asumir nivel.
- Corrección: fechas en segundos leídas como milisegundos (Himalayas, Get on Board). Cambió la huella de la tabla unificada.
- Corrección: tableros respondidos 411 y no 413.
- Parámetros movidos a `config/parametros.json`; los resultados no cambiaron (misma huella de la muestra, misma tabla de demanda).
- Pendiente: lectura humana doble (kappa), segunda lectura de planes, seis carreras sin contenidos, entrevistas, fecha y acta del Directorio para LinkedIn.

## 1.0.1 — 06/11/2026 (solo documentación y orden; los resultados no cambian)
- Archivos renombrados con nombres descriptivos: `avisos_poblacion_unificada.csv`, `avisos_muestra_analisis.csv`, `resultados_demanda_linea_base.csv`, `resultados_cobertura_planes.csv`; script 03 pasó a `03_capturar_agregadores_y_getonboard.py`; informe a `informe_final.*`. Las huellas SHA-256 no cambian (dependen del contenido).
- Nuevo `src/10_perfilado_de_datos.py` y carpeta `reports/` (perfilado y `metricas.json`).
- Nuevo `docs/CONTINUIDAD_REVISION_Y_MONITOREO.md`.

## 1.0.2 — 06/11/2026 (repositorio completo; resultados sin cambios)
- Se incorporan al repositorio los datos crudos (`data/raw/`), los textos de la muestra y la hoja de lectura humana; el repositorio es privado (`docs/AVISO_DE_DATOS.md`).
- Nuevos scripts 11 (preparar lectura humana) y 12 (kappa entre lectores), `docs/GUIA_LECTURA_HUMANA.md`.
- `run_all.sh`: modos `reconstruir` (desde los crudos, sin red) y `publico` (zip sin crudos ni textos).
- README reescrito con estructura, modos de uso y orden de ejecución.

## 1.0.3 — 06/11/2026 (sin cambios en resultados)
- Nuevo `docs/PENDIENTES.md` (por qué y cómo de cada pendiente), `src/13_acuerdo_planes.py` (kappa de los planes) y archivos de trabajo en `data/lectura_humana/`: plantilla del segundo lector de planes y muestra de control del filtro por título (100 avisos, semilla 2026).
