"""Utilidades comunes: cliente HTTP educado, huella SHA-256 y manifiesto."""
import hashlib, json, time, urllib.request, urllib.error, datetime, pathlib

UA = "UNSTA-student-project/0.1 (academic research; Fundamentos de Ciencia de Datos)"
PAUSA = 1.0  # segundos entre pedidos (ver justificación en la Etapa 2)

def ahora():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")

def get_json(url, pausa=PAUSA, reintentos=2):
    for i in range(reintentos + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=40) as r:
                crudo = r.read()
            time.sleep(pausa)
            return crudo, r.status
        except urllib.error.HTTPError as e:
            time.sleep(pausa)
            if e.code in (404, 410):      # tablero inexistente: no es un error del proceso
                return None, e.code
            if i == reintentos:
                return None, e.code
            time.sleep(3 * (i + 1))
        except Exception:
            if i == reintentos:
                return None, -1
            time.sleep(3 * (i + 1))

def sha256(b):
    return hashlib.sha256(b).hexdigest()

def guardar_crudo(carpeta, nombre, crudo, manifiesto, fuente, url, estado):
    ruta = pathlib.Path(carpeta) / nombre
    ruta.write_bytes(crudo)                      # se guarda tal cual lo devolvió la API
    manifiesto.append({"archivo": str(ruta), "fuente": fuente, "url": url,
                       "fecha_captura_utc": ahora(), "http": estado,
                       "bytes": len(crudo), "sha256": sha256(crudo)})
