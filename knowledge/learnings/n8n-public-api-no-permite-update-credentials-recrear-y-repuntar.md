---
title: n8n public API no permite UPDATE credentials — solo POST/DELETE
date: 2026-05-25
source: claude-code-session
tags: [n8n, api, credentials]
---

`/api/v1/credentials` solo admite `POST` (crear) y `DELETE`. No hay `PATCH` ni `PUT` para rotar password/token de una cred existente.

Para rotar credencial sin tocar UI:
1. `POST /api/v1/credentials` con misma config + valor nuevo → devuelve ID nuevo
2. `DELETE /api/v1/credentials/<old_id>`
3. `GET /api/v1/workflows` + filtrar nodos que referenciaban old_id → `PUT /api/v1/workflows/<id>` con cred ID reemplazada en `node.credentials.<type>.id`

Sin paso 3 los workflows quedan apuntando a la cred borrada y fallan en runtime con "Credential not found".

Caso real: EcoBox SMTP 2026-05-25 — placeholder → real Gmail app-password requirió recrear + repuntar 3 workflows (`Reservar_cita`, `Meta token health check`, `TEST Email Templates`).
