---
title: umbral de watchdog de cron debe tolerar ≥1 tick perdido (2× intervalo)
date: 2026-06-19
source: claude-code-session
tags: [monitoring, cron, dokploy, facturaia]
---
Un watchdog que marca "cron caído" si el último run supera ~1× su intervalo
da FALSO POSITIVO en cuanto el scheduler se salta un solo tick — algo normal
en deploys o jitter de host. Si el cron está programado en `:30` y el
scheduler pierde ese tick, su siguiente run es 1 intervalo después → el hueco
duplica el intervalo y cruza el umbral.
Regla: `max_intervalo` = 2 × intervalo + buffer. Así un tick perdido nunca
alarma; solo salta ante ≥2 fallos consecutivos (parada real).
Caso TuFacturaIA 2026-06-19: 3 emails ALTA "Cron en fallo" falsos (bot-error
-backfill, ingesta/email zombie-sweep) con todos los runs `success`; el
scheduler de Dokploy perdió el tick 02:30 UTC. Fix #393 (registry.ts).
El `scheduler-heartbeat` ya aplicaba este principio (tolera 10× sobre 1 min).
RECURRENCIA 2026-07-04: el fix #393 no cubrió `mcp-dcr-cleanup` (quedó a 36h,
<2×24h) → volvió a paginar en falso. Tunear umbral por-cron es frágil; el
patrón robusto es clasificar por criticidad → mantenimiento auto-sanable no
paginua. Ver [[cron-mantenimiento-auto-sanable-no-debe-paginar-severidad-por-criticidad]].
Ver [[dokploy-schedule-step-expression-no-catch-up-tras-caida]].
RECURRENCIA 2026-08-12 (Simarro, 3ª vez): watchdog nuevo (con cooldown, creado
anoche) con umbral 8h sobre un sync que solo corre 1×/día (24h) → avisaba en
Slack cada tarde sin nada roto; el dato real (`last_seen_at`) coincidía al
segundo con la hora del cron, el sync SÍ corría a tiempo. Aquí NO aplica 2×
intervalo (48h deja 2 días de catálogo obsoleto sin avisar en un dato de
cara al cliente) — el margen correcto depende de CRITICIDAD, no de un
multiplicador fijo. Subido a 26h (cadencia+margen corto).
