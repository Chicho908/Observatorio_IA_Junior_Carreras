# Observatorio de IA — «El junior de IA hoy y lo que muestran las carreras»
Edición 1 · corte 06/11/2026 · Fundamentos de Ciencia de Datos, UNSTA · M. A. Chalín, L. A. Sappia, L. A. Tartarini.

**Pregunta (H1):** las habilidades de producción (integración, despliegue, monitoreo, nube/contenedores, Git) tienen menos evidencia publicada en los planes de las carreras argentinas de IA que las habilidades de base (Python, SQL, estadística, ML clásico, deep learning), aunque los avisos de nivel inicial también las piden. Δ = cobertura de base − cobertura de producción, con remuestreo por institución (10.000, semilla 2026). **Resultado de esta edición:** Δ = 0,55 [0,30; 0,80] sobre 5 carreras con contenidos publicados (provisorio; ver §8).

> **AVISO — repositorio PRIVADO.** Este repositorio incluye los datos crudos y los textos de los avisos, incluidos los de LinkedIn (captura automatizada) y Get on Board (`ai-train=no`). **No lo hagas público.** Para compartir algo público se genera la versión sin crudos ni textos con `./run_all.sh publico` (ver `docs/AVISO_DE_DATOS.md`).

## 1. Estructura
```
informe/                    Informe final (informe_final.pdf, fuente .tex y figuras)
data/raw/                   Fuentes crudas, tal como las devolvió cada fuente (no se editan)
  boards/                     413 respuestas de tableros de Greenhouse, Lever y Ashby
  agregadores/                Himalayas, Jobicy, RemoteOK, Remotive y Get on Board
  hn/                         36 hilos «Ask HN: Who is hiring?» (descubrimiento de tableros)
  linkedin/                   Captura de LinkedIn (Apify), limpia, con huella
data/manifiestos/           URL, fecha UTC, código HTTP, tamaño y SHA-256 de cada captura + logs
data/processed/             Tablas generadas por los scripts (CSV sin texto; los .pkl se regeneran)
data/lectura_humana/        Textos de la muestra y hoja de lectura para la codificación humana
config/                     Parámetros, búsquedas, diccionario, codificación de planes, huellas
src/                        Scripts numerados (00 a 12), se ejecutan en orden
reports/                    Perfilado de datos, métricas de la edición y figuras de perfilado
docs/                       Origen de los datos y limpieza, diccionario, guías, continuidad
CHANGELOG.md  requirements.txt  run_all.sh
```

## 2. Cómo usarlo (3 modos)
Requisitos: Python 3.13 y `pip install -r requirements.txt`. Desde la raíz del repositorio:
| Comando | Qué hace | Red | Tarda |
|---|---|---|---|
| `./run_all.sh verificar` | Comprueba huellas y recalcula Δ, figuras y perfilado con las tablas incluidas | no | segundos |
| `./run_all.sh reconstruir` | Rehace todo desde `data/raw/` (pasos 4 a 10 y 11) y verifica que da las mismas huellas | no | ~1 min |
| `./run_all.sh edicion` | Repite el estudio completo con otra fecha de corte (pasos 1 a 11) | sí | horas |
| `./run_all.sh publico` | Genera el zip público (sin crudos ni textos) en `publico/` | no | segundos |

## 3. Orden de ejecución
| Paso | Script | Entrada | Salida | Red |
|---|---|---|---|---|
| 1 | `01_descubrir_tableros.py` | hilos «Ask HN: Who is hiring?» | `config/tableros_descubiertos.json` | sí |
| 2 | `02_capturar_tableros.py` | tableros descubiertos | `data/raw/boards/` + manifiesto | sí |
| 3 | `03_capturar_agregadores_y_getonboard.py` | `config/busquedas.json` | `data/raw/agregadores/` + manifiesto | sí |
| LinkedIn | manual (§4) | cuatro búsquedas | `data/raw/linkedin/…csv` | sí |
| 4 | `04_unificar.py` | crudos + manifiestos | `avisos_api_bruto.pkl` | no |
| 5 | `05_seleccion.py` | API + LinkedIn | `avisos_poblacion_unificada.{pkl,csv}` | no |
| 6 | `06_preparar.py` | población | `avisos_muestra_analisis.{pkl,csv}` | no |
| 7 | `07_linea_base.py` | muestra + diccionario | `resultados_demanda_linea_base.csv` | no |
| 8 | `08_cobertura_planes.py` | `codificacion_planes.csv` | `resultados_cobertura_planes.csv`, Δ, IC, sensibilidad | no |
| 9 | `09_figuras.py` | resultados | `informe/fig_*.png` | no |
| 10 | `10_perfilado_de_datos.py` | tablas procesadas | `reports/` (perfilado y `metricas.json`) | no |
| 11 | `11_preparar_lectura_humana.py` | muestra | `data/lectura_humana/` (textos y plantilla) | no |
| 12 | `12_acuerdo_lectura_humana.py` | dos hojas completadas | `reports/acuerdo_lectura_humana.csv` (kappa) | no |
`00_verificar.py` comprueba las huellas de `config/huellas_esperadas.json` y el valor de Δ.

