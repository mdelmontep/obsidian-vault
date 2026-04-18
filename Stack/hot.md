---
title: hot cache
date: 2026-04-17
tags: [stack, index]
---

# Hot Cache — Últimas 2 semanas

Patrones y soluciones recientes que probablemente se reutilicen pronto.
Se lee PRIMERO antes de buscar en el resto del vault.

> Si algo tiene más de 2 semanas aquí, moverlo al índice correspondiente en Stack/ o eliminarlo.

---

## Slack API — escribir en canvas (2026-04-18)

```bash
# 1. Unir bot al canal
curl -s -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"channel":"C0ARS4X5MF0"}' "https://slack.com/api/conversations.join"

# 2. Editar canvas (insert al final)
curl -s -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json; charset=utf-8" \
  -d '{"canvas_id":"F0AT6KEJLQZ","changes":[{"operation":"insert_at_end","document_content":{"type":"markdown","markdown":"- [ ] Tarea nueva\n"}}]}' \
  "https://slack.com/api/canvases.edit"
```

- Canvas Tareas Pendientes: file_id `F0AT6KEJLQZ` en canal `C0ARS4X5MF0` (#01-tareas-pendientes)
- Bot no tiene `groups:read` — solo listar canales publicos
- Ver [[slack-canvas-api-requiere-changes-array-con-operation]] y [[slack-bot-sin-groups-read-no-lista-canales-privados]]

## n8n API — credenciales no expuestas (2026-04-18)

`GET /api/v1/credentials` lista id/nombre/tipo pero nunca devuelve secrets. Guardar tokens fuera de n8n si se necesitan en otro contexto.
Ver [[n8n-api-publica-no-expone-valores-de-credenciales]]
