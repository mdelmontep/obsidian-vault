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

**La hermana, 30-ago (agentesia-crm)**: el mismo silencio por el otro lado — `className={s.resto}`
con `.resto` **ausente de la hoja**. El valor es `undefined`, React omite el atributo y el elemento
sale con los estilos por defecto del navegador. No lo ve el compilador (no hay tipos de la hoja), ni
el linter de CSS (mira lo que la hoja DECLARA), ni un gate de tokens (mira que cada `var(--x)` exista):
ninguno cruza las dos mitades. **Detección barata**: por cada `import s from './x.module.css'`, cruzar
los `s.loQueSea` contra los selectores `.clase` de esa hoja. En un árbol de 110 componentes tardó
segundos y encontró el único caso, que era el que acababa de entrar.
