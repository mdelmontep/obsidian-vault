---
title: un 4xx del proveedor que culpa al archivo no es una caída del pipeline
date: 2026-08-03
source: claude-code-session
tags: [llm, openai, ocr, integraciones, alertas]
---
Un `fetch` a un proveedor de IA lanza el mismo error para «este PDF está roto»
(400 `invalid_value`, *"The uploaded file could not be processed"*) que para
«el modelo no existe» (400 `model_not_found`). Si el caller traduce todo a 502
retryable, mezcla dos cosas opuestas: el worker quema sus reintentos recibiendo
el mismo 400 permanente, y se abre una alerta de severidad ALTA por
organización («el OCR está caído») por **un** documento de **un** usuario.

Patrón: clasificar el 4xx antes de tratarlo. 413/415 son del archivo por
definición; 400/422 solo si el cuerpo señala al fichero (`could not be
processed`, `invalid image`, `invalid base64`…). Lo que no encaje sigue siendo
fallo de pipeline: **falla de ese lado**, porque una pista de más convierte una
caída real en documentos archivados en silencio. El camino «archivo» va al
mismo destino que un documento ilegible: revisar, 2xx sin reintento, alerta
resuelta, aviso al usuario con copy propio.

Caso: TuFacturaIA `ocr-process`, PR #1492. Ver
[[alerta-que-se-resuelve-al-volver-a-funcionar-queda-huerfana-si-su-sujeto-desaparece]]
