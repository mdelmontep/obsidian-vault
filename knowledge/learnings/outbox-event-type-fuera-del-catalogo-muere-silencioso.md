---
title: outbox — un event-type fuera del catálogo suscribible muere en silencio
date: 2026-06-27
source: claude-code-session
tags: [webhooks, outbox, postgres, testing]
---
En un bus outbox+suscripción (trigger BD → `enqueue_outbox_event` → fan-out a endpoints suscritos), si un trigger emite un `event_type` que NO está en el catálogo suscribible (el enum TS del que la UI deriva los checkboxes), el evento se encola pero **ningún endpoint puede suscribirse** → se marca `fanout_completed` sin crear delivery → **muere silencioso**: ni error, ni log, nadie se entera.

Caso real FacturaIA: mig 035 emitía `presupuesto.convertido`/`rechazado`, ausentes de `WEBHOOK_EVENT_TYPES` → no entregables durante meses.

Guard barato y duradero: **test-contrato emisor ⊆ catálogo**. Escanea los `.sql` de migraciones, extrae todo `enqueue_outbox_event(_, 'X.Y'` (+ el patrón indirecto `v_event := '...'`) y asegura que cada uno está en el enum. Caza el desajuste al añadir triggers nuevos, sin lista hardcodeada que mantener.
