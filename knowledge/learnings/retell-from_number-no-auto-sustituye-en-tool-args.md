---
title: Retell `{{from_number}}` NO se auto-sustituye en argumentos de tool
date: 2026-05-25
source: claude-code-session
tags: [retell, sip, dynamic-variables]
---

`{{from_number}}` se sustituye al renderizar el texto del PROMPT del agente (lo que el LLM lee). Pero cuando el LLM construye los argumentos de una tool call, suele pasar la cadena literal `{{from_number}}` si el prompt le instruye "usa {{from_number}} como phone".

Causas:
1. Algunos providers SIP (Zadarma, certos trunks BYO) NO populan `retell_llm_dynamic_variables.from_number` automáticamente.
2. Aunque se popule, depende del modelo entender que la variable se sustituye y no pasarla como string.

Fix robusto en backend (n8n / endpoint):
```js
const llmPhone = body.args?.phone;
const isBad = !llmPhone || /\{\{.*\}\}/.test(llmPhone);
const fallback = body.call?.from_number || body.call_inbound?.from_number;
const phone = isBad ? fallback : llmPhone;
```

El payload de Retell siempre incluye `call.from_number` real en inbound calls.

Caso real: EcoBox 2026-05-25 — `Reservar_cita` guardó "{{from_number}}" literal en GCal description hasta añadir el fallback + guard validación.
Segundo caso real: Simarro 2026-08-12 — `Reservar` recibió `"phone":"+34{{from_number}}"` literal (el propio texto de la instrucción del nodo mencionaba `{{from_number}}` entre paréntesis, y el LLM copió el placeholder en vez de sustituirlo); n8n ya tenía el guard aplicado (`Edit Fields3`) y no llegó a romper el dato. Patrón confirmado transversal entre clientes — revisar el mismo guard en cualquier flujo de voz nuevo que reciba `phone`/`from_number` de un LLM.
