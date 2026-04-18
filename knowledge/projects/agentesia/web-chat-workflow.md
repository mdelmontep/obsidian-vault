---
title: workflow Web Chat Agentesia — estructura y diferencias con ChatBOT WhatsApp
date: 2026-04-15
source: claude-code-session
tags: [n8n, agentesia, chatbot, workflow, agentes-ia]
---

Workflow n8n creado el 2026-04-15 para el widget de chat de la web de AgentesIA (`localhost:8080` en desarrollo, `agentesia.madrid` en producción). Replica la funcionalidad del agente de WhatsApp pero adaptado para chat web síncrono.

## Metadata

- **Nombre**: `Web Chat Agentesia`
- **ID n8n**: `G8vbSYm0SY3zi912`
- **Host**: `https://n8n.agentesia.madrid`
- **Webhook público**: `https://n8n.agentesia.madrid/webhook/web-chat-agentesia`
- **Método**: `POST`
- **Request body**: `{ "message": "...", "sessionId": "..." }`
- **Response body**: `{ "output": "..." }`
- **Estado**: activo
- **Widget conectado en**: `~/Agentesia/WEBSITES/Agentesia WEB/new-project-setup/src/pages/ChatbotPage.tsx:17`

## Estructura (12 nodos)

1. **Webhook** (`n8n-nodes-base.webhook`) — POST `/webhook/web-chat-agentesia`, `responseMode: "responseNode"`
2. **Normalizar** (Set) — mapea `message → chatInput`, `sessionId → sessionKey` con prefijo `web:` para separar la memoria de la de WhatsApp
3. **AI Agent** (`langchain.agent`) — system prompt adaptado (ver sección siguiente)
4. **OpenAI Chat Model** — `gpt-4.1`, temp 0.3, credenciales `LwQa5VpuTLKK0Lop`
5. **Postgres Chat Memory** — `sessionKey = web:{sessionId}`, `contextWindowLength: 15`, credenciales `1QKsiFW3B4U1mAzz`
6. **Think** (`toolThink`) — misma descripción que WhatsApp, sin referencia a chatId como teléfono
7. **Mirar Dispo** (`googleCalendarTool`) — calendar `Leads Agentesia` (`c_9d60e09dfaa1c27ff780d83f8fb7071576178ba95e0b3be3f22cc5112a9505e6@group.calendar.google.com`)
8. **Reservar** (`googleCalendarTool`) — mismo calendar, creación de eventos de demo
9. **Registro Sheets** (`googleSheetsTool`) — Sheet `Registro de Leads AGENTESIA` (`1kEUGE3q58A0yqIOj6YZKie6EtJmQ8OCDDYahKu27NCk`), con `Channel = "web"`
10. **Lead caliente** (`slackTool`) — canal `C0ARXC2L406`, texto con tag "— ChatBOT WEB"
11. **Lead cita DEMO** (`slackTool`) — mismo canal, tag "— ChatBOT WEB"
12. **Respond to Webhook** — devuelve `{ "output": "{{ $('AI Agent').item.json.output }}" }`

## Diferencias respecto al ChatBOT WhatsApp

| Aspecto | WhatsApp (`enVlCyi7McKfwkRQ`) | Web (`G8vbSYm0SY3zi912`) |
|---|---|---|
| Identidad prompt | "AIA por WhatsApp" | "AIA en el chat de la web" |
| sessionKey memoria | `chatId` (teléfono puro) | `web:<uuid del widget>` |
| Teléfono del cliente | Ya conocido del `chatId`, no se pide | Se pide explícitamente en el flujo de datos |
| Respuesta | Envía mensaje vía WhatsApp Cloud API | Devuelve JSON por HTTP (Respond to Webhook) |
| Infraestructura adicional | Chatwoot sync, Redis sentinel para batches | Ninguna — flow lineal simple |
| Channel en Sheets | `whatsapp` | `web` |
| Tag Slack | `- ChatBOT` | `- ChatBOT WEB` |

## System prompt — adaptaciones hechas al copiarlo de WhatsApp

Cinco replacements aplicados sobre el prompt original:

1. `"Eres AIA, asistente virtual de AgentesIA por WhatsApp"` → `"...en el chat de la web"`
2. `"AIA atiende 24 horas por WhatsApp"` → `"AIA atiende 24 horas por chat web y WhatsApp"`
3. Regla eliminada: `"Teléfono del cliente: {{ chatId }} — nunca lo inventes."` (no aplica, en web no hay teléfono de entrada)
4. Instrucción DATOS: `"2. Teléfono → confirmar repitiéndolo..."` → `"2. Teléfono → pídelo y confirma repitiéndolo..."`
5. Check del Think: `"Teléfono: {{ chatId }} (ya lo tengo del chat)"` → `"Teléfono (pedirlo explícitamente, no lo tengo por defecto)"`

## Bugs encontrados y fixes aplicados (solo al workflow Web)

### Bug 1 — tool mismatch "Agendar" / "Reservar"

El system prompt original de WhatsApp usaba `"Agendar"` como nombre de la tool en los pasos `<flujo_agendar>`, pero el nodo real se llama `"Reservar"`. El LLM no encontraba la tool y saltaba la llamada silenciosamente sin error. El agente decía "te reservo el jueves a las 11:00" pero no creaba el evento.

**Fix aplicado al workflow Web** (3 reemplazos en system prompt + 1 en Think description):
- `"Agendar"` → `"Reservar"`
- `**Agendar**` → `**Reservar**`
- `"+ Agendar,"` → `"+ Reservar,"`

