---
title: un fail-closed cuenta la fuente que puede fallar, no el total agregado
date: 2026-08-15
source: claude-code-session
tags: [gates, testing, mutacion, tucrmia]
---
Al poner un candado «cero elementos mirados es ROJO», el umbral tiene que ir sobre **la fuente que la
avería rompería**, no sobre la suma de todas.

Caso: un gate recorría ficheros de test (~377) + los `setupFiles` de vitest (1). El fail-closed se
escribió como `total === 0`. Roto el filtro de tests a propósito, el recorrido **seguía devolviendo 1**
—el setup entra por otra puerta— así que el candado no disparó: **mutación sin víctima**, indistinguible
de un candado que funciona.

Fix: contar las fuentes por separado y poner el umbral en la que importa (`ficherosDeTest === 0`).

Y la regla de método, que es lo que hay que llevarse: **no basta con que la mutación ponga rojo — tiene
que ponerlo por el motivo que dices**. Aquí no disparó; en otro caso del mismo día disparó por una razón
distinta a la vigilada. Los dos se leen igual desde el código de salida.

Ver [[un-gate-que-exige-n-claves-se-apaga-trayendo-el-resto-con-spread]] · [[guard-de-migracion-que-recalcula-la-formula-no-verifica-nada]].
