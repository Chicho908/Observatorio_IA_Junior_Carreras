# Aviso sobre los datos
- **Repositorio privado.** Incluye texto completo de avisos de empleo de terceros. Se usa solo con fines académicos de este estudio.
- **LinkedIn:** sus términos restringen la captura automatizada; se hizo con un servicio de terceros (Apify) y el Directorio la trató como aprobada (fecha y acta pendientes). Esos textos no deben salir del equipo.
- **Get on Board:** su `robots.txt` declara `ai-train=no`; su texto se lee solo a mano y no se procesa automáticamente (campo `codificacion_solo_humana`).
- **Greenhouse, Lever, Ashby, Himalayas, Jobicy, RemoteOK, Remotive y Hacker News:** se consultaron sus API públicas con User-Agent identificado y pausas; no se verificaron sus condiciones para redistribuir los textos, por eso tampoco se publican.
- **Versión pública:** `./run_all.sh publico` crea `publico/observatorio_ia_publico.zip` con código, configuración, informe, tablas sin texto y manifiestos, sin `data/raw/` ni `data/lectura_humana/avisos_muestra_con_texto.csv`.
- No hay datos personales de candidatos; los avisos mencionan empresas, no personas.
