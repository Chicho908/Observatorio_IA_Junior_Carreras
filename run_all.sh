#!/usr/bin/env bash
# Uso:  ./run_all.sh verificar   -> reproduce Delta y figuras con los datos incluidos (sin red)
#       ./run_all.sh reconstruir -> rehace todo desde data/raw (sin red) y compara huellas
#       ./run_all.sh publico     -> zip sin crudos ni textos
#       ./run_all.sh edicion     -> repite todo el recorrido con config/parametros.json (usa red; ver README)
set -euo pipefail
cd "$(dirname "$0")"
case "${1:-verificar}" in
  reconstruir)
    rm -f data/processed/*.pkl
    for p in 04_unificar 05_seleccion 06_preparar 07_linea_base 08_cobertura_planes 09_figuras 10_perfilado_de_datos 11_preparar_lectura_humana; do
      echo "== $p"; python "src/$p.py" > /dev/null; done
    python src/00_verificar.py ;;
  publico)
    mkdir -p publico; zip -qr publico/observatorio_ia_publico.zip . -x "data/raw/*" "data/lectura_humana/avisos_muestra_con_texto.csv" "*.pkl" ".git/*" "publico/*" "__pycache__/*"
    echo "Creado publico/observatorio_ia_publico.zip" ;;
  verificar) python src/00_verificar.py; python src/09_figuras.py; python src/10_perfilado_de_datos.py ;;
  edicion)
    for p in 01_descubrir_tableros 02_capturar_tableros 03_capturar_agregadores_y_getonboard 04_unificar 05_seleccion 06_preparar 07_linea_base 08_cobertura_planes 09_figuras 10_perfilado_de_datos 11_preparar_lectura_humana; do
      echo "== $p"; python "src/$p.py"; done
    echo "Falta: captura de LinkedIn (manual con el actor indicado en el README) ANTES del paso 05, y lectura humana." ;;
  *) echo "modo desconocido"; exit 1 ;;
esac
