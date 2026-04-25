---
title: n8n api activate es POST no PATCH
date: 2026-04-25
source: claude-code-session
tags: [n8n, api]
---

Endpoints de la API pública de n8n para gestionar estado de workflows:

| Acción | Método | Endpoint |
|--------|--------|----------|
| Activar | `POST` | `/api/v1/workflows/{id}/activate` |
| Desactivar | `POST` | `/api/v1/workflows/{id}/deactivate` |
| Actualizar nodos/connections | `PUT` | `/api/v1/workflows/{id}` |

**No usar PATCH** — devuelve `405 Method Not Allowed`.

El `PUT` para actualizar requiere el campo `name` obligatorio en el body, además de `nodes`, `connections` y `settings`. Sin `name` devuelve `request/body must have required property 'name'`.
