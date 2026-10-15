---
title: antes de abrir un arreglo, mira si otro worktree ya toca ese fichero
date: 2026-10-15
source: facturaia
tags: [metodo, paralelo, worktrees, sesiones-paralelas]
---
Durante una QA encontré un defecto visual (fechas de la barra de albaranes de venta) y lo arreglé
en un PR propio: revisión de cierre, QA en prod a cinco anchos, artifact y test con mutación.
Otra sesión llevaba el MISMO arreglo, más completo, en una rama sin PR (#3416). Lo cazó el
orquestador del tren, no yo. Mi PR se cerró como duplicado; solo se salvó el test.

Buscar PRs abiertos no basta: el trabajo vivo está en ramas sin PR y en cambios sin commitear.
Antes de abrir el arreglo, recorre los worktrees mirando el fichero:

`for w in $(git worktree list --porcelain | awk '/^worktree/{print $2}'); do (git -C $w diff --name-only origin/main...HEAD; git -C $w status --porcelain) | grep -q <ruta> && echo $w; done`

Si sale otro, pregunta a esa sesión antes de escribir una línea. Ver
[[una-ventana-de-coordinacion-se-dispara-por-fichero-no-por-reloj]].
