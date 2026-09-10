---
title: plegar una columna solo sirve si el ancho que libera hace caber al vecino
date: 2026-09-10
source: agency-portal
tags: [css, layout, frontend, ux]
---
Un botón de plegar puede funcionar —el estado cambia, la URL lo guarda, el aria lo
dice— y no cambiar NADA de lo que se ve. Pasó en la Pizarra: con la agenda plegada,
los cuatro carriles seguían recortados y con el mismo scroll.

Dos causas, las dos se miden y ninguna se razona:

- **Una pista `1fr` colapsada sigue comiendo su parte.** Plegar dentro de
  `grid-cols-N` no devuelve ancho a nadie; hay que pasar la fila a flex con `min-w`
  por columna, y entonces la plegada sí lo suelta.
- **El mínimo del vecino tiene que caber en el hueco liberado.** Real: 1512 de
  viewport − 280 de sidebar = 1127 de contenido; agenda abierta deja 848, plegada
  1092. Con `min-w:17rem`, 4×272+36 = 1124 > 1092 → plegar era inerte. A 16rem,
  4×256+36 = 1060 ≤ 1092 → entra.

Se mide con `clientWidth`/`scrollWidth` de la fila en el navegador, no sumando CSS:
[[la-maqueta-se-mide-con-el-motor-no-se-modela-sumando-anchos]].
