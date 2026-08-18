---
title: un carácter fuera de latin-1 en una cabecera HTTP tumba la respuesta entera
date: 2026-08-18
source: claude-code-session
tags: [http, fetch, nextjs, bugs-silenciosos, copy]
---

Los valores de cabecera HTTP son **ByteString**: cualquier carácter por encima de U+00FF
hace que `new Response(body, { headers })` lance un `TypeError`, y la petición muere con 500
después de haber hecho todo el trabajo. Los acentos pasan (`ó` = U+00F3), pero el **em-dash**
(`—`, U+2014), las comillas tipográficas y las flechas, no.

```js
new Response('x', { headers: { 'X-Status': 'formato oficial — pendiente' } })
// TypeError: Cannot convert argument to a ByteString ... value of 8212
```

La trampa es de dónde sale el texto: **una constante de prosa reutilizada como cabecera**.
Nació para un JSON de respuesta o un mensaje de UI —donde el em-dash es normal— y alguien la
enchufó también a un header. Nadie revisa una constante de copy pensando en bytes.

Caso real (TuFacturaIA, 18-ago): `STATUS_303_POSICIONAL` viajaba en `X-Fiscal-Status`, así que
**toda** descarga del fichero oficial de la AEAT devolvía 500 — nunca funcionó. Sobrevivió
porque la ruta no tenía un solo test y porque en producción no había ni una descarga: el primer
test que se escribió contra ella lo destapó de rebote.

Regla: si una constante de texto puede acabar en una cabecera, mantenla ASCII, o asértalo
(`[...s].every(c => c.codePointAt(0) <= 255)`). Y sospecha de los nombres de fichero: en
`Content-Disposition` el mismo problema entra por `filename=` con acentos.

Ver [[postgrest-max-rows-trunca-silencioso-in-revienta-url]] — misma familia: el fallo no avisa
porque el camino no se recorre nunca.
