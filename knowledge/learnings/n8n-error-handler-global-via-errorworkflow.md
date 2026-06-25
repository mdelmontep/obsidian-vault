---
title: n8n error handler global via settings.errorWorkflow + incoming webhook
date: 2026-06-25
source: claude-code-session
tags: [n8n, slack, observabilidad, patron]
---

Para avisar de fallos de cualquier workflow n8n: 1 workflow handler `Error Trigger → Set (contexto) → httpRequest` y asignar `settings.errorWorkflow = <id handler>` en cada workflow vía API (GET de cada uno → PUT con `{name,nodes,connections,settings}`, filtrando `binaryMode`/`availableInMCP` que la API rechaza).

- **Incoming Webhook de Slack > nodo Slack OAuth**: el webhook es una URL, no depende de credencial por instancia (portable entre n8n distintos). Body: `={{ JSON.stringify({ text: $json.slack_message }) }}` (evita control chars).
- **No se hereda**: cada workflow NUEVO hay que asignárselo a mano o re-correr el script. El Error Trigger solo dispara para los workflows que lo referencian, no global.
- Workflows `archived=true` no son editables (`400 Cannot update an archived workflow`) → excluirlos; no se ejecutan igualmente.
- El campo `dedupe_key` del template típico no hace nada sin un nodo que deduplique; si hay spam, dedup real con `staticData`.

Ver [[n8n-api-put-workflows-rechaza-settings-desconocidos]] · [[n8n-api-activate-es-POST-no-PATCH]] · [[n8n-jsonbody-stringify-evita-control-characters]].
Caso real: Simarro, handler `j3Rtnj0fBskd5meD` → Slack #01-incidencias, 29 workflows.
