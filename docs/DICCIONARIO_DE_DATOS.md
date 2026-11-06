# Diccionario de datos

Cada tabla indica qué es una fila, de dónde sale y qué significa cada columna. «NA» = dato ausente; en la codificación de planes, NA significa información insuficiente y no «cero».

## 1. `data/processed/avisos_poblacion_unificada.csv` (población unificada; 18.206 filas)
Una fila = un aviso único (identificador `fuente:id`). Generada por `src/04_unificar.py` y `src/05_seleccion.py`. No incluye el texto.
| Columna | Tipo | Significado |
|---|---|---|
| `id_unico` | texto | `fuente:identificador` del aviso en su plataforma |
| `fuente` | texto | greenhouse, ashby, lever, linkedin, himalayas, getonboard, jobicy, remoteok, remotive |
| `metodo_captura` | texto | «API pública» o scraping automatizado (LinkedIn) |
| `consulta` | texto | búsquedas en las que apareció el aviso, separadas por « | » |
| `fecha_captura` | fecha UTC | cuándo se pidió el archivo de origen |
| `sha256_origen` | texto | huella del archivo crudo de origen (ver `data/manifiestos/`) |
| `url` | texto | enlace público del aviso |
| `fecha_publicacion` | fecha UTC | fecha de publicación según la plataforma (puede ser la de última actualización) |
| `titulo`, `empresa`, `ubicacion` | texto | tal como los publica la fuente |
| `modalidad` | texto | remote / hybrid / onsite si la fuente lo informa (76,6 % NA) |
| `nivel_declarado` | texto | nivel que declara la plataforma; **no se usa** para clasificar (no es confiable), salvo Get on Board (95,6 % NA) |
| `codificacion_solo_humana` | lógico | verdadero para Get on Board (`ai-train=no`): su texto no se procesa automáticamente |
| `rol_ia_titulo` | lógico | el título contiene un término de rol de IA (regla D5 del informe) |
| `anios_req` | número | máximo de años de experiencia pedido en el texto, en contexto de experiencia, ignorando números > 20 (30,1 % NA) |
| `nivel_regla` | texto | `entrada (<=2)`, `no entrada (>=3)`, `entrada/no entrada (declarada)` o `sin dato` ; valores reales: `no entrada (>=3)` 10.405, `sin dato` 5.329, `entrada (<=2)` 2.312, `no entrada (declarada)` 149, `entrada (declarada)` 11 |
| `acceso` | texto | Argentina; LatAm o mundial declarado; remoto sin país; otra región |

## 2. `data/processed/avisos_muestra_analisis.csv` (muestra de análisis; 97 filas)
Una fila = un aviso de entrada y de rol de IA, vigente, con ≥100 palabras, sin repetir empresa y título, máximo 10 por empresa. Generada por `src/06_preparar.py`. Tiene las columnas de la tabla 1 y además:
| Columna | Significado |
|---|---|
| `idioma` | `en` o `es` (heurística por palabras frecuentes) |
| `palabras` | cantidad de palabras del texto limpio |
| `dias` | días entre la publicación y la fecha de corte |
| `clave` | clave de duplicado (empresa + título normalizados) |

## 3. `data/processed/resultados_demanda_linea_base.csv` (11 + 3 filas)
`habilidad`, `grupo` (base, produccion, ia_actual, resumen), `avisos` (k), `pct` (100·k/n, n = 95), `ic_inf`, `ic_sup` (IC 95 % por remuestreo de empresas, 10.000, semilla 2026).

## 4. `config/codificacion_planes.csv` (50 filas = 5 carreras × 10 habilidades)
| Columna | Significado |
|---|---|
| `carrera`, `institucion` | carrera codificada y su institución (unidad de remuestreo) |
| `habilidad`, `grupo` | una de las 10 habilidades y su grupo (base o producción) |
| `valor` | `1` = el plan publicado muestra la habilidad (con cita); `NA` = información insuficiente |
| `asignatura`, `cita` | dónde y con qué texto (celdas positivas y casos límite) |
| `url` | página o PDF consultado el 06/11/2026 («idem» = la de la fila anterior de la misma carrera) |

## 5. `data/processed/resultados_cobertura_planes.csv`
Por carrera: proporción de habilidades de base con evidencia (`base`), de producción (`produccion`) y `delta` = base − producción.

## 6. `data/raw/*/manifiesto_*.json` (copiados en `data/manifiestos/` del paquete)
Una entrada por archivo crudo: `archivo`, `fuente`, `url` consultada, `fecha_captura_utc`, `http` (código), `bytes`, `sha256`.

## 7. `config/*.json`
`parametros.json` (parámetros de la edición), `busquedas.json` (palabras clave y categorías), `diccionario_habilidades.json` (expresiones regulares de la línea de base, v1.0), `tableros_descubiertos.json` (tableros de Greenhouse/Lever/Ashby descubiertos), `huellas_esperadas.json`.

## 8. `reports/` (generado por `src/10_perfilado_de_datos.py`)
| Archivo | Contenido |
|---|---|
| `metricas.json` | Métricas de la edición: tamaños, Δ, intervalo, veredicto de H1, semilla, huellas SHA-256 y versiones del entorno |
| `perfilado_columnas_*.csv` | Por columna: tipo, nulos, % de nulos, valores únicos (población y muestra) |
| `perfilado_numericas_*.csv` | Estadísticos descriptivos de las columnas numéricas |
| `perfilado_frecuencias_*.csv` | Conteos por fuente, nivel, acceso e idioma |
| `perfilado_resumen.json` | Filas, columnas y duplicados (por identificador y por empresa más título) |
| `figuras/perfil_*.png` | Valores vacíos por columna y distribuciones de la muestra |

Nota: en la población hay 2.069 filas repetidas por empresa y título (mismo puesto en varias sedes o fuentes); no se eliminan allí porque la población describe lo publicado, y se resuelven en la muestra (regla de duplicados, 0 repetidos).
