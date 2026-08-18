---
title: Blueprint recepcionista virtual para peluquería (n8n + Retell)
date: 2026-08-18
source: agentesia
tags: [n8n, retell, supabase, whatsapp, blueprint, peluqueria, onboarding]
---

# Blueprint recepcionista virtual para peluquería

Diseño completo de marzo de 2026 para el agente de una peluquería: **n8n + Retell + Supabase +
Google Calendar + WhatsApp**, desplegado en Dokploy. Es el patrón que la skill
`client-onboarding` clona como blueprint del vertical peluquerías.

**Por qué está aquí:** vivía como `MEMORY.md` suelto en
`~/.claude/projects/-Users-manueldelmonte-AI-N8N-Workflows-N8N-Peluqueria-N8N-Claude/`, un cwd que
dejó de existir al migrar de Mac. No lo cargaba ninguna sesión. Recuperado en la limpieza del
18-ago-2026 junto con otras 111 memorias huérfanas.

## Piezas generadas

**Workflows n8n** — un router principal (`MAIN_ReceptionistaVirtual`) y diez subworkflows:
`SW_IdentifyClient`, `SW_CheckAvailability`, `SW_CreateAppointment`, `SW_ModifyAppointment`,
`SW_CancelAppointment`, `SW_SendWhatsApp`, `SW_UpdateMemory`, `SW_GetBusinessManual`,
`SW_LogToSheets` y `SW_ReminderScheduler` (cron cada 15 min).

**Retell** — prompt del agente «Sofía» y seis tools: `get_client_info`, `check_availability`,
`book_appointment`, `modify_appointment`, `cancel_appointment`, `get_business_info`.

**Base de datos** — esquema SQL con RLS, triggers, vistas e índices, más semilla de staff,
servicios y `business_manual`.

**Documentación** — despliegue en Dokploy, alta de credenciales OAuth2 de Google y Supabase,
recomendaciones de seguridad y RGPD, y ejemplos de payload Retell ↔ n8n.

## Decisiones de arquitectura

- **Un solo webhook** `/webhook/retell/events` para todos los eventos y tool calls, con switch por
  `event_type`. Menos superficie que un endpoint por tool.
- **Subworkflows con `Execute Workflow`**, con los IDs en variables de entorno `SW_*_WORKFLOW_ID`:
  el clonado a otro cliente no exige tocar los nodos.
- **Supabase con RLS activo** y `service_role` solo en el backend de n8n.
- **Memoria conversacional** por resumen con LLM y *fallback* basado en reglas, para que un fallo
  del modelo no deje la conversación sin contexto.
- **Google Calendar** en slots de 30 min, hasta 3 alternativas, horario L-V 9-20 y S 9-15.
- **WhatsApp con capa abstracta** enrutada por `WHATSAPP_PROVIDER` (meta/twilio), decidida antes de
  elegir proveedor. Ver [[checklist-migracion-chatbot-mejorado]].

## Pendiente de la segunda pasada

- Varios estilistas con calendario individual.
- Error workflow global en n8n.
- Validación más robusta de fechas pasadas.
- En `modifyAppointment`, clientes con nombre sin confirmar: buscar por teléfono con JOIN a
  `clients`.

## Credenciales

No van aquí. La URL de Supabase, el client ID de Google y el resto de valores del proyecto están en
1Password y en el `.env` del cliente. Timezone del despliegue: `Europe/Madrid`.
