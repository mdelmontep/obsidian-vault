---
title: stack chatwoot — reglas y patrones
date: 2026-04-20
source: claude-md-migration
tags: [chatwoot, whatsapp, infra]
---

# Stack Chatwoot

- Imagen: `chatwoot/chatwoot:latest`
- `ENABLE_ACCOUNT_SIGNUP=false` en producción siempre
- SMTP hardcodeado en compose, no en variables de entorno (Dokploy no las inyecta bien)
- Si SMTP falla → verificar con `docker exec chatwoot-sidekiq env | grep SMTP`
- Error "sendmail delivery failed" = las vars SMTP no llegaron al contenedor
- Postgres vacío tras crash: restaurar con `db:schema:load` + `db:seed` desde `chatwoot-rails`
- Inbox API sin webhook URL — si tiene URL, Chatwoot marca mensajes con 404

## Automation Rules y Teams

- **`allow_auto_assign: true` en un Team cascada a assignee individual** — si el workflow usa `assignee == null` como gate, el cascade rompe el gate inmediatamente. Desactivar con `PATCH /teams/{id}` body `{"allow_auto_assign": false}`
- **Automation Rules con `assignee_id is_not_present` disparan en CADA update** si no hay assignee individual — condición siempre verdadera. Para "vuelta al bot", usar `status equal_to resolved` como trigger en vez de `assignee_id is_not_present`
- **Webhook `message_created` de Chatwoot no trae labels** — para gatear por labels, hacer GET `/conversations/{id}/labels` en un Code node antes del IF gate
- **Agent Bot debe asignarse al inbox correcto** — al crear un inbox WhatsApp Cloud nuevo (ej: id=2), el Agent Bot puede quedar asignado al inbox viejo (id=1). Si el workflow no ejecuta tras enviar mensaje, verificar con `GET /inboxes` que el bot está en el inbox donde llegan los mensajes. Reasignar con `POST /inboxes/{id}/set_agent_bot`
- **WhatsApp Cloud en Chatwoot requiere redirigir el webhook de Meta** — sin cambiar la Callback URL en Meta Developer Console → WhatsApp → Configuration, los mensajes siguen llegando al destino anterior (n8n directo) y Chatwoot muestra 0 conversaciones. Configurar URL + Verify Token + suscribir campo `messages`
