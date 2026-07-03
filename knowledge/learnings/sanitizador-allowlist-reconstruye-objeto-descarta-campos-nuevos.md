---
title: sanitizador que reconstruye un objeto por allowlist descarta silenciosamente campos nuevos si no se actualiza a la vez
date: 2026-07-03
source: claude-code-session
tags: [validation, sanitize, config-jsonb, regresion-silenciosa]
---

Patrón: una función `sanitizeX(raw)` que RECONSTRUYE el objeto desde cero
listando explícitamente cada campo permitido (en vez de whitelist+passthrough)
es segura contra inyección pero es una trampa al añadir un campo nuevo al
tipo: si no se añade también aquí, el campo se pierde sin error, sin warning,
sin fallo de tests (los tests viejos no lo cubren porque el campo no existía).

Peor aún si la función se ejecuta también en el **path de render/lectura**
(no solo al guardar) — entonces el dato puede estar bien guardado en BD y
seguir sin aplicarse nunca, porque cada render lo vuelve a descartar.

Fix: al añadir un campo a un tipo con sanitizador de este estilo, grep el
sanitizador Y añadir un test que falle si el campo se pierde. Caso real
(TuFacturaIA, `CabeceraOpts.mostrarNombre`): el toggle se guardaba bien pero
el PDF seguía mostrando el nombre porque `normalizeLayout()` se llama en
cada render y su sanitizador no conocía el campo nuevo.
