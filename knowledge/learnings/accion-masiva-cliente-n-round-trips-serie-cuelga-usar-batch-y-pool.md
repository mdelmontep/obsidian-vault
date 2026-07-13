---
title: acción masiva en cliente con N round-trips en serie cuelga la UI — batch + pool + progreso
date: 2026-07-13
source: claude-code-session
tags: [frontend, supabase, ux, performance]
---
Una acción en lote que en el cliente hace `for (item of items) { await query }` con 1-2
round-trips por ítem escala fatal: 96 facturas × (SELECT+UPDATE) = 192 llamadas en serie
→ ~1 min de "botón pensando" sin señal. No es falta de feedback, es el patrón de red.

Fix en tres capas:
- **Lectura**: una sola query `... .in('fk', ids)` + `Map` por id, no N selects.
- **Escritura**: si TODAS van al mismo valor → un `UPDATE ... .in('id', ids)`. Si cada una
  difiere → pool de concurrencia acotada (~6 en vuelo), no `Promise.all` sin límite ni serie.
- **Progreso**: contador `N/total` + relleno del propio botón (CSS `::before` con `width:
  var(--pct)`); incrementar dentro del worker del pool.

Reutiliza el helper de concurrencia si ya existe (no dupliques) y súbelo a `lib/` si vive
enterrado en `_parts/` de otra feature. Ojo optimistic-update: marca solo los ids con `ok`,
no todos. Ver [[fire-and-forget-resultado-descartado-esconde-fallo-loguear-en-transporte]].
