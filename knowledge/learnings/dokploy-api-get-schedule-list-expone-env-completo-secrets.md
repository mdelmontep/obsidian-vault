---
name: dokploy-api-get-schedule-list-expone-env-completo-secrets
description: GET /api/schedule.list devuelve compose.env COMPLETO con todos los secrets en plano. API key Dokploy = acceso a todos los secrets.
date: 2026-05-22
source: claude-code-session
tags: [dokploy, security, secrets, api]
---

**Gotcha**: el endpoint `GET https://<dokploy>/api/schedule.list?id=COMPOSE_ID&scheduleType=compose` devuelve para cada schedule una estructura que incluye `compose: { env: "VAR1=...\nVAR2=..." }` con el **bloque environment COMPLETO** del compose padre — secrets en plano. Aparecen `SUPABASE_SERVICE_ROLE_KEY`, `STRIPE_SECRET_KEY`, `META_WHATSAPP_ACCESS_TOKEN`, `WEBHOOK_SIGNING_KEY`, `*_ENCRYPTION_KEY`, passwords BD, tokens externos, etc.

**Implicación**: quien tenga la **API key Dokploy** tiene acceso de lectura a **todos los secrets de todos los servicios** del compose. La key NO necesita permiso especial para listar schedules.

**Mitigaciones**:
- Tratar la API key Dokploy como secret tier-1 (mismo nivel que SUPABASE_SERVICE_ROLE_KEY).
- Restringir IP origin del panel Dokploy si la infra lo soporta.
- Rotar API key cada 3-6 meses (Settings → Profile → API Keys → regenerar).
- Si compartes la key con un agente externo, asumir que vio TODOS los secrets — no es leak técnico, es comportamiento del endpoint.
- Auditar quién tiene la key (humanos + agentes + integraciones).

Aplicable a cualquier Dokploy production multi-secret. Otros endpoints tRPC `*.one`/`*.list` probablemente expongan misma estructura.
