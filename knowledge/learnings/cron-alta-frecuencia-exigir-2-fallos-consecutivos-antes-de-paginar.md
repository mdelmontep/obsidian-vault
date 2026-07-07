---
title: cron de alta frecuencia — exigir ≥2 fallos consecutivos antes de paginar por email
date: 2026-07-07
source: claude-code-session
tags: [monitoring, cron, alerting, facturaia]
---
Los crons de alta frecuencia (dispatchers cada minuto, enrich cada 10 min) son
workers de cola auto-sanables: un blip transitorio de infra (Cloudflare/Supabase
520/522 que tumba UNA llamada, o un run colgado que el watchdog reapea como
zombie ~20 min) hace fallar UN run y el siguiente se recupera solo. Si la salud
pagina ALTA (email) ante UNA sola observación mala —un run `error`, o un `running`
colgado más que su intervalo— cada microcaída de infra genera correo → fatiga de
alertas → el día que falle algo real se ignora.
Patrón durable: exigir **≥2 fallos terminados CONSECUTIVOS** antes de dar
'rojo'/email. 1 fallo suelto rodeado de éxitos → 'ambar' (panel, sin email).
`zombie` cuenta como fallo. Un cron que DEJA de dispararse (último éxito más viejo
que su intervalo) sigue paginando al instante: esa detección NO depende de la racha.
3ª palanca del mismo tema, complementa
[[cron-mantenimiento-auto-sanable-no-debe-paginar-severidad-por-criticidad]]
(criticidad) y [[watchdog-umbral-debe-tolerar-un-tick-perdido]] (umbral).
Fix FacturaIA PR #790: `CONSECUTIVE_FAIL_THRESHOLD=2` en `computeHealth` + `limit(4)`.
