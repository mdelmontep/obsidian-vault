---
title: agency-portal — workflows n8n
date: 2026-04-29
tags: [n8n, agency-portal, onboarding, whatsapp]
---

# Agency Portal — Workflows n8n

Instancia: `https://n8n.agentesia.madrid`

## Onboarding WhatsApp

| Workflow | ID | Trigger | Estado |
|---|---|---|---|
| AIA Onboarding — Research y arranque | `Xwh3IHFRumrz0IfO` | Webhook HTTP `POST /webhook/aia-onboarding` | Activo |
| AIA Onboarding — Conversación | `3ts4ChLJKC90syOp` | `executeWorkflowTrigger` (sub-workflow del anterior) | Activo |

### Flujo

1. Portal → n8n: `POST https://n8n.agentesia.madrid/webhook/aia-onboarding`
   - Payload: `{ event, client_id, session_id, business_name, website, whatsapp_phone, notes, callback_url }`
   - `callback_url` = `https://clientes.agentesia.madrid/api/webhooks/whatsapp-onboarding`
2. n8n hace research (GPT-4o-mini) + inicia conversación WhatsApp
3. n8n → portal: `POST callback_url` con header `x-webhook-secret: <WHATSAPP_ONBOARDING_WEBHOOK_SECRET>`

### Credenciales en el portal

Configurar en `/agency/admin/connectors` → proveedor **WhatsApp Onboarding**:

| Campo | Valor |
|---|---|
| `N8N_ONBOARDING_TRIGGER_URL` | `https://n8n.agentesia.madrid/webhook/aia-onboarding` |
| `WHATSAPP_ONBOARDING_WEBHOOK_SECRET` | shared secret (también configurado en n8n para los callbacks) |

### n8n debe enviar en los callbacks al portal

Header: `x-webhook-secret: <valor de WHATSAPP_ONBOARDING_WEBHOOK_SECRET>`
