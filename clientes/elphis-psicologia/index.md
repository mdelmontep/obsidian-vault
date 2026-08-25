---
title: Elphis Psicología — HUB
date: 2026-08-24
updated: 2026-08-25
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
  **`service_slug` realineado con la web el 25/08** (`adultos|adolescentes|pareja|
  sin-decidir` — el whitelist del nodo divergía del repo y habría rechazado toda
  reserva real): parche en prod vía API + comentario de procedencia en el nodo +
  `CHECK` en `crm_events` (mig `02-service-slug-check.sql`, **pendiente de aplicar
  a mano**). → [[un-consumidor-del-shape-puede-vivir-fuera-del-repo]] ·
  [[nodo-gcal-de-n8n-no-soporta-extendedproperties]] ·
  [[lock-e-idempotencia-en-n8n-con-redis-incr-sin-set-nx]] ·
  [[parse-roto-de-una-respuesta-200-se-confunde-con-fallo-y-duplica]]
- ✅ **PR #30 abierto vía fork (25/08)** — `mdelmontep` sigue solo-lectura en el repo
  (y `mdelmonteagentesia` sin acceso a la org), pero el repo permite fork: rama
  `agenda-service-slug-fix` en `mdelmontep/elphis-psicologia` → PR contra `main` con
  los 6 commits de infra+agenda. Entregar ya no espera al write; falta el merge de Borja.
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

## Próximo (plan del bloque B CERRADO el 25/08, prompt de continuación entregado)

Orden: 0a OAuth (12/12) · 0b confirmaciones · 1 webhook del formulario (§4 bis) · 2 KB ·
3 WABA + plantillas · 4 WhatsApp · 5 voz Retell · 6 crisis E2E real · 7 notificaciones.
**Decisiones tomadas** (el ejecutor las registra en `docs/bloqueantes.md`): KB **inline
desde el repo, sin pgvector** hasta que exista el blog (corpus ~15 docs, divergencia
razonada del spec) · voz = **Retell prompt único**, no conversation flow (apéndice B.1:
en flows la crisis solo alcanza los nodos con arista) · honeypot = campo `website` ·
LLM = Claude API con DPA/zero-retention, sub-encargados (Anthropic, Retell) flageados a
Borja/legal. Crisis: **no transfiere nunca**, 024/112 + correo — lo CONTRARIO de
Adicciones. Guiones VERBATIM del protocolo v1; cambiar una palabra = v2 + re-OK de Alba.

## Bloqueos (terceros)

- Borja: **merge del PR #30** · write al repo (ya no bloquea entregar: hay fork) · Wasabi ·
  decidir `.agentesia.madrid` ANTES de registrar webhooks · DPA · móvil real
  de avisos (el 659 877 708 NO vale: emisor de la WABA de Adicciones).
- Manu (bloquean la WABA y el paso 3): ① confirmar que el +34 910 059 223 está **virgen**
  ② proveedor/SIP del número ③ quién recibe el OTP de Cloud API ④ credenciales SMTP de
  `info@elphispsicologia.com` · password del ítem 1P «Elphis Psicologia» · Connect OAuth.