**Estado en WhatsApp**: no tocado. Probablemente también está roto ahí. Pendiente de auditar.

### Bug 2 — Google Sheets con `columns.value: {}` inserta filas vacías

El nodo `Registro Sheets` se copió con `mappingMode: "defineBelow"` pero `value: {}` vacío. Esto hace que las filas se inserten en blanco sin dar error.

**Fix aplicado al workflow Web** — mapping explícito por columna:

```json
{
  "Fecha": "={{ $now.toFormat('yyyy-MM-dd HH:mm') }}",
  "Nombre": "={{ $fromAI('Nombre', 'Nombre completo del cliente', 'string') }}",
  "Teléfono": "={{ $fromAI('Telefono', 'Teléfono del cliente en formato internacional', 'string') }}",
  "Empresa": "={{ $fromAI('Empresa', 'Nombre de la empresa del cliente, o vacío si no lo dio', 'string') }}",
  "Tipo negocio": "={{ $fromAI('Tipo_negocio', 'Sector o tipo de negocio (clínica, taller, restaurante, etc.)', 'string') }}",
  "Interés": "={{ $fromAI('Interes', 'Resumen corto del servicio que le interesa al cliente', 'string') }}",
  "Urgencia": "={{ $fromAI('Urgencia', 'Una de: callback_inmediato | cita_agendada | solo_info', 'string') }}",
  "Fecha cita": "={{ $fromAI('Fecha_cita', 'Solo si urgencia=cita_agendada. Formato YYYY-MM-DD. Vacío si no aplica', 'string') }}",
  "Hora cita": "={{ $fromAI('Hora_cita', 'Solo si urgencia=cita_agendada. Formato HH:MM. Vacío si no aplica', 'string') }}",
  "Estado": "nuevo",
  "Channel": "web"
}
```

**Estado en WhatsApp**: no tocado. Sospecha fuerte de que lleva tiempo insertando filas vacías. Pendiente de auditar.

### Bug 3 — Agente re-dispara tools de escritura en turnos posteriores

`memoryPostgresChat` solo persiste mensajes user/assistant, no tool calls. El agente re-llamaba `Registro Sheets` + `Lead caliente` en cada mensaje nuevo del cliente aunque ya las hubiera llamado antes.

**Fix aplicado al workflow Web** — regla explícita añadida en `<reglas>` del system prompt:

> **No repetir acciones ya ejecutadas**: Antes de llamar a Reservar, Registro Sheets, Lead caliente o Lead cita DEMO, revisa el historial de mensajes. Si ya hay un mensaje tuyo anterior diciendo "el equipo te llama en un ratito", "listo [nombre]", "perfecto [nombre]" o similar confirmación final, el lead YA está registrado y notificado. NO vuelvas a llamar a estas cuatro herramientas.

### Bug 4 — Reservar disparado antes de tener datos del cliente

Cuando el usuario decía "perfecto, confirmo" tras elegir hora, el agente llamaba a `Reservar` inmediatamente con `Cliente: ""` y `Teléfono: ""` vacíos, creando un evento basura en el Calendar. Luego, al recibir los datos, llamaba otra vez a `Reservar` creando un evento duplicado completo.

**Fix aplicado al workflow Web** — regla explícita:

> **Orden obligatorio antes de Reservar**: NUNCA llames a Reservar sin tener explícitamente recogidos estos tres datos del cliente: nombre completo, teléfono y empresa/negocio. Si el cliente confirma una hora ("perfecto", "vale", "confirmo") pero aún no has pedido estos datos, tu siguiente acción es PEDIRLOS uno a uno, NO llamar a Reservar. Solo cuando tengas los tres datos, en el mismo turno: primero Reservar, luego Registro Sheets, luego Lead cita DEMO.

## Testing end-to-end verificado

Tests manuales ejecutados vía `curl` al webhook con `sessionId` único por escenario:

- ✅ **Callback inmediato** — `Registro Sheets` + `Lead caliente` disparadas una vez cada una con datos completos
- ✅ **Cita agendada** — `Mirar Dispo` leyó el calendar, `Reservar` creó el evento, `Registro Sheets` + `Lead cita DEMO` registraron con `urgencia: cita_agendada` y `fecha_cita`/`hora_cita`
- ✅ **No-repeat tras cierre** — al continuar la conversación tras un cierre de callback, el agente no re-disparó tools
- ⚠️ **OpenAI rate limit**: >10 mensajes en 30s dispara 429. Pacing de 10-12s entre turnos en tests

## Credenciales compartidas con WhatsApp (no duplicadas)

- OpenAI: `LwQa5VpuTLKK0Lop` (cuenta "OpenAI account")
- Postgres: `1QKsiFW3B4U1mAzz` (cuenta "Postgres account")
- Google Calendar: `TzTKThlcSL2T4Cxa` (cuenta "Google Calendar account 2")
- Google Sheets: heredadas del workflow original
- Slack: `Ac696Zz30fbPnqxA` (cuenta "Slack account")

## Cómo actualizar el system prompt vía API

```bash
curl -X PUT "https://n8n.agentesia.madrid/api/v1/workflows/G8vbSYm0SY3zi912" \
  -H "X-N8N-API-KEY: <KEY>" \
  -H "Content-Type: application/json" \
  -d '{"name":"...","nodes":[...],"connections":{...},"settings":{"executionOrder":"v1"}}'
```

El endpoint PUT solo acepta `name`, `nodes`, `connections`, `settings`, `staticData`. Cualquier otro campo da error.
