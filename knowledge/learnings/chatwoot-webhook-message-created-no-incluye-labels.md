---
title: chatwoot webhook message_created no incluye labels
date: 2026-04-16
source: claude-code-session
tags: [chatwoot, webhooks, labels, n8n, gate]
---

El webhook `message_created` de Chatwoot envía el objeto `conversation` con `meta` (assignee, sender), `additional_attributes`, `status`, etc. pero **no incluye las labels** de la conversación.

## Impacto

Si el workflow n8n necesita gatear por labels (ej: "solo responder si NO tiene label `humano`"), no puede hacerlo directamente desde el payload del webhook.

## Fix

Añadir un Code node antes del gate que haga GET a la API de Chatwoot:

```javascript
const conversationId = $input.first().json.body?.conversation?.id;
let labels = [];
try {
  const resp = await this.helpers.httpRequest({
    method: 'GET',
    url: `https://chatwoot.example.com/api/v1/accounts/1/conversations/${conversationId}/labels`,
    headers: { 'api_access_token': '<TOKEN>' },
    json: true,
  });
  labels = resp?.payload || [];
} catch (e) { labels = []; }
return [{ json: { ...$input.first().json, _labels: labels, _botPaused: labels.includes('humano') } }];
```

El gate entonces usa `_botPaused !== true` en vez de parsear el webhook directamente.

## Coste

Una HTTP call extra por mensaje entrante. Aceptable para volúmenes de chat normales (<100 msg/min).
