---
title: un anti-replay que lanza convierte el webhook en 500 y provoca los reintentos que evitaba
date: 2026-07-31
source: claude-code-session
tags: [webhooks, idempotencia, meta, resiliencia]
---
Al añadir anti-replay a un receptor de webhooks (candado por `message.id` contra una
PK), la primera versión **lanzaba** si la tabla no respondía — por ejemplo porque la
migración aún no estaba aplicada. Ese `throw` sube hasta el handler y devuelve **500**,
que es exactamente lo que hace a Meta (y a Stripe, y a cualquier emisor con reintentos)
**reintentar en bucle**: el guard contra duplicados los habría multiplicado.

Regla: el candado va **fail-open** ante cualquier fallo que no sea la violación de
unicidad (`23505`), y el `try/catch` cubre TAMBIÉN las excepciones, no solo el `error`
devuelto por el cliente. Procesar dos veces un mensaje es malo; dejar de atender a
todos los clientes mientras dura una incidencia de BD es peor. Loguear el modo
degradado para que no sea silencioso.

Corolario de método: lo detectaron 55 tests hermanos poniéndose rojos, no una revisión.
Un cambio en un handler compartido se valida corriendo la suite del módulo entero, no
solo los tests nuevos.

Caso real: FacturaIA `qa-028`, PR #1404 (receptor de Meta, mig 600).
