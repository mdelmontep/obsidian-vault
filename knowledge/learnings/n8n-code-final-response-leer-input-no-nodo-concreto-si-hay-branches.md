---
title: n8n Code final response — leer $input, no $('NodeX'), si hay ramas con cortocircuito
date: 2026-05-22
source: claude-code-session
tags: [n8n, code-node, branches]
---

`$('Shape result').first().json` crashea si `Shape result` no se ejecutó (caso típico: rama de cortocircuito por dry_run, error temprano, validation fail). El error es opaco: `Cannot read properties of undefined`.

Patrón seguro en nodos de respuesta final que reciben input de múltiples ramas:

```js
const inp = $input.first().json || {};
if (inp._short_circuit === true) {
  const { lock_key, ...pub } = inp;
  return [{ json: pub }];
}
try {
  const r = $('Shape result').first().json;
  return [{ json: r }];
} catch(e) {
  return [{ json: inp }];
}
```

Caso real Elphis 2026-05-22: `clientify-upsert-contact` Final response leía `$('Shape result')` y devolvía `[{}]` (output vacío) en path dry_run, rompiendo el caller upstream que esperaba contact_id.
