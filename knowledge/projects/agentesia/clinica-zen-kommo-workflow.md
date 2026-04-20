---
title: clinica zen - workflow kommo + n8n
date: 2026-04-17
source: claude-code-session
tags: [clinica-zen, kommo, n8n, workflow]
---

## Infraestructura

- **Servidor**: `185.47.13.168`
- **n8n**: `n8nclinicazen.agentesia.madrid`
- **Cuenta Kommo**: `citasclinicazenes.kommo.com`
- **Account ID**: 36308863
- **amojo_id**: `a72ef68d-df26-4110-ac87-c53f1c54120c`

## Workflow principal

- **ID**: `u0AQPe9pxN79dbFa` — "Chatbot clinica zen"
- **Origen**: copiado de gonzaloautomatizaciones, adaptado
- **Webhook**: `POST /webhook/clinica_zen` (evento `add_message`)
- **AI Agent**: GPT-5.1
- **Envío de mensajes**: 12 nodos HTTP Request a `amojo.kommo.com/v1/chats/{amojo_id}/{chat_id}/messages`

## Sub-workflows

| ID | Nombre | Tool en el agente |
|---|---|---|
| `RN0wl8RaRmwLpnfQ` | Leads entrantes | Reservar_cita |
| `DkueIeGFWLKh8nTj` | Leads cambio de fecha o anulacion | Cancelar_cita |
| `15bh3GWag2IgwLe8` | Derivacion Humano | Derivar_agente |
| `s3q2LceTDBvohSIx` | Buscar_base_de_datos | Buscar_base_de_datos |

## Workflows auxiliares

| ID | Nombre | Trigger |
|---|---|---|
| `qBUnBCRxKJEOJGFv` | Especialista Asignado | Webhook Kommo `status_lead` (id 47214819) |

## Credenciales n8n

| ID | Tipo | Uso |
|---|---|---|
| `eBH0xTDDB5zBjyii` | OAuth2 | Kommo API (sin scope Chats) |
| `HidiDidMl2JAsQur` | Header Auth | amojo_token manual (`X-Auth-Token`) |
| `07Vlog8HTbvwxKvu` | Kommo Long Lived Token | API REST Kommo |
| `9JQVVnT0EPH9hFg6` | OpenAI | GPT-5.1 |
| `H1wn4lZvjovP24lt` | Redis | Cache |
| `NPRK6H9eslShVGuk` | Postgres | Memoria chat |
| `FuL6BvRXqQ4JJO47` | Supabase | Vector store RAG |
| `evGPhnDHcPZ2fW7V` | Google Calendar | Citas |

## Estado actual (2026-04-20)

- **Funcional**: recibe mensajes y responde vía amojo API v1
- **Prompt**: versión 7 — confirmación con día de semana + STOP antes de Reservar_cita + regla anti-invención disponibilidad
- **Error handling**: 4 toolWorkflow nodes con `onError: continueErrorOutput` (antes: stopWorkflow)
- **Emails**: todos apuntan a `citas@clinicazen.es` (antes: `info@hiflymadrid.com`)
- **Status IDs**: todos migrados de gonzalo a CZ
- **Problema**: amojo_token expira cada ~24h, hay que actualizarlo manualmente en la credencial Header Auth
- **Pendiente**: soporte Kommo habilite scope "Chats" → aplicar patrón Laserys (token dinámico) + typing entre mensajes
- **Integración OAuth2 Client ID**: `751c9caa-58b3-4d0b-aa90-e4204739b94d`

## Especialista Asignado (`qBUnBCRxKJEOJGFv`)

- Webhook Kommo `status_lead` (id 47214819)
- IF filter: `status_id == 104115983` para evitar ejecuciones en otros cambios de estado
- Field names corregidos: "Día de preferencia", "Email" (diferentes a gonzalo)
- Cadena completa: Calendar Create + Tasks Create + Email Confirmación

## Pendientes post-sesión

- Test cancelar cita (flujo completo + borrar evento Calendar — no implementado)
- Test cambio de fecha (flujo completo + mover evento Calendar)
- Validar prompt v7 con WhatsApp real
- Configurar agente de voz Retell en Leads entrantes (webhooks pueden apuntar a EasyPanel viejo)
- Formulario web Sheets — verificar funcional

## Fixes aplicados

- 26 correcciones vía API: headers, URLs, sub-workflow IDs, amojo_id (todo venía de gonzaloautomatizaciones)
- Webhook Kommo: seleccionar solo "Mensaje entrante recibido"
- Auth amojo: revertido de OAuth2 a Header Auth con token manual
- Prompt v5→v6→v7: varied closing, blocked pre-Reservar text, immediate email, anti-invención, STOP+confirmation
- Emails hiflymadrid→clinicazen en todos los workflows
- Status IDs gonzalo→CZ en todos los workflows
- IF anti-duplicados en Especialista Asignado
- onError: continueErrorOutput en 4 toolWorkflow nodes
