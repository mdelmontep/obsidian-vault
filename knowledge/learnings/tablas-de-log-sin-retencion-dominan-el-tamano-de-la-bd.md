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

## 2026-07-26: la retención se dimensiona contra el ritmo de escritura

Cinco semanas después, `cron_runs` había pasado de 46 MB a **169 MB (224.358
filas)** CON el sweep de retención funcionando. No estaba roto: 90 días × 42 crons
× 8.953 ejecuciones diarias son ~800.000 filas en régimen estacionario. 90 días es
un número redondo, no una decisión. Programar `purge_old_cron_runs()` (30 días,
existía desde la mig 063 sin programar) lo dejó en 224k.

Y el punto ciego mayor: **`cron.job_run_details`, la tabla que crea la propia
extensión pg_cron**, jamás se purgó — 96.114 filas, y por eso un INSERT de una
fila tardaba 199 ms. Las tablas de log que hay que vigilar no son solo las que
creas tú: también las que crea la plataforma.

Regla: elige la retención dividiendo el tamaño que aceptas entre las filas por
día, no eligiendo un redondo. Y haz inventario de las tablas de traza que NO son
tuyas.
