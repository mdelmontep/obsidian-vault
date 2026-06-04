---
title: los crons de dokploy (docker exec) no heredan las env que la app carga de /app/.env
date: 2026-06-04
source: claude-code-session
tags: [dokploy, cron, docker, env, hmac]
---
Dokploy lanza los Scheduled Tasks de un compose con `docker exec <container> bash -c "<cmd>"`.
Ese exec SOLO ve el ENVIRONMENT del proceso del container, NO las vars que la app
(Next standalone) carga en runtime desde `/app/.env`. En TuFacturaIA: el cron veía
`FACTURAIA_SERVICE_KEY` (sí está en el environment del container) pero NO
`FACTURAIA_SIGNING_SECRET` (solo en `/app/.env`, que Next lee y el exec no) →
un script de cron que firmaba HMAC con ese secret abortaba mudo (sin fila en `cron_runs`).
Diagnóstico que funcionó: crear un cron temporal con `command='env | grep -io "FACTURAIA[A-Z_]*"; echo node=$(command -v node); echo openssl=$(command -v openssl)'`
y leer su log EN EL PANEL Dokploy (los schedules compose NO exponen logs por API,
`schedule.runManually` da 500, `deployments` viene vacío).
Hallazgos imagen `node:20-alpine`: openssl NO está; node SÍ en `/usr/local/bin/node`.
Fix: el script de cron lee el secret de `/app/.env` con node (`fs.readFileSync` + regex)
si no está en env, y firma con node (no openssl). `compose.deploy` por API NO recrea
el container (no refresca env). Ver [[supabase-rpc-security-definer-execute-public]].
