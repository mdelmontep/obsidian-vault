---
title: mockear el wrapper de auth esconde el 400 que ve el usuario
date: 2026-07-27
source: claude-code-session
tags: [testing, api, nextjs, facturaia, vitest]
---

Un test de endpoint que mockea el wrapper de auth (`withApiAuth`, `withApiV1`,
`withCronTracking`) y le inyecta un contexto listo (`body: {}`, `orgId`, `role`)
prueba el handler, **no la petición**. Todo lo que el wrapper decide —parseo de
body, límites, rate limit, permisos— queda fuera del test, y ahí caben fallos
que el usuario ve en el primer clic.

Caso TuFacturaIA 2026-07-26. La acción nueva "Volver a abrir y recalcular"
llamaba con `fetch(url, { method: 'POST' })`, sin body. La ruta declaraba
`parseBody: true` sin `bodyOptional`, así que `withApiAuth` respondía
`400 Invalid JSON` **antes** del handler: la reapertura nunca funcionó desde la
interfaz, y el usuario solo leía "No se pudo volver a abrir la declaración". Los
tests estaban verdes porque el mock inyectaba `body: {}`. Las otras dos acciones
de la misma ruta sí mandaban body, así que funcionaban — la asimetría no la ve
nadie leyendo el handler.

Qué hacer:

- Si se mockea el wrapper, añadir **un** test que compruebe las opts con las que
  la ruta se registra (`expect(authOpts.bodyOptional).toBe(true)`). Es barato y
  cubre justo lo que el mock esconde.
- Mejor aún, un test con `Request` real sin body contra el wrapper de verdad,
  para las rutas cuya UI llama sin payload.
- `fetch(POST)` sin body manda `Content-Length: 0` y `req.json()` lanza. Un POST
  sin payload necesita `bodyOptional` explícito.
- Regla general: la suite verde no dice que el botón funcione. Pulsarlo sí.

Ver [[mock-de-createdocument-oculta-violaciones-de-check-del-nucleo-fiscal]]
