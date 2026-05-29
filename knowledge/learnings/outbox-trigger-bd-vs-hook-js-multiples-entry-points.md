---
title: outbox para columna mutada por múltiples puntos → trigger BD, no hook JS
date: 2026-05-29
source: claude-code-session
tags: [outbox, postgres, triggers, integraciones, drive-sync]
---

Cuando una columna se muta desde N puntos del código (en TuFacturaIA Drive sync: 8 — `createDocument`, `emitir-borrador`, `render-and-upload`, `update-presupuesto`, `process-attachments`, `/api/upload`, `whatsapp/ingesta`, `anular`), un hook JS en uno solo PIERDE el resto. Caso real: hook en `createDocument` habría perdido las recibidas que entran vía Gmail/iCloud/WhatsApp.

Patrón correcto: `AFTER UPDATE OF columna ON tabla` `SECURITY DEFINER` que encola en la tabla outbox. Atómico con la transacción del UPDATE, imposible saltarse. Función helper hace JOIN a tablas relacionadas (clientes/proveedores) para popular metadata necesaria. Fallback graceful: si helper falla, no bloquea el UPDATE original.

Trigger se aplica una vez en migración. Cero mantenimiento por cada nuevo caller. Ver [[select-for-update-skip-locked-via-rpc-security-definer]] para race protection del worker, [[outbox-idempotencia-por-hash-contenido]] para detectar regeneraciones.
