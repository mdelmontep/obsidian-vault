---
title: EXECUTIONS_DATA_MAX_AGE de n8n va en HORAS — un "7" deja 7 horas de historial
date: 2026-07-29
source: claude-code-session
tags: [n8n, dokploy, observabilidad, clinica-zen]
---
`EXECUTIONS_DATA_MAX_AGE` se expresa en **horas** (default oficial `336` = 14 días). Poner
`7` pensando en días deja **7 horas** de historial: el panel de ejecuciones parece normal
—hay decenas de filas— pero no existe ni una de ayer, así que un fallo recurrente es
indetectable y cualquier incidente se investiga a ciegas pasado medio día.

No da error ni aviso: el valor es válido, solo significa otra cosa.

Caso real (Clínica Zen): 44 ejecuciones retenidas, todas del mismo día. El bug estaba
**dentro del `composeFile`** del stack, no en el Environment de Dokploy — buscar solo en
`env` da "no está configurado" y lleva a añadir la variable por duplicado. Revisar los dos.

Síntoma que lo delata: `GET /api/v1/executions?limit=250` y todas las fechas del mismo día.
Ver [[camino-critico-sin-smoke-se-pudre-meses]] · [[clinica-zen]]

RECURRENCIA 2026-08-12 (Simarro): mismo síntoma exacto — 71 ejecuciones vía API,
ninguna anterior a ~6,5h. Llevó a sospechar (mal) que un workflow con cron activo
nunca había corrido; la prueba real fue el timestamp de negocio (`last_seen_at`
en Supabase), no el log de ejecuciones. No confirmado aún por SSH si es el mismo
`EXECUTIONS_DATA_MAX_AGE` mal puesto — pendiente revisar en el compose de Simarro.
