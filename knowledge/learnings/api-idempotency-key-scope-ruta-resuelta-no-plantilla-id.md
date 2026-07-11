---
title: idempotency-key de una API debe escoparse a la ruta resuelta, no a la plantilla del endpoint
date: 2026-07-11
source: claude-code-session
tags: [api, idempotency, next, multi-tenant]
---

Un handler compartido deduplicaba idempotencia por `(org, endpoint_label, key) + hash(body)`. `endpoint_label` era la **plantilla** con `[id]` literal (ej. `POST /v1/facturas/[id]/duplicar`), idéntica para todos los recursos. Como el hash solo cubre el body, reusar una `Idempotency-Key` en dos recursos distintos del mismo endpoint con el mismo body (típico: acciones de body vacío — duplicar, marcar-cobrada) caía en la rama `completed`+mismo-hash → **replay del primer recurso; el segundo nunca se ejecuta**. Fallo silencioso (200 + `Idempotent-Replay: true`).

**Fix**: escopar la dedup a la ruta RESUELTA (fingerprint estilo Stripe = método+path+body): `const idemScope = \`${endpoint} ${new URL(req.url).pathname}\``. Endpoints de colección (mismo pathname para todos, ej. `POST /v1/facturas`) no cambian. `org` sigue siendo la 1ª componente → aislamiento intacto.

**Gotcha**: `hash(body)` NO discrimina recursos en rutas `[id]`; el path resuelto es el discriminante que falta. La etiqueta del endpoint sirve para logging/audit, no como scope de idempotencia.

Caso real: FacturaIA #833 — afectaba a 16 endpoints `/api/v1/*/[id]/*`. Ver [[outbox-idempotencia-por-hash-contenido]] · [[nulls-not-distinct-idempotencia-con-discriminador-opcional]].
