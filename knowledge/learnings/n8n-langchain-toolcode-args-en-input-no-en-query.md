---
title: n8n langchain toolCode con specifyInputSchema — args en $input.first().json, no en `query`
date: 2026-05-30
source: claude-code-session
tags: [n8n, langchain, gotcha, toolcode]
---

En `@n8n/n8n-nodes-langchain.toolCode` v1.1+ con
`specifyInputSchema:true + schemaType:'manual' + inputSchema` JSON Schema,
los argumentos que rellena el LLM llegan al jsCode como objeto en
`$input.first().json`. La variable mágica `query` queda VACÍA en ese caso.

Sin schema, `query` SÍ trae el texto crudo que mandó el LLM. Ése es el
patrón viejo (registrar_gasto_rapido en TuFacturaIA v2 lo usa, pero ese
nodo se creó pre-2.15 — quizá funciona por compat). Para tools nuevos:

```js
let params = {};
try {
  const item = $input.first();
  if (item?.json && typeof item.json === 'object' && !Array.isArray(item.json)) {
    params = { ...item.json };
  }
} catch (e) {}
// Fallback a query string solo si llega como string
if (Object.keys(params).length === 0 && typeof query === 'string' && query.length > 0) {
  try { params = JSON.parse(query); } catch (e) {}
}
```

Síntoma del bug: el output de inputOverride del nodo muestra el JSON
correcto que el LLM mandó, pero el código devuelve `nombre_required`
porque parsea `query` y siempre obtiene `{}`.

Ver [[$fromAI-en-toolCode-lanza-no-execution-data-available-en-n8n-2.15.x]].
