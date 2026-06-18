---
title: tablas de log/tracking sin retención crecen sin cota y dominan el tamaño de la bd
date: 2026-06-18
source: claude-code-session
tags: [supabase, postgres, performance, observabilidad, crons]
---

Al crear una tabla de tracking/audit/log (`cron_runs`, `api_request_log`,
`*_events`, `*_audit`), crear el **cron de purga en la misma tanda**. Si no,
crece sin cota y nadie lo nota hasta que es el grueso de la BD.

Caso FacturaIA 2026-06-18: `cron_runs` 46MB (90k filas) + `api_request_log`
18MB eclipsaban TODAS las tablas de negocio juntas (facturas: 424KB). Ninguna
tenía retención; sí la tenían module-events/email-bodies/chat-state.

Fix: cron `logs-retention-sweep` (>90d, `finished_at IS NOT NULL` para no tocar
runs en curso, borrado por lotes select-IDs→delete-IN con GUARD anti-DELETE-sin-
filtro). Patrón **opuesto** al de tablas de negocio: aquí el cuello no es índice
ni N+1, es retención. Ver [[auditoria-performance-priorizar-por-tamano-real-de-tabla]].
