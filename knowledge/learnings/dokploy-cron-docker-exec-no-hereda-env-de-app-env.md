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

ADENDA (migración crons HMAC v2): un cron cuyo command legacy mandaba `-d '{}'`
(cosmético — el legacy x-service-key NO firma el body) falla con 401 bad_signature
al migrar a firma v2 si firmas sha256('{}'): el endpoint pasa body vacío a
requireServiceAuth. Fix: migrar SIN body (firma sha256('')). Validar cada cron
con body por separado al migrar. Crons inocuos (purgas/sweeps) ejecutables
manualmente vía firma para validar; los de notificación (cobros-reminders,
*-alerts, fiscal-avisos) NO dispararlos a mano (envían a clientes) — validar en ciclo.

ADENDA 2 (auditoría post-migración): al migrar crons a HMAC v2 (`sign-call.sh`) NO asumir
que TODOS los endpoints `/api/internal/*` usan `requireServiceAuth`. `verifactu/process`
tiene authCheck CUSTOM (`x-service-key === SUPABASE_SERVICE_ROLE_KEY`, no la firma ni el
FACTURAIA_SERVICE_KEY normal). Migrar su cron a sign-call.sh (firma v2) lo dejó dando 401
(estaba disabled, no rompió). Verificar el authCheck del endpoint ANTES de migrar su cron.

ADENDA 3 (2026-07-03, SE REPITIÓ): mismo error exacto, mismo endpoint, dos meses después,
en otra sesión — al re-habilitar `verifactu-process` (deshabilitado desde mayo) lo
"moderni­cé" a sign-call.sh sin releer esta nota antes → 401 en bucle + 40 min persiguiendo
env stale/`compose.deploy` antes de volver al mismo sitio. Check mecánico obligatorio antes
de tocar CUALQUIER cron: `grep -A15 "withCronTracking(" route.ts` y mirar si el 2º argumento
trae `auth:` propio — si lo tiene, el comando NO cambia aunque el resto use HMAC v2.
