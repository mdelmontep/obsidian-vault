---
title: ADR-025 — Drive sync de PDFs facturas usa outbox + worker, no fire-and-forget post-response
date: 2026-05-29
status: accepted
tags: [adr, facturaia, drive-sync, integraciones, outbox]
---

## Contexto
Tras cut-over OCR a plataforma integraciones (mig 170), tocaba cablear el envío de PDFs facturas al Drive del cliente. Cliente Drive scope `drive.file` ya en el OAuth. La pregunta: ¿upload síncrono en `createDocument`, fire-and-forget async, o outbox + worker?

## Opciones consideradas
- **A — Fire-and-forget post-response en `createDocument`**: `void uploadToDrive(...).catch(log)`. Cero infra. Pero en Next.js 16 + Dokploy serverful, la promesa post-response NO tiene garantía de completarse (container recycling, OOM, deploy). Sin observabilidad: "¿qué facturas NO están en Drive?" inrespondible. Sin backfill: script ad-hoc separado.
- **B — Outbox + worker async con triggers BD** (este PR #85): tabla `drive_sync_queue` + trigger `AFTER UPDATE OF documento_url` encola atómico con la transacción + RPC `SELECT FOR UPDATE SKIP LOCKED` + worker con backoff exponencial. ~500 LOC + 1 mig + 1 cron. Observable, retriable, idempotente, backfill trivial.
- **C — Manual desde UI (botón "Subir a Drive")**: regresión producto. Holded/Quaderno lo hacen automático. Descartado.

## Decisión
**B**, porque (1) los 8 puntos de entrada que mutan `documento_url` se cubren con UN trigger BD (atómico, imposible saltarse — un hook JS perdería las recibidas vía Gmail/iCloud/WhatsApp); (2) el backfill histórico futuro reutiliza la misma cola sin código nuevo; (3) cascade revoke + token expired + retry exponencial son comportamientos que SOLO un worker async puede modelar correctamente.

## Consecuencias
- Compromiso: cualquier integración nueva tipo "subir documento a cloud X" usa este patrón (OneDrive, Dropbox copy/paste). Tabla genérica si crece a 2+ providers.
- Cerramos opción "hook simple en `createDocument`" como atajo futuro — solo cubre el 12% de entry points reales.
- Dependencia operativa nueva: cron 1/min hitting `/api/internal/drive-sync-dispatcher`. Watchdog si falla 5 min consecutivos (notificación admin vía `withCronTracking`).
- Ver [[outbox-trigger-bd-vs-hook-js-multiples-entry-points]], [[outbox-idempotencia-por-hash-contenido]], [[select-for-update-skip-locked-via-rpc-security-definer]], [[oauth-cascade-revoke-por-external-id-multi-org]], spec [[facturaia-drive-sync-architecture]].
