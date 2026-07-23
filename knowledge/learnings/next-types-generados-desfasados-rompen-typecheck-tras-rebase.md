---
title: next .next/types desfasados rompen typecheck tras rebase (cacheLife custom)
date: 2026-07-23
source: claude-code-session
tags: [nextjs, typescript, ci]
---
Next 16 (cacheComponents) genera tipos en `.next/types` durante `next build`/`dev`, incluidos los perfiles `cacheLife` custom de `next.config.ts`. Si haces rebase/pull que añade un perfil nuevo (`cacheLife('dashboard')`) y corres `tsc --noEmit` SIN build previo, typecheck falla con TS2769 ("no overload matches") en código que en CI pasa — parece main roto y no lo es.

Fix: `npm run build` primero (regenera `.next/types`) y typecheck después. Señal para reconocerlo: el error apunta a `cacheLife('<perfil-custom>')` y desaparece tras build. No parchear el código ni castear.
