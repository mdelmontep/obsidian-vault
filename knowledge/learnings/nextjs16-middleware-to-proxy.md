---
title: next.js 16 renombra middleware.ts a proxy.ts
date: 2026-04-27
source: claude-code-session
tags: [nextjs, next16, middleware, proxy]
---

## Cambio
Next.js 16 depreca `middleware.ts` en favor de `proxy.ts`.
El archivo viejo sigue funcionando con warning en build.

## Migración
1. Renombrar `src/middleware.ts` → `src/proxy.ts`
2. Cambiar el export: `middleware` → `proxy`
3. El `config` con `matcher` permanece igual

```ts
// proxy.ts
export async function proxy(request: NextRequest) { ... }
export const config = { matcher: [...] }
```
