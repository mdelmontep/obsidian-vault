---
title: checklist migración ChatBOT mejorado a nuevo cliente
date: 2026-04-16
source: claude-code-session
tags: [inbox, pendiente, n8n, chatwoot, chatbot, migración, checklist]
---

Patrón reutilizable para migrar el ChatBOT mejorado a un nuevo cliente. Ya aplicado en Agentesia y Tecnocloud.

## Chatwoot — crear recursos

1. [ ] Labels: `bot-activo` (verde `#2ecc71`) + `humano` (naranja `#f39c12`)
2. [ ] Team (ej: "Soporte" o "Ventas") con `allow_auto_assign: false`
3. [ ] Añadir agentes al team
4. [ ] Agent Bot con `outgoing_url` apuntando al webhook del workflow
5. [ ] Inbox WhatsApp Cloud (necesita phone_number_id, WABA ID, API key permanente de Meta)
6. [ ] Asignar Agent Bot al inbox WhatsApp Cloud (no al API viejo)
7. [ ] Automation Rule "Reset a bot-activo al resolver" (status=resolved + labels=humano → remove humano, add bot-activo)
8. [ ] Desactivar auto-assign en el inbox

## Meta Developer Console

9. [ ] Redirigir Callback URL al de Chatwoot (`https://<chatwoot>/webhooks/whatsapp/<+phone>`)
10. [ ] Poner Verify Token generado por Chatwoot
11. [ ] Suscribir campo `messages`

## Workflow n8n — adaptar datos

12. [ ] System prompt: cambiar identidad, empresa, tools, flujo
13. [ ] URLs Chatwoot: todos los nodos (CW Enviar, CW Init, Cargar estado, Ejecutar handoff, Auto-asignar, Label humano)
14. [ ] Token Chatwoot: en headers HTTP y Code nodes
15. [ ] Typing Meta: phone_number_id + Bearer token
16. [ ] Webhook path: único por cliente
17. [ ] Credenciales n8n: OpenAI, Redis, Postgres, y las específicas del cliente (Gmail, Sheets, Calendar, Slack, PGVector...)
18. [ ] Tools del AI Agent: quitar las del cliente anterior, añadir las del nuevo, reconectar
19. [ ] Team ID en CW Init y Auto-asignar (puede no ser 1 si ya había teams)

## Post-migración

20. [ ] Activar workflow
21. [ ] Test: mensaje → bot responde → handoff → bot calla → resolver → bot vuelve
22. [ ] Verificar push notifications en app móvil
23. [ ] Cambiar CW Enviar a usar token del Agent Bot (para que firme como bot, no como usuario)
24. [ ] Desactivar workflow viejo del cliente
