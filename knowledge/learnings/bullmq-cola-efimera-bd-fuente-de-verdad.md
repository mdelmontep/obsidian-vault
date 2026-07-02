---
title: bullmq es disparador efímero, no almacén — bd fuente de verdad + reconciliación al boot
date: 2026-07-02
source: claude-code-session
tags: [bullmq, redis, scheduler, recordatorios]
---

Los delayed jobs de BullMQ viven en Redis: sobreviven a reinicios del worker, pero si Redis
cae sin persistencia se pierden (exige `maxmemory-policy noeviction` + AOF en prod). Trátalo
como **disparador efímero, no almacén durable**. El estado manda en una **tabla fuente de
verdad** (status enum + `last_error`), y al arrancar **reconcilia**: re-encola los pendientes
desde la BD (overdue → delay 0). El gate real de "ya enviado" es el `status` en BD (CAS
`scheduled→sent`), no el jobId — un job completado deja de contar como duplicado.

Gotchas:
- `jobId = <id-de-bd>` para dedup idempotente (sin `:`, no numérico puro).
- **`removeOnFail: true`**, no un número: un job fallido **retenido** ocupa el `jobId` → el
  reconciler hace `queue.add` con ese mismo id y **BullMQ lo deduplica a no-op** (jobs failed
  también dedupan) → el recordatorio nunca se re-arma. Retener = perderlo.
- Solo usar el scheduler durable (BullMQ) si el store también es durable (Postgres); durable
  sobre store in-memory = jobs que sobreviven pero apuntan a filas que ya no existen.
- Fallo transitorio (5xx/red) → rethrow para que reintente (attempts+backoff); permanente
  (sin destinatario) → marca failed sin reintentar.
