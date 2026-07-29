---
title: si algo se puede reintentar, el callback del intento viejo cerrará lo que ya se reabrió
date: 2026-07-29
source: claude-code-session
tags: [webhooks, idempotencia, reintentos, facturaia]
---

Al añadir "reabrir y reintentar" a un flujo, el callback del intento ANTERIOR sigue vivo
y llegará tarde: actuará sobre un estado que ya no es el que él dejó.

Caso TuFacturaIA: mergear el PR del runner cierra el ticket y manda el email de resolución
al cliente (`github-webhook`). Con la reapertura, el PR viejo seguía abierto —el propio
diálogo invita a cerrarlo— así que mergearlo cerraba el ticket recién reabierto y le decía
al cliente "ya está resuelto" por el arreglo que él acababa de decir que no le valía.

La guarda de idempotencia existente NO cubre esto: era `if (estado === 'resuelto') return`,
y lo que define el caso es que el ticket ya NO está resuelto. Idempotencia ("no lo hagas
dos veces") y vigencia ("¿sigues siendo el intento actual?") son cosas distintas.

Fix: el callback comprueba que su propio intento sigue siendo el último de la entidad
(`getLatestAiJob(ticket) !== job.id` → `ignored: 'pr_obsoleto'`). Barato y explícito en la
respuesta, para que el ignorado se vea en el log en vez de parecer un no-op.

Buscar el mismo agujero en todo callback externo de algo reintentable: pasarela de pago,
webhook de firma, resultado de OCR relanzado.
Ver [[idempotencia-de-entidad-no-debe-gatear-notificacion-side-effect]]
