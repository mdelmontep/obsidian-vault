---
title: playwright page.request respeta la caché http del browser
date: 2026-06-11
source: claude-code-session
tags: [playwright, e2e, cache, http]
---

`page.request.get()` en Playwright comparte el contexto del browser y **respeta su caché HTTP**: si el endpoint responde 200 sin `Cache-Control: no-store`, lecturas sucesivas en el mismo test devuelven datos stale (p. ej. stock que acaba de cambiar por una acción de UI).

Síntoma típico: el assert tras una mutación lee el valor antiguo aunque la BD ya esté actualizada.

Fixes:
- Workaround en test: cache-buster `?_=${i}` en la URL (contador, NO `Date.now()` si el harness lo bloquea).
- Fix real: el endpoint de lectura "fresca" debe enviar `Cache-Control: no-store` (o `private, no-cache`).

Caso real: E2E stock TuFacturaIA 2026-06-11, `/api/stock/productos` sin header → 8/8 PASS solo tras cache-buster.
