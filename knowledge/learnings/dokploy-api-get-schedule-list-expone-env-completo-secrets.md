---
name: dokploy-api-get-schedule-list-expone-env-completo-secrets
description: schedule.one/compose.one/application.one de Dokploy devuelven el compose.env COMPLETO en plano. Guardarraíl hook+wrapper monta en ~/.claude.
date: 2026-05-22
source: claude-code-session
tags: [dokploy, security, secrets, api]
---

**Gotcha**: los endpoints de lectura de Dokploy `schedule.one` / `compose.one` / `application.one` (y sus `.list`/`.all`) devuelven el `compose.env` COMPLETO del servicio padre en plano — `SUPABASE_SERVICE_ROLE_KEY`, `STRIPE_SECRET_KEY`, `META_WHATSAPP_ACCESS_TOKEN`, `WEBHOOK_SIGNING_KEY`, `*_ENCRYPTION_KEY`, passwords BD, tokens externos. Quien tiene la API key Dokploy lee TODOS los secrets. Fallo de diseño de Dokploy, no parcheable aguas arriba.

**Incidente real (2026-07-03)**: un agente llamó `compose.one` para revisar autoDeploy y volcó el env entero de `tufacturaia-app` al chat.

**Guardarraíl duro (2026-07-13, aplica a CUALQUIER Dokploy)**:
- Hook global `~/.claude/hooks/dokploy-secret-guard.sh` (PreToolUse Bash+WebFetch) BLOQUEA las llamadas crudas (`curl`/`wget`/`fetch`/`urllib`) a esos endpoints.
- Wrapper `~/.claude/bin/dokploy-safe.sh` hace la llamada y redacta el env (por nombre de campo + por patrón de valor) → devuelve solo metadata. Úsalo para leer appName/deployments/autoDeploy.
- NUNCA volcar el env real a chat/logs; si hace falta verlo, panel de Dokploy. Tratar la API key Dokploy como secret tier-1.

Runbook completo (rotación + sacar secrets del env) en repo TuFacturaIA `ops/security/README.md`. Ver [[docker-infra]] · [[op-read-secreto-nunca-en-comando-bash-ni-desde-memoria]].
