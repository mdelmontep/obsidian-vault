---
title: el timeout del caller debe cubrir el peor caso acumulado del retry interno del callee
date: 2026-07-09
source: claude-code-session
tags: [reliability, timeout, retry, colas]
---
Un cliente que invoca un servicio con reintentos internos y aborta con su propio
timeout debe fijarlo por encima del peor caso ACUMULADO del callee (N intentos ×
timeout_intento + backoffs), no del de un solo intento.

Gotcha: si el caller aborta antes (p.ej. 90s) que el peor caso del callee (~185s
= 3×60s + 1s+3s de backoff), un trabajo lento-pero-exitoso se contabiliza como
fallo de red. En una cola con dispatcher, la fila se re-encola y se re-reclama
mientras la 1ª ejecución sigue viva → DOBLE procesado: el estado final coincide
pero los side-effects no son idempotentes (doble upsert, doble fila de audit).

Fix: timeout_caller > Σ(peor caso callee) + margen; y guard compare-and-set
(`.eq('estado','procesando')`) en el write final para que la ejecución tardía no
pise un lifecycle ya cambiado. Mismo compare-and-set vale para cualquier
check-then-update (validar en el SELECT no basta si el UPDATE no reconfirma).
Caso real: cola OCR FacturaIA (worker 90s→200s, #805/#806). Ver
[[cron-endpoint-retirado-deja-schedule-externo-huerfano]].
