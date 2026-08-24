---
title: Elphis Psicología — HUB
date: 2026-08-24
updated: 2026-08-24
source: elphis-psicologia
tags: [cliente, agentesia, elphis-psicologia, voz, whatsapp, retell, n8n, dokploy, rgpd, agency-portal]
---

# Elphis Psicología · HUB

División de psicoterapia del grupo Elphis (O'Donnell 32, Madrid). **Proyecto DISTINTO de
[[clientes/centro-elphis/index|Centro Elphis]] (adicciones)**: no comparten CRM, agenda,
workflows ni número — solo host Dokploy y dirección. Repo `AgentesIA-MAdrid/elphis-psicologia`
(local `~/Projects/elphis-psicologia`; **arrancar las sesiones desde ahí**, no desde
`~/Projects/elphis` — la atribución de horas y las memorias van por cwd de arranque).
Bloque A (web, marca) = Borja · **Bloque B (agentes) = Manu**. Autoridad documental:
`docs/bloqueantes.md` > `docs/protocolo-crisis.md` > `PRODUCT.md` > spec de julio.

## Estado · 2026-08-24

- ✅ **Stack n8n dedicado desplegado y verificado** — Dokploy compartido, proyecto
  `elphis-psicologia`, n8n 2.36.5 + postgres + postgres-aux + redis (noeviction+AOF) en
  `n8n-psicologia.elphis.agentesialabs.com`. Los 8 gates del README pasados; purga diaria
  de retención probada 2 veces con el scheduler real. Esquema cerrado a propósito
  (3 tablas, sin texto libre: todo lo que entra es dato art. 9). IDs y detalle en la
  memoria del proyecto y en `infra/README-deploy.md`.
- ✅ **Adaptador de agenda (GCal) desplegado y activo** — `psico-agenda-*`: check/book/
  cancel/reschedule + test-runner. Horario L-V 10-21 (sábado NO confirmado por Alba →
  cerrado), 50 min default / 60 pareja, antelación 24 h, `service_slug` cerrado sin
  `motivo` libre. Idempotencia doble: Redis INCR/TTL + `bookingKey` en
  `extendedProperties.private` releído antes de crear. Si GCal no responde → error
  honesto, nunca inventa huecos. Contrato completo: `infra/README-agenda.md`.
  → [[nodo-gcal-de-n8n-no-soporta-extendedproperties]] ·
  [[lock-e-idempotencia-en-n8n-con-redis-incr-sin-set-nx]] ·
  [[parse-roto-de-una-respuesta-200-se-confunde-con-fallo-y-duplica]]
- ✅ **Chatwoot**: cuenta «Elphis Psicología» id 4 en la instancia compartida (estanca).
  Inbox API pendiente de los puentes.
- ⏳ **OAuth Google pendiente (bloquea la E2E de agenda)** — redirect URI añadido y
  «Connect my account» hecho el 24/08, pero **la credencial sigue sin token**:
  `agenda-e2e.sh` da 1/12 (resto cascada del mismo fallo) con
  `GCAL_ERROR: Unable to sign without access token` en el escenario 1. El Connect no
  cuajó — revisar si el popup se cerró antes de completar el flujo o si el client
  sigue en modo Testing (token a 7 días) antes de reintentar.
- ⚠️ **`~/Projects/elphis` (carpeta suelta, sin `.git`) sigue viva y ya mordió una vez**:
  atribuyó a `project=elphis` cuatro bloques de trabajo real de esta división (22 y
  24/08, sesión `4cf61623-…`) en `agency-portal`. Reatribuidos a mano el 24/08
  (`UPDATE work_sessions` vía SSH al self-hosted de agency-portal). Mientras la carpeta
  exista, cualquier sesión arrancada ahí por costumbre repite el fallo — renombrarla o
  borrarla lo cierra de raíz en vez de solo avisarlo en prosa.
- 🔴 **Wasabi 403 host-wide** (escalado a Borja): los Volume Backups de TODO el host
  fallan la subida ≥11 días — afecta también a Adicciones y Chatwoot. Se arregla en
  panel → Settings → S3 Destinations.

## Próximo (orden del bloque B)

3. KB Supabase (RAG pgvector — NUNCA en el Postgres self-hosted). 4-5. WhatsApp y voz
Retell (esperan número virgen + DPA). 6. Crisis + simulation tests (**no transfiere
nunca**: 024/112 + correo — lo CONTRARIO de Adicciones). 7. Notificaciones.
Plantillas Meta a aprobación el día 1 que exista la WABA.

## Bloqueos (terceros)

- Borja: write al repo para `mdelmontep` (3 commits locales sin pushear) · Wasabi ·
  decidir `.agentesia.madrid` ANTES de registrar webhooks · número + DPA · móvil real
  de avisos (el 659 877 708 NO vale: emisor de la WABA de Adicciones).
- Manu: corregir password del ítem 1P «Elphis Psicologia» (no valida contra n8n) + OAuth.
