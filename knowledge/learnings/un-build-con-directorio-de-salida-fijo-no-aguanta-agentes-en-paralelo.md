---
title: un build con directorio de salida fijo no aguanta agentes en paralelo
date: 2026-09-05
source: mandadm
tags: [nextjs, subagentes, gates, harness]
---

Varios agentes corriendo el gate a la vez sobre el **mismo working copy** dan `ENOENT` intermitentes
en `next build`: una corrida borra y reescribe `.next` mientras otra lo lee. El error no distingue
«código roto» de «dos builds solapados», así que se depura el sitio equivocado.

Fix: `distDir` por corrida. En `next.config.mjs`, `distDir: process.env.MDM_NEXT_DIST_DIR ?? '.next'`,
y el runner exporta `.next-gate-$$-$RANDOM` y lo borra en su trap. Vale igual para cualquier build con
salida fija (`dist/`, `build/`, `coverage/`).

Tres colas que trae detrás, medidas:
- El `ignores` del lint hay que ampliarlo a `**/.next*/**`, o el primer build paralelo mete miles de
  ficheros generados en el lint.
- Next **parchea `apps/web/tsconfig.json`** metiendo el `distDir` en `include` en cada corrida: se
  acumulan globs muertos. El runner hace copia y la restaura en el trap.
- Sin `outputFileTracingRoot` en un monorepo, el build ni siquiera es determinista entre corridas.

Corolario general: **no midas un sistema mientras otro agente lo mueve.** Tres «rojos» que reporté en
esta horda eran un `mutate` de otro agente corriendo a la vez. El gate final se corre con todos parados.
Ver [[editar-un-script-en-caliente-rompe-las-corridas-en-curso]] · [[la-suite-completa-bajo-paralelismo-no-distingue-regresion-de-saturacion]]
