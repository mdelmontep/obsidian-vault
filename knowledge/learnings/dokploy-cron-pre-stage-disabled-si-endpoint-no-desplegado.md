---
title: cron dokploy para código aún no desplegado = crearlo enabled:false (pre-staged)
date: 2026-06-18
source: claude-code-session
tags: [dokploy, cron, deploy, facturaia]
---

Si creas un schedule Dokploy (`schedule.create`) apuntando a un endpoint `/api/internal/*` que **aún no está en el `main` desplegado** (rama sin mergear), hace **404 a diario**. Y peor: una vez la rama despliega, el endpoint entra en el `CRON_REGISTRY` y el `cron-watchdog`/`system-health-sweep` lo esperan dentro de `max_intervalo_segundos` → lo marcan en **rojo y emailean** a los superadmins si el schedule no corrió bien.

Patrón: crear el schedule con `enabled:false` (pre-staged, no dispara) y dejar el flip a `enabled:true` como paso del **deploy**, DESPUÉS de aplicar las migraciones que el endpoint necesita. Documentar el `scheduleId` en el issue/runbook de deploy.

Caso real: `mcp-dcr-cleanup` (slice 054 MCP) creado disabled mientras `feat/mcp-server` sin mergear y migs OAuth fuera de prod. Ver [[facturaia-mcp-server]], [[dokploy-schedule-sin-servicename-no-se-ejecuta]].
