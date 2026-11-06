"""Reglas de selección v1 (fijadas antes de mirar habilidades). Mismo código para todas las fuentes."""
import re, html

RX_IA = re.compile(r'\b(?:ai|ia|ml|llm|llms|nlp|genai|mlops)\b|machine learning|data scien|deep learning|'
                   r'inteligencia artificial|computer vision|generative|agentic|ag[eé]ntica|cient[ií]fic[oa] de datos', re.I)
RX_SENIOR = re.compile(r'\b(?:senior|sr|lead|principal|staff|head|manager|director)\b', re.I)
RX_ANIOS = re.compile(r'(\d{1,2})\s*\+?\s*(?:(?:-|–|a|to)\s*\d{1,2}\s*)?(?:years?|años?)', re.I)
RX_CTX = re.compile(r'experien|experience|trabaj|working|background|track record|profesional', re.I)

def texto_plano(s):
    if not s: return ""
    s = html.unescape(html.unescape(str(s)))
    s = re.sub(r'<(?:br|/p|/li|/h\d|/div)[^>]*>', '\n', s, flags=re.I)
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'[ \t\r\f\v]+', ' ', re.sub(r'\n\s*\n+', '\n', s)).strip()

def rol_ia(titulo):
    return bool(RX_IA.search(titulo or ""))

def anios_requeridos(texto):
    """Máximo de años mencionado en contexto de experiencia (criterio v2). None si no hay dato."""
    t = re.sub(r'\s+', ' ', texto or ""); vals = []
    for m in RX_ANIOS.finditer(t):
        n = int(m.group(1))
        if n > 20: continue                       # antigüedad de la empresa, no requisito
        if RX_CTX.search(t[max(0, m.start()-80):m.end()+80]): vals.append(n)
    return max(vals) if vals else None

def nivel_v2(anios):
    if anios is None or anios != anios: return "sin dato"   # None o NaN (pandas)
    return "entrada (<=2)" if anios <= 2 else "no entrada (>=3)"

def grupo_acceso(ubic):
    u = (ubic or "").lower()
    if re.search(r'argentin|buenos aires|c[oó]rdoba|rosario|mendoza|tucum', u): return "Argentina"
    if re.search(r'latam|latin|latinoam|worldwide|anywhere|global|world', u): return "LatAm o mundial declarado"
    if re.search(r'^\s*remote\s*$|^\s*remoto\s*$|^\s*$', u): return "remoto sin país"
    return "otra región"
