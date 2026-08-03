---
title: el hueco «libre» de migraciones puede estar ya ocupado en producción
date: 2026-08-03
source: claude-code-session
tags: [supabase, migraciones, facturaia, sesiones-paralelas]
---

`npm run mig:renumerar` calcula el destino como **máximo ocupado + 1 contando
`origin/main` y lo local**. No pregunta a la base. El 3-ago mi rama iba a la 630
y prod ya tenía aplicadas la **630–636**: una sesión paralela (worktree
`wt-dto-fabricante`, obras-095) las había aplicado desde su rama sin mergear
todavía — que es justo lo que manda hacer «migración antes que merge».

Si llego a empujar la 630, `db push` la habría dado por aplicada **por versión**
y se la salta sin error: prod sin mi tabla y el push diciendo que todo al día.

Antes de fijar el número, mirar la BD, no solo el repo:

    supabase migration list --linked   # filas con local:"" = aplicadas sin fichero

Ahí se ve el rango real ocupado. Y si `db push` responde *«Remote migration
versions not found in local migrations directory»*, **no ejecutar el
`migration repair --status reverted` que sugiere**: mentiría sobre prod. Copiar
temporalmente (sin commitear) los `.sql` de la sesión paralela deja pasar la
comprobación y solo empuja lo tuyo — confirmar con `--dry-run` que la lista es
exactamente tu fichero.

Segunda trampa, para quien tenga la rama paralela: si renumeran antes del merge,
su SQL **ya aplicado** como 630-636 se reaplicaría con números nuevos.

Ver [[dockerfile-que-lista-modulos-uno-a-uno-mata-el-servicio-sin-fallar-el-build]]
