---
title: n8n langchain toolCode — usar $fromAI() para args, no `query` ni $input
date: 2026-05-30
source: claude-code-session
tags: [n8n, langchain, gotcha, toolcode, fromAI]
---

API canónica para leer args del LLM en `@n8n/n8n-nodes-langchain.toolCode`
con `specifyInputSchema:true + schemaType:'manual' + inputSchema` JSON
Schema: **`$fromAI(campo, descripcion, tipo)`** por cada campo del schema.

```js
const nombre = $fromAI('nombre', '', 'string');
const nif = $fromAI('nif', '', 'string');
```

**Por qué `query` falla**: en n8n langchain moderno (≥2.x verificado en
n8n.tufacturaia.com 2026-05-30), `query` llega como **objeto JS** ya
parseado, no como string. Patrones viejos `JSON.parse(query)` lanzan o
devuelven `{}` porque `typeof query === 'object'`.

**Por qué `$input.first().json` confunde**: contiene los args del tool
**mezclados** con el item del workflow upstream (chatInput, sessionId,
org_id, etc.). Funciona si filtras por clave, pero es frágil — colisión
si el schema tiene un campo llamado `org_id` o `sessionId`.

Envolver `$fromAI()` en try/catch — algunos forks reportan que lanza si
el campo está vacío.

```js
const safe = (k) => { try { const v = $fromAI(k,'','string'); return v == null ? '' : String(v).trim(); } catch { return ''; } };
```

Confirmado en runtime: el debug dump mostró `$fromAI('nombre','test','string')`
→ `"Hifly Madrid s.l."` ✓. Mantener `specifyInputSchema:true` con el
JSON Schema declarado — `$fromAI` lo lee de ahí.

Ver [[$fromAI-en-toolCode-lanza-no-execution-data-available-en-n8n-2.15.x]]
(versión vieja donde lanzaba; este learning aplica a la versión actual).
