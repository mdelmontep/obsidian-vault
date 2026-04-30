---
title: agency-portal — workflows n8n
date: 2026-04-30
tags: [n8n, agency-portal, onboarding, whatsapp]
---

# Agency Portal — Workflows n8n

Instancia: `https://n8n.agentesia.madrid`

## Onboarding WhatsApp

| Workflow | ID | Trigger | Estado |
|---|---|---|---|
| AIA Onboarding — Research y arranque | `Xwh3IHFRumrz0IfO` | Webhook HTTP `POST /webhook/aia-onboarding` | Activo |
| AIA Onboarding — Conversación | `3ts4ChLJKC90syOp` | `executeWorkflowTrigger` (sub-workflow del anterior) | Activo |

### Arquitectura (Opción B — portal como cerebro IA)

n8n actúa solo como capa I/O. GPT, historial y extracción de campos viven en el portal.

**Flujo completo:**
1. Portal → n8n: `POST https://n8n.agentesia.madrid/webhook/aia-onboarding`
   - Payload: `{ event, client_id, session_id, business_name, website, whatsapp_phone, notes, callback_url }`
2. n8n (Research y arranque): saludo personalizado vía WhatsApp Cloud → llama sub-workflow Conversación
3. n8n (Conversación — 5 nodos): recibe mensaje WhatsApp → `POST /api/onboarding/conversation` al portal → envía respuesta a Chatwoot → si `is_complete`, borra clave Redis de sesión
4. n8n → portal (callbacks webhook): `POST https://clientes.agentesia.madrid/api/webhooks/whatsapp-onboarding` con header `x-webhook-secret`

### Env vars en contenedor n8n (Dokploy) — pendiente añadir

| Var | Valor |
|---|---|
| `PORTAL_WEBHOOK_SECRET` | = `WHATSAPP_ONBOARDING_WEBHOOK_SECRET` de `/agency/admin/connectors` |
| `CHATWOOT_API_TOKEN` | `ST6t3xSRksMLaayFoHam8woM` |
| `META_WA_TOKEN` | token Meta WhatsApp Cloud |

### Credenciales en el portal

Configurar en `/agency/admin/connectors` → proveedor **WhatsApp Onboarding**:

| Campo | Valor |
|---|---|
| `N8N_ONBOARDING_TRIGGER_URL` | `https://n8n.agentesia.madrid/webhook/aia-onboarding` |
| `WHATSAPP_ONBOARDING_WEBHOOK_SECRET` | shared secret (también en `$env.PORTAL_WEBHOOK_SECRET` de n8n) |

### n8n debe enviar en los callbacks al portal

Header: `x-webhook-secret: <valor de WHATSAPP_ONBOARDING_WEBHOOK_SECRET>`
