---
title: EcoBox HUB
date: 2026-05-22
tags: [cliente, ecobox, hub]
---

# EcoBox 360 — HUB

Cliente AgentesIA · Taller de chapa y pintura + mecánica rápida · Las Rozas (Madrid). Onboarding 2026-05-20, despliegue 21-22.

## Identidad

- **Razón social**: ECOBOX 360 S.L · CIF B27609114
- **Domicilio**: Calle Rotterdam 3, 28232 Las Rozas (Madrid)
- **Contacto**: Cristian Sánchez Alonso — cristian@ecobox360.es
- **Web**: www.ecobox360.es
- **WhatsApp actual (app móvil personal)**: +34 636 521 315 (NO migrar — se queda con Cristian)
- **Slug interno**: `ecobox`

## Stack final desplegado

| Pieza | Detalle |
|---|---|
| Dokploy dedicado | `https://ecobox.agentesialabs.com` · server Stackscale `185.99.186.132:5251` (admin: técnico ajeno) |
| n8n self-hosted | `https://n8necobox.agentesialabs.com` · stack postgres17 + redis7 + n8nio/n8n:2.18.7 |
| Retell agent voz | `agent_250ae0d683b8086fdcaaed9027` — Alex — gpt-4.1 cascading sin high_priority, **Rigid Mode** ([[ADR-013-retell-conversation-flow-rigid-vs-flex-mode]]) |
| Retell Conversation Flow | `conversation_flow_5f455ab09cf4` — 13 nodos, 4 tools custom (Mirar_disponibilidad, Reservar_cita, Buscar_reserva, Cancelar_cita) |
| Retell KB | `knowledge_base_34f85cf8295d3369` — 11 chunks info taller |
| Chatwoot inbox | **compartido** AgentesIA `https://chatwoot.agentesia.madrid` acct=1 ([[ADR-012-ecobox-sin-crm-vs-chatwoot-vs-kommo]]). Bot `ChatBOT EcoBox` id=2 |
| Pipeline | 5 labels `ecobox-{nuevo,cita-agendada,peritaje-hecho,entregado,cancelado}` |
| Custom attrs | 14 conversation-scoped con prefijo `ecobox_*` (matrícula DEDUPE KEY, marca, daño, seguro, sustitución, recogida, fecha cita, gcal_event_id…). `ecobox_drive_folder` borrado 2026-05-22 — no aplica al flujo final |
| WhatsApp Cloud | **pendiente número + WABA** en portfolio EcoBox `1011127821491282` |
| Email SMTP | placeholder `notificaciones@ecobox360.es` — pendiente app-password |
| 1Password vault | "EcoBox" en agentesialab — 9 items con todas las creds |

## Workflows n8n desplegados

| WF | ID | Estado |
|---|---|---|
| Chatwoot Bot Alex | `lv7pee2XAU5OngOB` | **ACTIVO** (v1 sin tools n8n aún) |
| Mirar_disponibilidad | `iO9m2aSifPYY9LuA` | inactivo · necesita GCal OAuth |
| Reservar_cita | `bJwoFHSBO6BK7gUe` | inactivo · idempotency Redis + Calendar event_id sha1 ([[calendar-event-id-deterministico-sha1-phone-slot-anti-doble-booking]]) + envía emails cliente+Cristian + **append Google Sheet `EcoBox - Leads`** (log universal voz+chat) |
| Buscar_reserva | `HHryz8eDv3GOxZMF` | inactivo |
| Cancelar_cita | `L2W64JNIQmd0IJLV` | inactivo |
| Recordatorios cron 48h+24h | `QVPf25PZyLv0UHII` | inactivo · pendiente decisión cliente (sólo confirmación + alert por ahora) |
| Meta token health check | `Jbf5rZepHYM21MPQ` | inactivo · email alert a Cristian si falla |
| TEST Email Templates | `DogJ9b1iOHmJeS2S` | activo · webhook `/test-email-templates` |

## Pipeline conversacional Alex (voz + chat)

