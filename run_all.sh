#!/usr/bin/env bash
# Uso:  ./run_all.sh verificar   -> reproduce Delta y figuras con los datos incluidos (sin red)
#       ./run_all.sh edicion     -> repite todo el recorrido con config/parametros.json (usa red; ver README)
set -euo pipefail
cd "$(dirname "$0")"
case "${1:-verificar}" in
  verificar) python src/00_verificar.py; python src/09_figuras.py ;;
  edicion)
    for p in 01_descubrir_tableros 02_capturar_tableros 03_capturar_agregadores_gob 04_unificar 05_seleccion 06_preparar 07_linea_base 08_cobertura_planes 09_figuras; do
      echo "== $p"; python "src/$p.py"; done
    echo "Falta: captura de LinkedIn (manual con el actor indicado en el README) ANTES del paso 05, y lectura humana." ;;
  *) echo "modo desconocido"; exit 1 ;;
esac
