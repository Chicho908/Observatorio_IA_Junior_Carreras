"""Verifica que lo publicado se reproduce: huellas SHA-256 de los archivos y resultado de Delta.
Uso (desde la carpeta raiz del repositorio): python src/00_verificar.py
Los archivos que contienen texto de avisos no se redistribuyen: si faltan, se informa 'no presente' y no es un error."""
import hashlib, json, os, subprocess, sys
ok = True
for ruta, esperado in json.load(open("config/huellas_esperadas.json")).items():
    if not os.path.exists(ruta):
        print(f"[no presente] {ruta}"); continue
    h = hashlib.sha256(open(ruta, "rb").read()).hexdigest()
    print(("[OK]  " if h == esperado else "[DIFIERE] ") + ruta); ok &= (h == esperado)
salida = subprocess.run([sys.executable, "src/08_cobertura_planes.py"], capture_output=True, text=True).stdout
esperado = "0.55 [0.3 0.8]"
bien = esperado in salida
print(("[OK]  " if bien else "[DIFIERE] ") + f"Delta principal esperado {esperado}")
sys.exit(0 if ok and bien else 1)
