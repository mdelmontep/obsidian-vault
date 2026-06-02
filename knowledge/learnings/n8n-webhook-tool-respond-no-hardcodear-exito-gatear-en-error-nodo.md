---
title: workflow-webhook que respalda un tool LLM no debe hardcodear éxito en el respond
date: 2026-06-01
source: claude-code-session
tags: [n8n, workflow, llm, gotcha]
---

Un workflow-webhook que respalda un tool de un agente LLM NO debe hardcodear `confirmation_text:"Listo, hecho"` en el `respondToWebhook`. Si el nodo de acción (GCal create/delete, HTTP, etc.) tiene `onError:continueRegularOutput`, el error se traga y el Respond devuelve éxito → el bot **confirma al cliente algo que no ocurrió** (reserva/cancelación fantasma).

Fix:
- Tras el nodo de acción, `IF` sobre `!$json.error` → rama true (efectos: WhatsApp/email + Respond éxito) / rama false (`Respond` con `status:error` + texto honesto).
- En cancelación/borrado simple: Respond ternario sobre `$('GCal delete').item.json.error` → `status:ok|error`.
- El prompt del bot debe LEER `status`/`confirmation_text` y reflejarlo, no inventar.

Caso EcoBox 2026-06-01. Ver [[onError-continueRegularOutput-devuelve-axiosError-no-statusCode]].
