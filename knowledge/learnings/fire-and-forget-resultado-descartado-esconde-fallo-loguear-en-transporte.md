---
title: fire-and-forget cuyo resultado se descarta esconde el fallo — loguear en el transporte compartido
date: 2026-07-05
source: claude-code-session
tags: [observabilidad, whatsapp, async, facturaia]
---

Distinto de "el side-effect no llega a ejecutarse" ([[fire-and-forget-en-handler-corto-pierde-side-effect]]):
aquí la llamada SÍ se ejecuta completa, pero su resultado (`{ok:false, errorCode, errorText}`)
se descarta porque todos los callers hacen `void enviar(...)` sin mirarlo. Si la función
de transporte tampoco loguea internamente, un fallo real (token, rate-limit, restricción)
queda 100% invisible: sin error, sin efecto visible al usuario, sin fila en BD.

Caso TuFacturaIA (WhatsApp): `postToGraph` (base de `sendText`/`sendInteractiveButtons`/
`sendInteractiveList`) devolvía el resultado granular pero nunca lo logueaba; ~35 call
sites en el webhook usan `void sendText(...)`. Un fallo de Meta tras un flujo multi-org
recién arreglado quedó indiagnosticable — el log del contenedor no tenía NADA tras el
punto donde el flujo (confirmado por BD) siguió adelante.

Fix: loguear en el ÚNICO punto de transporte compartido (`postToGraph`), no en cada uno
de los N callers — 1 línea de log cubre todos los fire-and-forget de golpe. Nunca loguear
el body del mensaje (PII), solo `errorCode`/`errorText`/metadata.

Regla general: si una función se llama `void` en más de un sitio, ES ella (no el caller)
quien debe garantizar que un fallo deja rastro.
