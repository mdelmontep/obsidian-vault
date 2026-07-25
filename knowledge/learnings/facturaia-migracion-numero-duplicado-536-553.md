---
title: migración con número duplicado se cuela cuando ramas paralelas mergean el mismo hueco
date: 2026-07-24
source: claude-code-session
tags: [facturaia, migraciones, supabase, git]
---

PR #1111 (`536_...`) vs #1114 (`536_...`) Y, la MISMA tarde, PR #1199
(`553_...`) vs #1111 ya renumerada a `553_...` — 2 choques el mismo día.
Causa: la convención numera "al abrir el PR", no al crear rama; si dos
ramas abren casi a la vez, ambas ven el mismo hueco libre.

Fix manual cada vez: `git mv` al primer hueco tras el máximo actual (no
huecos históricos antiguos) + `grep -rn "mig NNN"` para actualizar solo
las referencias cruzadas del propio archivo (ojo con otros usos del mismo
número en comentarios de código no relacionados).

**Fix sistémico 2026-07-24**: `.githooks/pre-push` ahora aborta el push si
detecta el mismo prefijo `NNN` en dos archivos distintos (local ∪
`origin/main`). Límite conocido: no cubre 2 ramas pusheadas ANTES de que
cualquiera mergee (el número aún no está en `origin/main`) — solo el
momento de rebase/push posterior al primer merge, que es cuando se
detectó en los 2 casos reales de hoy.

**Tercer choque (2026-07-25, PR #1202 con 555/556 → 559/560)**: el hook FUNCIONÓ y
abortó el push. Coste real de renumerar: 13 ficheros, porque las referencias
`mig NNN` viven en comentarios de código y tests, no solo en el SQL. Trampa propia de
este caso: las OTRAS ramas habían mergeado también una 555 y una 556, así que un
`sed` global de "mig 555" habría corrompido SUS referencias. Hay que reemplazar
fichero a fichero comprobando de qué migración habla cada mención.
