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

- **El cuerpo se arma en un Code node, no en la expresión del HTTP.** Un
  `={{ JSON.stringify({...blocks...}) }}` con la plantilla dentro no se evalúa: devuelve
  `{"error":"invalid syntax"}` y, si el nodo lleva `onError: continueRegularOutput`, la
  ejecución sale en verde **sin haber avisado**. Y Slack responde 200 aunque rechace el
  mensaje, así que hace falta un nodo que exija `ok===true`. Ver
  [[un-canal-de-avisos-solo-se-verifica-mirando-el-canal]].

Ver [[n8n-api-put-workflows-rechaza-settings-desconocidos]] · [[n8n-api-activate-es-POST-no-PATCH]] · [[n8n-jsonbody-stringify-evita-control-characters]].
Casos reales: Simarro, handler `j3Rtnj0fBskd5meD` → #01-incidencias, 29 workflows (25-jun).
Elphis, handler `QKuw8ranAthAKSNh` → mismo canal, 28 workflows (12-ago), con dedup real de 60 min
por `workflow+nodo` en `idempotency_log`.

**Este patrón llevaba desde junio resuelto para Simarro y Elphis no lo tenía**: su handler existía,
activo, asociado a 2 workflows de 25, y sus 55 errores en 14 días no llegaron a nadie. Al montar
algo así, replicarlo el mismo día en el resto de clientes o queda como pieza de uno solo. La nota
de Elphis decía además que la API rechazaba `settings.errorWorkflow` con un 500 — **obsoleto**: hoy
lo acepta sin problema, 27 de 27 a la primera.
