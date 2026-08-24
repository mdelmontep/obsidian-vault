---
title: lock e idempotencia en n8n con redis incr — el nodo no tiene set nx
date: 2026-08-24
source: elphis-psicologia
tags: [n8n, redis, idempotencia, lock]
---
El nodo Redis de n8n no expone SET NX. Lock atómico equivalente: **INCR con
`expire: true, ttl: N`** — si devuelve 1 el lock es tuyo; >1, de otra ejecución
(y expira solo). Liberar = DELETE de la clave.

Shapes medidos (sonda, n8n 2.36):
- GET → `{<propertyName>: "valor"}` y `{<propertyName>: null}` si no existe;
  **reemplaza el item** (no passthrough) → leer upstream con `$('Nodo')`.
- INCR → `{"<clave>": n}` con la clave literal como campo → `Object.values($json)[0]`.
- SET → passthrough del item de entrada.

Redis caído: `onError: continueErrorOutput` a una rama "degraded" que deja pasar
marcando `_lock_degraded` — válido solo si hay una segunda guarda (relectura del
recurso) antes de escribir. Ver [[nodo-gcal-de-n8n-no-soporta-extendedproperties]]
