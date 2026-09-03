---
title: un iframe con sandbox="" deja el documento en origen opaco y sus fuentes caen en silencio
date: 2026-09-03
source: facturaia
tags: [iframe, csp, webfonts, preview, seguridad]
---

Un preview que monta HTML por `srcDoc` dentro de `<iframe sandbox="">` queda en un
**origen opaco**. Consecuencia: el `font-src 'self'` de la CSP del documento no casa con
nada y los `/fonts/*.woff2` pasan a ser cross-origin sin CORS. **No hay error visible**:
el navegador maqueta con la fuente de respaldo.

Duele cuando el preview mide algo. En el reel, el preview calculaba cuántas líneas ocupa
el cierre con `sans-serif` mientras el render real usaba Switzer: distinto ancho de
texto, distinto reparto de líneas, y se aprobaba una composición distinta de la que se
publicaba.

Fix: `sandbox="allow-same-origin"` **sin** `allow-scripts`. El mismo origen sin scripts
es inerte, así que no se regala nada: sigue sin poder ejecutar código, y la CSP del
propio documento puede quedarse en `default-src 'none'`.

Tell general: si un preview y su render pueden divergir, se mide con el motor real
(Playwright + `document.fonts`), no leyendo la spec.
