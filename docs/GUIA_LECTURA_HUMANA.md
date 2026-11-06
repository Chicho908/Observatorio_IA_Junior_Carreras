# Guía de lectura humana de la muestra (97 avisos)
Objetivo: comprobar el diccionario automático y cubrir los avisos de Get on Board (solo lectura humana). Umbral del equipo: kappa ≥ 0,6 (Landis y Koch, 1977).
1. `python src/11_preparar_lectura_humana.py` (ya generado) deja en `data/lectura_humana/` los textos y `hoja_lectura_plantilla.csv`.
2. Cada lector copia la plantilla a `hoja_lectura_A.csv` o `hoja_lectura_B.csv` y lee **por separado**, sin ver la hoja del otro ni los resultados del diccionario.
3. Por aviso y habilidad: **1** si el aviso nombra o exige la habilidad (aunque sea en una lista); **0** si no la nombra. No inferir: si no está escrita, es 0. Las 10 habilidades y sus palabras están en el Anexo A del informe.
4. `python src/12_acuerdo_lectura_humana.py data/lectura_humana/hoja_lectura_A.csv data/lectura_humana/hoja_lectura_B.csv` calcula el kappa por habilidad y global (`reports/acuerdo_lectura_humana.csv`).
5. Si una habilidad queda bajo 0,6: discutir los desacuerdos, precisar la definición, repetir y registrar en el CHANGELOG (nueva versión del diccionario).
6. Reportar en el informe el acuerdo y las diferencias contra el diccionario automático.
