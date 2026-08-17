---
title: correr la suite filtrada por las carpetas del PR no ve los guards de arquitectura
date: 2026-08-17
source: claude-code-session
tags: [testing, ci, guards, gate, gotcha]
---

Un repo con trinquetes (tests que vigilan reglas globales: "nadie parsea importes a
mano", "cada cron del registro tiene handler") los guarda **fuera** de la carpeta del
código que vigilan — por diseño, porque vigilan a todo el repo. Correr `vitest <carpetas
del PR>` para ir rápido los salta **todos**, y cada PR sale verde.

Medido el 17-ago (TuFacturaIA, ola 4 del empaquetado): 5 PRs mergeados con su gate
individual en verde; la suite completa sobre `main` ya mergeado destapó dos regresiones
reales, una de negocio (un precio de 3.060,50 € que se guardaba como 3,06 €, ver
[[replace-coma-punto-solo-sustituye-la-primera-y-rompe-los-millares]]) y otra de cableado
(dos crons sin `case` en su `loadHandler`). El `pre-push` tampoco las veía: corre lint,
typecheck y build, no la suite.

**Regla**: el gate de una RAMA puede filtrarse; el cierre de una TANDA no. Tras mergear,
`lint && typecheck && build && vitest` completo sobre `main` actualizado, antes de dar la
sesión por cerrada. Con PRs encadenados el rojo aparece en la composición, no en las
piezas.
