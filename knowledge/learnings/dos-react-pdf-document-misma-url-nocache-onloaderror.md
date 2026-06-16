---
title: dos <Document> de react-pdf con misma URL no-cache concurrentes → onLoadError
date: 2026-06-16
source: claude-code-session
tags: [react-pdf, pdf, nextjs]
---
Montar dos `<Document file={url}>` de react-pdf a la vez con la MISMA URL servida con
`Cache-Control: no-cache` (p.ej. el visor central + un comparador en un drawer) hace que
el navegador comparta/aborte una de las dos peticiones in-flight → la 2ª instancia recibe
un body abortado → dispara `onLoadError` → "No se pudo cargar el documento".

No es problema de tamaño del contenedor (con width 0 muestra skeleton, no error).
Fix barato: cache-buster por instancia, `url + (url.includes('?')?'&':'?') + 'cmp=1'`
(el endpoint ignora params extra). Alternativa: no montar dos visores del mismo PDF.
Caso: FacturaIA details-panel comparador, 2026-06-16.
