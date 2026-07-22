---
title: next.js 16 revalidatetag exige un segundo argumento (perfil de cachelife)
date: 2026-07-22
source: claude-code-session
tags: [nextjs, cache-components, use-cache, typescript]
---

En Next 16, `revalidateTag(tag)` con un solo argumento da `TS2554: Expected 2
arguments, but got 1`. La firma cambió a `revalidateTag(tag, profile)`, donde
`profile` es el nombre del perfil `cacheLife` usado en el `'use cache'`
correspondiente (`'seconds'`, `'minutes'`, un perfil custom de
`next.config.ts`) o un objeto `{ expire: 0 }` para expirar YA en vez de
quedar "stale" (SWR).

**Gotcha real**: en un refactor con 15+ call-sites de `revalidateTag` (todos
copiados del mismo patrón), si el primero se escribe sin el 2º argumento, el
error se repite en TODOS. El gate de pre-commit (typecheck) lo bloquea en
bloque — no lo trates como 15 fixes independientes, es 1 patrón que hay que
corregir con sed/Edit en todos los sitios a la vez.

Sin el 2º argumento explícito y correcto, el tag queda en modo SWR (sigue
sirviendo el valor viejo un tiempo) en vez de expirar inmediato — crítico en
dominios donde "dato viejo tras mutar" es un bug de negocio, no cosmético.
