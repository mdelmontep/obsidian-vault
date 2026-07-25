---
title: un Server Component que toca la BD en su cuerpo se prerenderiza y tumba el build entero
date: 2026-07-25
source: claude-code-session facturaia
tags: [nextjs, cache-components, build, gates, prerender]
---

Bajo Cache Components (Next 16), una página que llama a su cliente de BD **en el cuerpo del Server
Component** y no declara nada se prerenderiza estática: ese cliente corre en build-time. Sin env de
Supabase en local (y `.env.local` no está en el repo, son secretos) el build muere con
`supabaseUrl is required` y **se lleva por delante el build completo**, no solo esa ruta.

Caso real: `/admin/onboarding` (panel de funnel). Fix de una línea, `await connection()` antes de
tocar el admin client, que difiere a request-time. Patrón ya establecido en el repo
(`(dashboard)/fiscal/page.tsx`). La ruta pasa de estática (`○`) a partial prerender (`◐`).

**Dos lecciones que valen más que el fix:**

1. **Prerenderizar un dashboard en vivo es incorrecto de negocio, no solo un fallo de build**: los
   conteos quedarían congelados al momento del build. Si el fallo no hubiese existido, el bug seguiría.
2. **Un gate que no se puede satisfacer se bypasea siempre y deja de defender.** El `pre-push` exige
   build verde, así que con esto NADIE podía empujar sin `--no-verify` desde ningún checkout. Antes de
   asumir "el gate está roto para mí", correrlo en el checkout principal: si también falla ahí, el gate
   está caído para todo el equipo y eso es el bug a arreglar.

Detalle del hook a tener presente: el `pre-push` corre `npm run build` sobre **el árbol de trabajo del
cwd**, no sobre los commits que empujas → empujar una rama desde otro directorio da un verde falso.
Ver [[defensa-cableada-vs-codigo-muerto]] · [[actions-sin-billing-hooks-locales-unico-gate]]
