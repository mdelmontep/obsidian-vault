---
title: `??` no cubre env vacía — Number("") es 0 y rompe el default
date: 2026-05-30
source: claude-code-session
tags: [javascript, env-vars, gotcha, nullish-coalescing]
---

Patrón roto, frecuente:

  `Number(process.env.FOO ?? 500)`

Si `FOO=""` (declarada vacía en Dockerfile/Dokploy/`.env.example`), el
nullish coalescing NO la considera nullish — coalesce solo cubre `null`
y `undefined`. Resultado: `Number("") === 0`. Si el código usa esa
variable como umbral, TTL, retry count, max size, etc., toda la lógica
colapsa.

Aplica también a `parseInt`/`parseFloat` (devuelven NaN para `""`,
mejor) y al chiste clásico distinto `Boolean("0") === true`.

Fix: helper defensivo que rechaza string vacía, NaN, Infinity y ≤0 para
magnitudes positivas:

```ts
function parseNumEnv(raw: string | null | undefined): number | null {
  if (raw == null || raw === '') return null
  const n = Number(raw)
  return Number.isFinite(n) && n > 0 ? n : null
}
const value = parseNumEnv(process.env.FOO) ?? DEFAULT
```

Caso real TuFacturaIA: panel `/admin/system?tab=storage` mostró
"Umbral aviso 0 MB" con todas las orgs en rojo. PR #120.