## 4. Captura de LinkedIn (declarada tal como se hizo)
Scraping automatizado con el actor de Apify `dataji/apify-linkdin-jobs` (v0.0.7): ubicación Argentina, sin filtro de nivel, exclusión de títulos con senior/sr/lead/principal/staff/head/manager/director, descripción completa, tope 300 por búsqueda; cuatro búsquedas (`machine learning`, `AI engineer`, `data scientist`, `inteligencia artificial`); 648 filas brutas, 279 avisos únicos; costo aproximado USD 0,60. Tratado como aprobado por el Directorio (**fecha y acta: completar**). Guardar el resultado en `data/raw/linkedin/` con la fecha y registrar su SHA-256 en `config/huellas_esperadas.json`.

## 5. Documentación (leer en este orden)
| Archivo | Contenido |
|---|---|
| `informe/informe_final.pdf` | Informe final: problema, datos, método, resultados, límites; el Anexo C reúne las 29 decisiones justificadas |
| `docs/DATOS_ORIGEN_Y_LIMPIEZA.md` | De dónde salió cada dato, qué se hizo, qué se limpió, perfil de la muestra |
| `docs/DICCIONARIO_DE_DATOS.md` | Columnas y significado de cada tabla y archivo |
| `docs/GUIA_LECTURA_HUMANA.md` | Cómo completar la lectura humana doble y calcular el acuerdo |
| `docs/CONTINUIDAD_REVISION_Y_MONITOREO.md` | Quién sigue, revisión entre pares y señales de monitoreo |
| `docs/AVISO_DE_DATOS.md` | Condiciones de las fuentes y qué se puede compartir |
| `CHANGELOG.md` | Versiones y correcciones |

**Archivos vigentes:** `informe/informe_final.pdf`, `data/processed/*.csv`, `config/*` y `reports/`. Los `.pkl` son intermedios (se regeneran y no se versionan).

## 6. Nueva edición (otro semestre o año)
1. Clonar a una carpeta fechada. 2. Editar `config/parametros.json` (sobre todo `fecha_corte`) **sin cambiar umbrales**; si hay que cambiar uno, justificarlo y subir `version_protocolo`. 3. `./run_all.sh edicion` (pasos 1 a 3) y captura de LinkedIn antes del paso 5. 4. Pasos 4 a 7. 5. Releer cada plan (fecha de consulta nueva; anotar si cambió) y actualizar `codificacion_planes.csv`. 6. Pasos 8 a 12. 7. Actualizar las cifras del informe. Comparar ediciones solo si reglas y fuentes son las mismas.

## 7. Cómo ampliar
Sumar carreras: filas nuevas en `codificacion_planes.csv` con el mismo libro de códigos. Sumar palabras clave o zonas: editar `config/busquedas.json` y reportar el efecto sobre la población. Sumar fuentes: un script nuevo que deje crudos y manifiesto como los pasos 2 y 3.

## 8. Qué falta (a cargo de quien continúe)
Lectura humana doble de los 97 avisos con kappa ≥ 0,6 (pasos 11 y 12); resolver por lectura los avisos de IA sin dato de años; muestra de control de 100 avisos para el filtro por título; segunda lectura independiente de los planes; codificar las seis carreras con listado o identificación como sensibilidad; 3 a 5 entrevistas; fecha y acta de aprobación de LinkedIn; asignar responsables de la línea (docs de continuidad).

## 9. Límites conocidos
Los avisos de empleo cambian a diario: repetir la captura da otros números (por eso se fija la fecha de corte). Los planes de estudio pueden cambiar y sus páginas **no se guardaron con huella** (la codificación lleva cita textual y URL). Los resultados son provisorios: 5 de 11 carreras, un solo codificador de planes, sin lectura humana de avisos ni entrevistas todavía.
