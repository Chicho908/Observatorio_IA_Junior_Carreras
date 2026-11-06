# Observatorio de IA — El junior de IA hoy y lo que muestran las carreras
Edición 1 (corte 06/11/2026). Fundamentos de Ciencia de Datos, UNSTA. Autores: M. A. Chalín, L. A. Sappia, L. A. Tartarini.

Este paquete permite (A) **verificar** los resultados del informe sin red y (B) **repetir** el estudio en otra fecha.
El informe (`informe/informe.pdf`) justifica cada decisión; el Anexo C las reúne todas en una tabla.

## 1. Qué hay en cada carpeta
| Ruta | Contenido |
|---|---|
| `informe/` | Informe en LaTeX y PDF, y las figuras |
| `config/parametros.json` | Todos los parámetros de la edición (fecha de corte, semilla, vigencia, tope, años de entrada, remuestreos) |
| `config/busquedas.json` | Las cuatro palabras clave de búsqueda |
| `config/diccionario_habilidades.json` | Diccionario de la línea de base (versión 1.0, fijado antes de ver resultados) |
| `config/codificacion_planes.csv` | Codificación de los planes: 10 habilidades por carrera, 1 o NA, asignatura, cita y URL |
| `config/tableros_descubiertos.json` | Tableros de empresas descubiertos en los hilos de Hacker News |
| `config/huellas_esperadas.json` | Huellas SHA-256 de los archivos de referencia |
| `src/` | Scripts numerados; se ejecutan en orden |
| `data/processed/` | Tablas **sin texto de avisos**: población unificada, muestra de análisis, demanda, cobertura |
| `data/manifiestos/` | Manifiestos de captura (URL, fecha UTC, código HTTP, tamaño, SHA-256 de cada respuesta) |

Los archivos crudos y los textos de los avisos **no se redistribuyen**: LinkedIn restringe la captura automatizada y su uso se limita a este estudio; Get on Board declara `ai-train=no`. Sí se publican identificadores, URL y huellas.


## 1b. Documentación del repositorio (léase en este orden)
| Archivo | Para qué sirve |
|---|---|
| `docs/DATOS_ORIGEN_Y_LIMPIEZA.md` | De dónde salió cada dato, cómo se capturó, qué se hizo en cada paso, qué se limpió y perfil de la muestra |
| `docs/DICCIONARIO_DE_DATOS.md` | Columnas, tipos y significado de cada tabla y archivo de configuración |
| `CHANGELOG.md` | Versiones del protocolo y correcciones (cuál es la versión vigente y por qué cambió) |
| `informe/informe.pdf` | Informe final (versión vigente); `informe_v1.tex` es solo histórico |

**Archivos vigentes:** `data/processed/*.csv` (se regeneran con `src/`), `config/*` y `informe/informe.pdf`. Todo lo demás es histórico o intermedio y no debe usarse para citar resultados.

## 2. Verificar (sin red)
```
pip install -r requirements.txt
./run_all.sh verificar
```
Comprueba las huellas de los archivos presentes y recalcula Δ (esperado 0,55; IC 95 % 0,30 a 0,80) y las figuras.

## 3. Orden de ejecución completo
| Paso | Script | Entrada | Salida | Red |
|---|---|---|---|---|
| 1 | `01_descubrir_tableros.py` | hilos «Ask HN: Who is hiring?» | `config/tableros_descubiertos.json` | sí |
| 2 | `02_capturar_tableros.py` | tableros descubiertos | `data/raw/boards/` + manifiesto | sí |
| 3 | `03_capturar_agregadores_gob.py` | `config/busquedas.json` | `data/raw/agregadores/` + manifiesto | sí |
| LinkedIn | (manual, ver 4) | cuatro búsquedas | `data/raw/linkedin/…csv` | sí |
| 4 | `04_unificar.py` | crudos + manifiestos | `api_unificado_bruto.pkl` | no |
| 5 | `05_seleccion.py` | API + LinkedIn | `avisos_unificado*.{pkl,csv}` | no |
| 6 | `06_preparar.py` | población unificada | muestra de análisis | no |
| 7 | `07_linea_base.py` | muestra + diccionario | `demanda_linea_base.csv` | no |
| 8 | `08_cobertura_planes.py` | `codificacion_planes.csv` | cobertura, Δ, IC, sensibilidad | no |
| 9 | `09_figuras.py` | resultados | `informe/fig_*.png` | no |

## 4. Captura de LinkedIn (declarada tal como se hizo)
Scraping automatizado con el actor de Apify `dataji/apify-linkdin-jobs` (v0.0.7): ubicación Argentina, sin filtro de nivel, exclusión de títulos con senior/sr/lead/principal/staff/head/manager/director, descripción completa, tope 300 por búsqueda; cuatro búsquedas (`machine learning`, `AI engineer`, `data scientist`, `inteligencia artificial`). Costo aproximado: USD 0,60. Requiere aprobación del Directorio (fecha y acta: completar). Guardar el resultado en `data/raw/linkedin/` con la fecha y registrar su SHA-256.

## 5. Nueva edición (otro semestre o año)
1. Copiar el paquete a una carpeta fechada. 2. Editar `config/parametros.json` (sobre todo `fecha_corte`) **sin cambiar umbrales**; si hay que cambiar uno, justificarlo y subir `version_protocolo`. 3. Ejecutar los pasos 1 a 3 y la captura de LinkedIn. 4. Pasos 4 a 7. 5. Releer cada plan (fecha de consulta nueva, anotar si cambió) y actualizar `codificacion_planes.csv`. 6. Pasos 8 y 9. 7. Actualizar las cifras del informe. Comparar ediciones solo si reglas y fuentes son las mismas.

## 6. Cómo ampliar
Sumar carreras: agregar filas a `codificacion_planes.csv` con el mismo libro de códigos. Sumar palabras clave o zonas: editar `config/busquedas.json` y reportar el efecto sobre la población. Sumar fuentes: un script nuevo que deje crudos y manifiesto como los pasos 2 y 3.

## 7. Qué falta (a cargo de quien continúe)
Lectura humana doble de los 97 avisos con kappa ≥ 0,6; resolver por lectura los avisos de IA sin dato de años; muestra de control de 100 avisos para el filtro por título; segunda lectura independiente de los planes; codificar las seis carreras con listado o identificación como sensibilidad; 3 a 5 entrevistas; fecha y acta de aprobación de LinkedIn.

## 8. Límites conocidos de la reproducción
Los avisos de empleo cambian a diario: repetir la captura da otros números (por eso se fija la fecha de corte). Los planes de estudio pueden cambiar. Las páginas de los planes no se guardaron con huella; por eso `codificacion_planes.csv` lleva la cita textual y la URL.
