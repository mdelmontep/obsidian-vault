---
title: supabase-js embed via FK tipa array pero runtime devuelve objeto
date: 2026-05-02
source: claude-code-session
tags: [supabase, typescript, gotcha]
---

`.select('cliente:clientes(id, nombre)')` con FK simple many-to-one (la tabla padre tiene FK a la hija):

- **Runtime**: devuelve **objeto único** `{id, nombre}` o `null`.
- **TypeScript**: lo tipa como **array** `{id, nombre}[]` porque supabase-js no infiere cardinalidad sin metadata del schema.

Resultado: `data.cliente.id` falla typecheck con `error TS2352: Conversion of type '{...}[]' to type '{...}' may be a mistake`.

Fix defensivo (sobrevive cualquier cambio futuro de comportamiento):
```ts
const raw = data.cliente as
  | { id: string; nombre: string }
  | { id: string; nombre: string }[]
  | null
const embed = Array.isArray(raw) ? (raw[0] ?? null) : raw
```

Aplica también a presupuestos, quotes, contracts — cualquier embed por FK simple. No usar `as unknown as X` directo, no documenta la dualidad runtime/types.
