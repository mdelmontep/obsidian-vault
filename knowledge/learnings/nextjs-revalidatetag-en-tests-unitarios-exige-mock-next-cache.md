---
title: revalidatetag en route handlers rompe tests unitarios sin mockear next/cache
date: 2026-07-23
source: claude-code-session
tags: [nextjs, cache-components, vitest, testing]
---

`revalidateTag`/`updateTag`/`cacheTag`/`cacheLife` exigen el "static
generation store" (AsyncLocalStorage) que Next.js monta por-request en
runtime real. Un test unitario que invoca el handler de un Route Handler
directamente como función (sin pasar por el servidor de Next) no tiene ese
store → `Invariant: static generation store missing in revalidateTag`.

**No es un bug de producción** — en el servidor real (dev o prod) el store
siempre existe. Verificable comparando con QA manual en un dev server real:
si ahí funciona sin error, el fallo es solo del entorno de test.

**Fix**: mock global en el setup de tests (`vi.mock('next/cache', ...)`
devolviendo no-ops para `revalidateTag`/`cacheTag`/`cacheLife`, spreadeando
el resto del módulo real vía `importOriginal`). No verifica QUÉ se invalida
— eso lo cubre QA manual o un test de integración aparte — solo evita que
la ausencia de runtime rompa tests que no tienen nada que ver con caché.

**Antes de asumir que X tests rotos son culpa de tu PR**: compáralos contra
el mismo run en el commit inmediatamente anterior (worktree limpio). Si el
conteo y los archivos son idénticos, son preexistentes, no tuyos.