```
START → Welcome → Extract DV (intent) → Branch classifier
    ├─ nueva_cita → SUBAGENT recoger datos (nombre, daño, coche, matrícula,
    │              email-solo-chat, seguro, sustitución, recogida, día) → Reservar_cita
    ├─ gestionar_cita → SUBAGENT Buscar_reserva + Cancelar_cita
    ├─ info_rapida → consulta KB + bucle a classifier
    └─ humano / idioma raro → transfer_call (voz) o label `humano` (chat)
```

## Decisiones clave

- [[ADR-012-ecobox-sin-crm-vs-chatwoot-vs-kommo]] — Chatwoot compartido vs Kommo vs NocoDB
- [[ADR-013-retell-conversation-flow-rigid-vs-flex-mode]] — Rigid €0.135/min vs Flex €0.20-0.35
- **Notificaciones** = nativas Chatwoot (no Telegram). Cristian instala app móvil → push handoff + asignación.
- **Email pedido SÓLO en chatbot** (no voz). Si no hay email → solo email a Cristian.
- **Plantillas email**: 2 únicamente (confirmación cliente + alert Cristian). Resto descartado.
- **Recordatorios HSM 48h/24h**: descartados por cliente (workflow desplegado pero inactivo).

## Pendientes externos (Cristian)

1. Comprar número telefónico provider AgentesIA habitual
2. Crear WABA en portfolio `1011127821491282` + registrar número + generar Permanent Access Token Meta
3. Crear plantilla HSM `confirmacion_cita` (categoría **Utility**, no Marketing — ahorra 7×)
4. Crear Google Calendar dedicado "EcoBox - Peritajes" + Google Sheet "EcoBox - Leads" (importar `ecobox_leads_template.csv` con 17 columnas). Compartir ambos con cuenta OAuth n8n
5. App-password Gmail `notificaciones@ecobox360.es` para SMTP
6. Logo PNG público + color marca hex confirmados (defaults `#0F1B2D` + `#E76F51`)
7. URL Google Maps corta de Rotterdam 3

## Pendientes técnicos (Manu)

- OAuth Google en n8n UI (requiere browser consent) — gotcha: [[n8n-public-api-google-oauth-schema-buggy-crear-en-ui]]
- SMTP funcional ya para probar plantillas email (gmail Manu app-password como test temporal)
- Crear agente Cristian en Chatwoot

## Cuando llegue todo (yo, ~30 min)

1. Reemplazar sentinels en workflows: `GCAL_ID` (de `primary` a real), `PHONE_NUMBER_ID`
2. Editar cred `Meta WhatsApp Bearer` con permanent token real
3. Crear inbox WhatsApp EcoBox en Chatwoot + asociar bot id=2
4. Activar los 6 workflows inactivos
5. Smoke tests E2E llamada Retell + WhatsApp

## Archivos locales

- `/Users/manueldelmonte/Ecobox/CLAUDE.md` — estado completo + decisiones
- `/Users/manueldelmonte/Ecobox/ARQUITECTURA.md` — diseño Chatwoot
- `/Users/manueldelmonte/Ecobox/CHECKLIST_ARRANQUE.md` — 14 pasos para conectar
- `/Users/manueldelmonte/Ecobox/email_templates.md` — diseño 2 plantillas (cliente + Cristian)
- `/Users/manueldelmonte/Ecobox/email_previews/` — HTMLs navegables
- `/Users/manueldelmonte/Ecobox/whatsapp_templates.md` — sintaxis Meta `{{1}}{{2}}{{3}}`
- `/Users/manueldelmonte/Ecobox/.credentials.local` — IDs y tokens (NO commitear)

## Learnings de esta sesión

- [[retell-conversation-flow-flex-vs-rigid-coste-token-scaling]]
- [[retell-tools-conversation-flow-require-tool-id-field]]
- [[retell-knowledge-base-api-requiere-multipart-form-data]]
- [[chatwoot-custom-attribute-definitions-endpoint-v3-renombrado]]
- [[chatwoot-bot-token-vs-admin-token-scopes-distintos]]
- [[n8n-network-external-true-falla-en-dokploy-sin-pre-create]]
- [[n8n-postgres-webhook-lastnode-solo-devuelve-primer-row]]
- [[n8n-public-api-google-oauth-schema-buggy-crear-en-ui]]
- [[calendar-event-id-deterministico-sha1-phone-slot-anti-doble-booking]]
