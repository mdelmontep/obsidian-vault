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
- **Prompt Retell**: versión 8 — reglas reforzadas "UNA SOLA PREGUNTA cada vez" + secuencia post-disponibilidad paso a paso
- **Prompt chatbot WhatsApp**: versión 7 — confirmación con día de semana + STOP antes de Reservar_cita + regla anti-invención disponibilidad
- **Error handling**: 4 toolWorkflow nodes con `onError: continueErrorOutput`
- **Emails**: todos apuntan a `citas@clinicazen.es`
- **Status IDs**: todos migrados de gonzalo a CZ
- **Code Node disponibilidad**: ARREGLADO — usa `$input.all()` del Calendar real (antes: datos hardcodeados 2025)
- **Ruta contacto existente**: ARREGLADO — `$if($('Create new contacts1').isExecuted, ..., $('Code in JavaScript1').item.json.primer_contacto.id)` 
- **Create new tasks fallback**: ARREGLADO — `doctorAsignado || 'Cita programada'` (doctor se asigna manualmente después)
- **Calendar events formato limpio**: summary = `Valoración - Tipo - Nombre`, description = Lead ID + teléfono + motivo + fuente
- **Problema**: amojo_token expira cada ~24h, hay que actualizarlo manualmente en la credencial Header Auth
- **Pendiente**: soporte Kommo habilite scope "Chats" → aplicar patrón Laserys (token dinámico) + typing entre mensajes
- **Integración OAuth2 Client ID**: `751c9caa-58b3-4d0b-aa90-e4204739b94d`

## Especialista Asignado (`qBUnBCRxKJEOJGFv`)

- Webhook Kommo `status_lead` (id 47214819)
- IF filter: `status_id == 104115983` para evitar ejecuciones en otros cambios de estado
- Field names corregidos: "Día de preferencia", "Email" (diferentes a gonzalo)
- Cadena completa: Calendar Create + Tasks Create + Email Confirmación
- Tasks: `task_type_id: 1`, text = doctor asignado o "Cita programada" si aún no hay
- Calendar: summary limpio `Valoración - tipoServicio - nombre`, description con Lead ID + datos

## Agente de Voz Retell (2026-04-20)

- **Agent ID**: `agent_350620f6b3044226efaeba9111`
- **LLM ID**: `llm_271c1594207dffae30974c56b5e6`
- **Voz**: `cartesia-Isabel` (española, femenina)
- **Modelo**: GPT-4.1
- **JSON corregido**: `~/Downloads/clinica zen 2 corregido.json`
- **Webhooks corregidos**: URLs de EasyPanel → `n8nclinicazen.agentesia.madrid`
- **Herramientas configuradas**:
  - `Mirar_disponibilidad` → webhook `/mirar_disponibilidad` — VERIFICADO OK, devuelve datos reales del calendario
  - `Reservar` → webhook `/Reservar_crm` — VERIFICADO OK (contacto existente + nuevo)
  - `Cancelar_cita` → webhook `/cancelar_cita` — AÑADIDO 2026-04-21, parameter_type json
  - `end_call` → nativo Retell
  - `transfer_call` → configurado via JSON, número provisional +34617314938 (pendiente: cambiar al definitivo de la clínica)
- **parameter_type**: `json` en Reservar y Cancelar_cita (n8n espera JSON body)
- **is_published**: false (pendiente publicar cuando se conecte teléfono)
- **Test real completado**: llamada con reserva exitosa (Julián Fernández, 24/04 13:00)
- **Prompt actualizado (2026-04-21)**: flujo cancelar/cambiar fecha con tools (antes redirigía a WhatsApp)

## Pendientes post-sesión

- ~~Conectar teléfono definitivo de la clínica en Retell~~ HECHO 2026-04-23
- ~~Test cancelar cita (flujo completo + borrar evento Calendar — no implementado)~~ HECHO 2026-04-21
- ~~Test cambio de fecha (flujo completo + mover evento Calendar)~~ HECHO 2026-04-21 (cancel + re-reservar)
- ~~Publicar agente Retell (`is_published: true`)~~ HECHO 2026-04-23
- ~~Scope "Chats" Kommo (contactar soporte)~~ DESCARTADO 2026-04-23 — no se puede habilitar
- ~~Verificar contenido RAG (Supabase) actualizado para CZ~~ HECHO 2026-04-23
- ~~15 eventos de test creados en calendario (semana 21-25 abril)~~ Ya borrados (sesión test 2026-04-21)
- ~~Revisar salesbot 68822 en GUI Kommo — quitar acción que mueve leads a 104115975~~ HECHO 2026-04-23

## Fixes aplicados

- 26 correcciones vía API: headers, URLs, sub-workflow IDs, amojo_id (todo venía de gonzaloautomatizaciones)
- Webhook Kommo: seleccionar solo "Mensaje entrante recibido"
- Auth amojo: revertido de OAuth2 a Header Auth con token manual
- Prompt v5→v6→v7: varied closing, blocked pre-Reservar text, immediate email, anti-invención, STOP+confirmation
- Emails hiflymadrid→clinicazen en todos los workflows
- Status IDs gonzalo→CZ en todos los workflows
- IF anti-duplicados en Especialista Asignado
- onError: continueErrorOutput en 4 toolWorkflow nodes
- Redis debounce: añadido fallback `Merge.json.text` para transcripciones Whisper (antes solo buscaba `Merge.json.Mensaje` → audios se perdían silenciosamente)
- Flujo estados Retell: Create new leads2/3 ahora crean en 104111891 → Update lead to Pendiente actualiza a 104115975 → Respond to Webhook
- Envío via salesbot: PATCH field 1903454 + POST /api/v2/salesbot/run bot_id 68822 (migrado de amojo v1)
- Prompt AI Agent: regla 14 (no re-preguntar datos), regla 15 (cancelar antes de mover cita), detección implícita cambio fecha
- Derivación Humano: dual entry (executeWorkflowTrigger + webhook `/derivar_humano`), field_id corregido a 1828350
- Calendar events: duración 30 min (antes 60 min)
