---
title: chatwoot allow_auto_assign true cascada a assignee individual
date: 2026-04-16
source: claude-code-session
tags: [chatwoot, teams, auto-assign, gate, chatbot]
---

En Chatwoot, cuando un Team tiene `allow_auto_assign: true` (valor por defecto), asignar una conversación al team vía `POST /assignments` con `{ "team_id": 1 }` hace que Chatwoot **cascadee automáticamente** a un agente individual del equipo (round-robin).

## Problema

Si el workflow usa `conversation.meta.assignee == null` como gate para decidir si el bot debe responder, el cascade rompe el gate inmediatamente: la conversación llega con `assignee = { id: 3, name: "Manuel" }` y el bot queda silenciado desde el primer mensaje.

## Síntoma

- El bot saluda una vez y luego no responde más
- En el webhook `message_created`, `conversation.meta.assignee` ya tiene un agente individual
- En Chatwoot UI, la conversación aparece asignada a un agente concreto además del team

## Fix

```bash
curl -X PATCH "https://<chatwoot>/api/v1/accounts/1/teams/<team_id>" \
  -H "api_access_token: <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"allow_auto_assign": false}'
```

Con `allow_auto_assign: false`, el team se asigna pero NO cascadea a agente individual. La conversación queda visible para todos los miembros del team (lo cual es deseable para visibilidad + push notifications) sin romper el gate del bot.

## Nota importante

Si ya hubo cascade antes del fix, hay que desasignar manualmente las conversaciones afectadas:

```bash
curl -X POST "https://<chatwoot>/api/v1/accounts/1/conversations/<id>/assignments" \
  -H "api_access_token: <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"assignee_id": null}'
```
