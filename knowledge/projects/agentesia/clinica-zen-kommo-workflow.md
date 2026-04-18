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

## Estado actual (2026-04-17)

- **Funcional**: recibe mensajes y responde vía amojo API v1
- **Problema**: amojo_token expira cada ~24h, hay que actualizarlo manualmente en la credencial Header Auth
- **Pendiente**: soporte Kommo habilite scope "Chats" → aplicar patrón Laserys (token dinámico) + typing entre mensajes
- **Integración OAuth2 Client ID**: `751c9caa-58b3-4d0b-aa90-e4204739b94d`

## Fixes aplicados en esta sesión

- 26 correcciones vía API: headers, URLs, sub-workflow IDs, amojo_id (todo venía de gonzaloautomatizaciones)
- Webhook Kommo: seleccionar solo "Mensaje entrante recibido"
- Auth amojo: revertido de OAuth2 a Header Auth con token manual
