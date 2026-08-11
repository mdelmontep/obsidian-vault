---
title: n8n HTTP Request sin responseFormat json explícito devuelve el body como string en .data
date: 2026-08-12
source: claude-code-session
tags: [n8n, http-request, gotcha]
---
Un nodo `httpRequest` sin `options.response.response.responseFormat: "json"` explícito, contra una
API que sí devuelve JSON, no siempre lo autodetecta y parsea — a veces entrega el body crudo como
STRING dentro de un campo `data` (`{json: {data: "{\"id\":123,...}"}}`) en vez de `{json: {id:123}}`
directo.

Síntoma: un Code node que hace `$json.custom_fields_values` o similar da `undefined` sin error — el
campo real está en `$json.data` (string) y hay que `JSON.parse` primero. Pasó dos veces en la misma
sesión (Simarro): en `Reconcile lead_preferences` (ya lo manejaba con un parche) y en un nodo nuevo
que no lo esperaba, dando falsos negativos (`tieneInfo:false` con datos reales guardados).

Fix: `let body = $json.data !== undefined ? $json.data : $json; if (typeof body === 'string') body
= JSON.parse(body);` antes de leer cualquier campo. Mejor aún: fijar `responseFormat: "json"`
explícito en el nodo para no depender de la autodetección.
