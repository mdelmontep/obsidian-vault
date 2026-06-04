---
title: validar la url resolviendo dns no cierra el rebinding si el fetch re-resuelve por hostname
date: 2026-06-05
source: claude-code-session
tags: [ssrf, dns-rebinding, undici, seguridad, webhooks]
---
Un helper anti-SSRF que resuelve el hostname, valida que TODAS las IPs son públicas
y devuelve la IP NO cierra el DNS-rebinding si el caller luego hace `fetch(url)` por
hostname: undici/Chromium RE-RESUELVEN el DNS → ventana TOCTOU donde un DNS hostil
(TTL bajo) sirve IP privada entre la validación y el fetch.
Fix (Node/undici): pinear el fetch a la IP ya validada con un Agent custom —
`new Agent({ connect: { lookup: (h,o,cb)=>cb(null,[{address: ip, family}]) } })` y pasarlo
como `dispatcher` en el fetch. MANTENER el hostname en la URL (NO reescribir a
https://<ip>: rompe SNI + verificación de cert). Cerrar el Agent tras el fetch (1 uso).
`redirect:'manual'` para no seguir Location con la IP pineada. Chromium (Puppeteer) NO
se puede pinear fácil → residual; mitigar con JS off + CSP default-src none + solo type=image.
El comentario del helper no debe prometer mitigación que el caller no implementa.
Caso TuFacturaIA webhooks dispatcher PR #153. Ver [[dokploy-cron-docker-exec-no-hereda-env-de-app-env]].
