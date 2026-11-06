# Continuidad, revisión entre pares y monitoreo

## 1. Continuidad (el observatorio debe poder seguir sin sus fundadores)
- Todo lo necesario para repetir la edición está en este repositorio; no depende de pasos que solo conozca una persona.
- **Responsables:** los cargos del Observatorio (dirección, suplencias, responsable por línea) **no están asignados todavía**; se definirán en el Directorio. Mientras tanto, esta línea la mantienen sus tres autores. Completar al decidirse:
  | Rol | Titular | Suplente | Desde |
  |---|---|---|---|
  | Responsable de la línea «El junior de IA» | _a definir_ | _a definir_ | _a definir_ |
- Quien deje la línea lo avisa en el repositorio (CHANGELOG) y entrega la edición en curso con su `metricas.json`.
- Ritmo de actualización propuesto: una edición por semestre, con las mismas reglas (ver README §5).

## 2. Revisión entre pares (liviana, antes de publicar)
Quien publica pide la lectura de una persona de **otra línea**. Lista de control (5 minutos, respondida con sí / no / no sé):
1. ¿El problema, la unidad de análisis y la hipótesis se entienden sin explicación oral?
2. ¿Cada dato dice de dónde viene, cuándo y cómo se obtuvo (`docs/DATOS_ORIGEN_Y_LIMPIEZA.md`)?
3. ¿Cada umbral o decisión está justificado (Anexo C del informe)?
4. ¿Los números del informe coinciden con `reports/metricas.json` y con `./run_all.sh verificar`?
5. ¿Lo que se afirma es lo que muestran los datos (cobertura publicada ≠ aprendizaje; muestra pequeña)?
6. ¿Se declaran los límites y lo que no se hizo?
7. ¿Hay algo que pueda perjudicar a una persona o institución (nombres, datos personales, rankings)?

Registro de la revisión (completar):
| Fecha | Revisor/a y línea | Observaciones | Resuelto |
|---|---|---|---|
| _pendiente_ | | | |

## 3. Monitoreo y actualización
El producto es un informe, no un servicio en línea; se vigilan estas señales en cada edición:
| Riesgo | Señal | Acción |
|---|---|---|
| Cambio de esquema | Una API cambia campos o devuelve error (el manifiesto registra código HTTP y tamaño) | Fallar al capturar, anotar en CHANGELOG, ajustar `04_unificar.py` |
| Cambio de distribución | Cambian mucho el embudo, la proporción de avisos de entrada o el idioma frente a la edición anterior (`reports/perfilado_*.csv`) | Revisar reglas y fuentes; no comparar ediciones si cambió el protocolo |
| Cambio de los planes | Una carrera modifica su plan o su página | Volver a codificar con fecha y cita |
| Pérdida de acceso | LinkedIn o una fuente bloquea o cambia condiciones | Declararlo y registrar la nueva versión del protocolo |
| Pérdida de valor | La ficha por carrera no se usa o no responde a ninguna decisión | Revisar el problema con usuarios (informe, sección 6) |
