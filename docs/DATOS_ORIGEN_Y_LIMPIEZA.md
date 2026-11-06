# De dónde salieron los datos, qué se hizo y cómo se limpió

Captura realizada el **06/11/2026** (UTC). Los archivos crudos no se modifican; cada uno tiene URL, fecha, código HTTP, tamaño y SHA-256 en `data/raw/*/manifiesto_*.json` (copia en `data/manifiestos/`, que también va en la versión pública).

## 1. Fuentes
| Fuente | Qué es | Cómo se obtuvo | Avisos únicos |
|---|---|---|---|
| LinkedIn Argentina | Portal de empleo | Scraping automatizado con el actor de Apify `dataji/apify-linkdin-jobs` v0.0.7, 4 búsquedas (`config/busquedas.json`), 648 filas brutas; aprobado por el Directorio (fecha/acta a completar) | 279 |
| Greenhouse | Tableros de empresas | API pública `boards-api.greenhouse.io/v1/boards/{empresa}/jobs?content=true` | 11.264 |
| Ashby | Tableros de empresas | API pública `api.ashbyhq.com/posting-api/job-board/{empresa}` | 4.487 |
| Lever | Tableros de empresas | API pública `api.lever.co/v0/postings/{empresa}?mode=json` | 1.549 |
| Himalayas, Jobicy, RemoteOK, Remotive | Agregadores de trabajo remoto | API públicas, mismas palabras clave, pausa de 2 s | 223 / 133 / 99 / 12 |
| Get on Board | Portal de empleo tecnológico de LatAm | API pública, categorías `machine-learning-ai` y `data-science-analytics`; **texto solo para lectura humana** (`ai-train=no`) | 160 |
| Hacker News «Ask HN: Who is hiring?» | Hilos mensuales (36) | API pública de Algolia; solo para descubrir los tableros (513; 411 respondieron, 102 ya no existen) | — |
| Planes de estudio | 11 carreras de 10 instituciones | Páginas y PDF oficiales; 5 con contenidos codificadas el 06/11/2026 (`config/codificacion_planes.csv`) | — |

Buenas prácticas: User-Agent identificado («UNSTA-student-project, academic research»), pausa de 1 s (2 s en agregadores), sin datos personales, sin evadir restricciones.

## 2. Qué se hizo, paso por paso (con el script)
1. `01`: descubrir tableros en 36 hilos de HN → `config/tableros_descubiertos.json`.
2. `02`: capturar cada tablero → `data/raw/boards/` + manifiesto.
3. `03`: capturar agregadores y Get on Board → `data/raw/agregadores/` + manifiesto.
4. LinkedIn: captura manual con el actor indicado → `data/raw/linkedin/` (huella en `config/huellas_esperadas.json`).
5. `04`: unificar todas las fuentes en una tabla con las columnas del diccionario.
6. `05`: deduplicar por identificador, clasificar rol de IA por título y nivel por años pedidos, grupo de acceso.
7. `06`: limpiar texto (HTML a texto), idioma, vigencia ≤ 365 días, ≥ 100 palabras, deduplicar empresa + título, tope de 10 por empresa (semilla 2026).
8. `07`: línea de base de demanda con el diccionario v1.0 (bootstrap por empresa).
9. `08`: cobertura publicada de los planes, Δ y sensibilidad (bootstrap por institución).
10. `09`: figuras del informe.

## 3. Limpieza y control de calidad
| Problema | Hallazgo | Tratamiento |
|---|---|---|
| Duplicados | LinkedIn 648 filas → 279 avisos; entre avisos de entrada, 161 → 104 al unir empresa y título | Uno por identificador; uno por empresa y título |
| Años faltantes | 5.489 avisos (30,1 %) sin años pedidos: 5.329 quedan «sin dato» y 160 usan el nivel que declara la fuente; unos 470–500 de rol de IA a resolver por lectura humana | Categoría «sin dato», a resolver por lectura humana |
| Años atípicos | Números > 20 («fundada hace 25 años») | Se ignoran; solo cuentan cerca de palabras de experiencia |
| Fechas | Himalayas y Get on Board en segundos, leídas como milisegundos (1970) | Corregido en `04_unificar.py`; cambió la huella de la tabla unificada |
| Años `NaN` | Se clasificaban «no entrada» (5.329 avisos) | Corregido: «sin dato» |
| Tableros | Se informó 413 respondidos; son 411 | Corregido (413 contaba también manifiesto y registro) |
| Texto corto | 2 avisos < 100 palabras | Excluidos |
| Cobertura | 15 de 97 avisos son de Argentina; 88 % en inglés | Se describe aparte; límite declarado |

## 4. Perfil de la muestra (97 avisos)
61 empresas; fuentes: Greenhouse 42, Ashby 24, Himalayas 13, LinkedIn 12, Lever 3, Get on Board 2, Jobicy 1; acceso: otra región 81, Argentina 15, remoto sin país 1; idioma: 85 inglés y 12 español; mediana 633 palabras (104 a 1.878); fechas 11/2025 a 11/2026; años pedidos: 0 (4), 1 (23), 2 (68) y 2 sin años cuyo nivel es el declarado por la fuente.

## 5. Límites
Los avisos cambian a diario (otra captura da otros avisos); los textos se guardan solo en el repositorio privado; los planes pueden cambiar y sus páginas no se guardaron con huella (por eso la codificación lleva cita y URL).
