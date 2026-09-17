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

## ⚠️ NO revertir a `middleware.ts`

**Caso real 2026-05-20**: ante un Forbidden en endpoint que dependía de cookie `impersonate_org`, asumí erróneamente que Next.js 16 había dejado de invocar `proxy.ts` y reverté el rename. **Falso**: `proxy.ts` es la convención correcta v16; `middleware.ts` solo sigue activo por backcompat con deprecation warning. La causa real era otra (override semantics + cookie con maxAge 1h). Ver [[nextjs16-impersonation-cookie-stuck-no-implica-middleware-off]].

## ⚠️ En la RAÍZ con `src/` no se carga — y falla en silencio

**Medido 2026-09-17 (agency-portal, prod).** `proxy.ts` estaba en la raíz del repo y el proyecto usa
`src/`: Next no lo invoca nunca. No hay warning ni error; el síntoma es indirecto —las rutas protegidas
siguen redirigiendo a `/login` porque los guards de servidor tapan el agujero, pero **sin el `next=`**
que el proxy añadía—, así que quien llega desde un enlace externo acaba en `/` tras loguearse.
Tell de 5 segundos, sin leer código: `curl -sI <ruta protegida> | grep location`; si sale `/login` a
secas en TODAS las rutas, el proxy no corre. Va junto a `app/`: con `src/`, en `src/proxy.ts`.
