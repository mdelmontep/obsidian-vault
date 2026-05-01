---
title: webhook idempotency — borrar log en errores transitorios para reintento limpio
date: 2026-05-01
source: claude-code-session
tags: [webhooks, idempotency, integraciones, agency-portal, facturaia]
---

Receivers idempotentes loguean `event_id` antes de procesar para deduplicar. Si el handler falla con error transitorio (5xx upstream, timeout, red, lock contención), el log queda y el siguiente retry se trata como replay falso → evento perdido para siempre.

Patrón Stripe:
- 4xx (validación, FK violation, payload malo): mantener log → retry no reintenta nada nuevo
- 5xx / network / pgsql `serialization_failure`: **DELETE el log** antes de devolver error → retry reentra limpio

Implementación: try/catch alrededor del handler; en catch clasificar (status code, código pgsql) y `await sb.from('webhook_events').delete().eq('event_id', id)` solo en transitorios.

Bug real: agency-portal `/api/webhooks/facturaia` insertaba event_id antes del switch — fallo de FK por race con sync paralelo dejaba el evento muerto. Fix aplicado en audit de PRs P1-P7.
