---
title: usar el nombre de una clase de CSS Modules como string global da un selector muerto, sin error
date: 2026-08-04
source: claude-code-session
tags: [css, css-modules, frontend, skeleton]
---
`className="kpi-card"` (string literal, global) no coincide con nada si `kpi-card` es en realidad el
nombre de una clase dentro de `kpi-card.module.css` — CSS Modules la hashea (`kpiCard_x7f2a`), así que
el selector real nunca existe en `globals.css`. No hay error de build ni de lint: el elemento se monta
sin fondo/borde/padding, solo el contenido interno visible, y se lee como "mal alineado" o "apelmazado"
en vez de "sin estilo". Pasó en `SkeletonKPIs` (`ui/skeleton.tsx`): la card de esqueleto llevaba meses
sin caja porque nadie comparó visualmente contra la card real con `--brand` en foco.

**Detección**: `grep -n "kpi-card" globals.css tokens.css` sin resultado con className y con resultado
solo en comentarios que citan un `.module.css` → confirma que es un module, no una clase global.
**Fix**: usar la clase global que SÍ existe (aquí `kpi`), o convertir el consumidor a leer el mismo
`.module.css` real en vez de adivinar el nombre.
