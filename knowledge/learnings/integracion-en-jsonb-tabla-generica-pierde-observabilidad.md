---
title: integración crítica en jsonb de tabla genérica pierde observabilidad por diseño
date: 2026-05-26
source: claude-code-session
tags: [arquitectura, observabilidad, integraciones, oauth, jsonb]
---

OAuth / credenciales / estado de integración guardados en `<tabla_generica>.settings JSONB` PIERDEN observabilidad por diseño:
- Sin schema → no se valida shape.
- Sin foreign keys → no se garantiza consistencia.
- Sin `status` enum visible → cero queries del tipo "muéstrame integraciones rotas".
- Errores van a logs efímeros del cron / stdout → nadie monitoriza.

Caso real 2026-05-26 TuFacturaIA: cron OCR Gmail muerto **15 días**, nadie se enteró. Access_token expiró 11/05, refresh fallaba por `GOOGLE_CLIENT_ID/SECRET` perdidas en env Dokploy, errores en stdout del cron sin alerting.

Fix: tabla dedicada `integration_connections` con `status` enum (`active|expired|error|revoked|pending`) + `last_error/last_error_at timestamptz` + tabla de eventos persistente (`integration_events`). Cron semanal: `select * from integration_connections where status in ('error','expired') and last_error_at > now() - interval '7d'` → notifica superadmin. Imposible repetir el fallo silencioso.

Ver [[etag-por-path-upsert-stale-304]] para otro patrón "fallo silencioso por defecto invisible".
