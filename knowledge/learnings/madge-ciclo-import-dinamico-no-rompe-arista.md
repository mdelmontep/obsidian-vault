---
title: madge sigue imports dinámicos y de tipo — para romper un ciclo elimina la arista estática
date: 2026-06-27
source: claude-code-session
tags: [typescript, madge, arquitectura, dependencias]
---

`npm run deps:circular` (madge) sigue **tanto `import type`** (aunque TS lo borre en compilación) **como `await import()` dinámico**. Consecuencias al romper un ciclo:

(a) Un back-edge **solo-de-tipo** cuenta como ciclo. Fix: define el tipo en el módulo hoja y re-expórtalo desde el wrapper (`export type { X } from './hoja'`), no al revés.

(b) Cambiar un `import` estático por `await import()` **NO rompe el ciclo en madge** (perdí un intento probándolo). Hay que eliminar la arista de verdad: si A (bajo nivel) importa B (registry) solo por una función que en realidad vive en módulos hoja C, crea un módulo intermedio (un mapa/índice) que A importe en vez de B.

(c) **Matiz (2026-07-27)**: madge sigue el `await import()` solo si la ruta es un string estático. Con **template literal** (`import(\`@/components/templates/template-${tid}\`)`) la arista es INVISIBLE para madge y para `tsc` — renombrar el destino no rompe ni el grafo ni el build, revienta en runtime. Fix: mapa explícito `satisfies Record<Id, () => Promise<T>>`, que además obliga a registrar cada id nuevo o falla el typecheck. Si el grafo dice que una capa está limpia, comprueba antes que no haya `import()` con parte variable.

Caso real facturaia 2026-06-27 (4→0 ciclos): `tokens.ts` dejó de importar `registry` (que arrastraba providers→actions→tokens) vía un nuevo `refreshers.ts` que mapea slug→refresher importando directo de los `providers/*/oauth.ts` (hojas). Y `TimelineSeries`/`Registro349Fila` movidos al archivo hoja + re-export.
