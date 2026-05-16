---
title: Throw top-level en route.ts crashea build Next.js durante page-data collection
date: 2026-05-16
source: claude-code-session
tags: [nextjs, build, gotcha, ssg]
---

Si un `app/.../route.ts` tiene `throw new Error(...)` o `if (!env) throw` en el módulo (fuera del handler), el build de Next.js falla con:

```
Error: Failed to collect page data for /api/v1/openapi.json
```

Next.js evalúa cada route durante la fase "Collecting page data" (incluso si la ruta es 100% dinámica). Cualquier excepción al cargar el módulo aborta el build entero.

**Patrón roto**:
```ts
const URL = process.env.NEXT_PUBLIC_X
if (!URL) throw new Error('NEXT_PUBLIC_X no configurada')
const spec = { ..., servers: [{ url: URL }] }
```

**Fix A (fallback)**: `const URL = process.env.NEXT_PUBLIC_X || 'https://default.example'`. Hace build sin la env, runtime usa la real cuando esté.

**Fix B (lazy)**: mover el check dentro del handler:
```ts
export async function GET() {
  const URL = process.env.NEXT_PUBLIC_X
  if (!URL) return new Response('config error', { status: 500 })
  ...
}
```

Universal a Next.js 13+. Especialmente cuando Docker cache de build se invalida y el primer rebuild real expone el bug latente.
