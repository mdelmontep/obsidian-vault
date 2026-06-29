---
title: postgrest !inner join falla si no hay FK directa entre las dos tablas
date: 2026-06-30
source: claude-code-session
tags: [supabase, postgrest, queries, crons]
---

`facturas` → `org_features` no tienen FK directa (ambas referencian `organizations.id`
pero no entre sí). PostgREST no puede resolver el join `org_features!inner` desde `facturas`
→ query falla en runtime con 400, sin candidatas procesadas.

**Síntoma**: cron arranca, query lanza error, `withCronTracking` lo registra, 0 emails.

**Patrón correcto** (establecido en `cobros-reminders`, `fiscal-generar-borradores`):
1. Query `org_features` separada → obtener `orgIds`
2. `.in('org_id', orgIds)` en la query principal

**Regla**: si dos tablas no tienen FK directa, no usar `!inner` entre ellas. Siempre
verificar FK en la migración antes de escribir el join.
