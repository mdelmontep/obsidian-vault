---
title: observabilidad nueva destapa bugs viejos en silencio
date: 2026-05-11
source: claude-code-session
tags: [observability, crons, monitoring, debug]
---

Al añadir tracking/logging/cron_runs/audit table a infra existente, esperar destapar fallos preexistentes (envs vacías, edge cases nunca probados, rate-limits ignorados, retries silenciados). El primer run te enseña qué llevaba meses fallando.

**Reacción correcta**: documentar como "preexistente, no regresión introducida por el tracking". No panic, no rollback de la observabilidad — al contrario, ese es justo su valor.

**Caso real FacturaIA**: tras crear tabla `cron_runs` y wrappear el cron `storage-quota-check` con `withCronTracking`, el primer run capturó error `"invalid warn_mb"`. Causa: env `STORAGE_QUOTA_WARN_MB=""` en Dokploy → `Number("") = 0` → guard `<=0` lanzaba. El cron fallaba cada semana en silencio hace meses, nadie lo había visto. Fix: helper `parseMb` con fallback null/empty/non-numeric → cae al default 500 limpio.

**Patrón**: cuando habilites tracking nuevo, dedica el primer ciclo a clasificar lo que sale como "preexistente" vs "nuevo". Filtra falsos positivos del propio tracking antes de declarar bugs.
