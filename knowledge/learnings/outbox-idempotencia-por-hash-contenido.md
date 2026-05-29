---
title: outbox idempotencia por hash de contenido, no por clave estructural
date: 2026-05-29
source: claude-code-session
tags: [outbox, idempotency, postgres, drive-sync]
---

`UNIQUE(org, kind, source_id) + idempotency_key='v1'` literal NO detecta cambios de contenido. Caso real Drive sync: factura anulada regenera PDF con sello ANULADA — mismo `source_id`, contenido distinto. Con clave estructural `:v1` el ON CONFLICT no re-encola → Drive queda con la versión vieja.

Fix: añadir columna `pdf_sha256` (o `content_hash` genérico). El trigger BD encola sin recalcular hash (lo hace el worker al descargar). El worker compara con el hash guardado: bit-idéntico = skip upload; distinto = `PATCH` el `drive_file_id` existente (preserva link compartido con terceros).

`ON CONFLICT DO UPDATE SET status='pending'` solo si `excluded.storage_path` cambió O `status` previo era terminal (`synced/failed/cancelled`). Si la fila estaba `processing` no la pisamos — el worker actual termina lo suyo. Ver [[outbox-trigger-bd-vs-hook-js-multiples-entry-points]].
