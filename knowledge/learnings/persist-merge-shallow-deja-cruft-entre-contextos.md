---
title: persist merge shallow deja cruft entre contextos
date: 2026-05-18
source: claude-code-session
tags: [api, state, supabase, gotcha]
---

Endpoints de state machine que hacen `UPSERT` con merge shallow `{...existing, ...incoming}` contaminan al cambiar de contexto. Caso real: bot WhatsApp con `chat_state` JSONB. Sesión A deja `draft={...}` y `current_view='awaiting_confirmation'`. Sesión B nueva persiste `last_listado={...}` con `current_view='mostrando_listado'`. Resultado:

```
{ draft: {sesión A}, last_listado: {sesión B}, current_view: 'mostrando_listado' }
```

El LLM ve ambos y se confunde sobre cuál es el contexto activo.

**Fix**: en el cliente, al cambiar de contexto, enviar campos viejos como `null` explícito en el `state_json`. El merge shallow del endpoint sobreescribe:

```
state_json: { last_listado: {...}, draft: null, current_doc: null, resolved_slot: null }
```

Simétrico al guardar draft: nullear `last_listado` y `resolved_slot`.

Alternativa más limpia: endpoint con modo `replace` además de `merge`. Pero requiere ampliar contrato.

Ver [[slot-resolver-deterministic-pre-llm-nlu-regex-espanol]]
