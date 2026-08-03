---
title: un recurso de test con nombre constante no aísla entre procesos
date: 2026-08-03
source: claude-code-session
tags: [testing, postgres, worktrees, ci, flaky]
---

Ocho `.pg` creaban su BD con `const BOOT_DB = "agh_boot_test"` + `DROP DATABASE ... WITH (FORCE)`. Los comentarios la llamaban «dedicada y efímera»: **cierto por separado** (se borra al salir; no es la BD de trabajo) y **falso en conjunto** — un nombre constante lo comparten todos los procesos a la vez. Distingue de OTRA SUITE, no de OTRO PROCESO corriendo la misma.

Y la mitigación habitual **no cubre**: apuntar `DATABASE_URL` a una BD por sesión no sirve si el nombre auxiliar no se deriva de esa URL.

El síntoma no se parece a la causa y varía: carrera en el `CREATE` (`duplicate key ... pg_database_datname_index`, ~4 s) o bloqueo en el `DROP` esperando el lock ajeno (~10 s = timeout de un **HOOK** de vitest, no del test). Por eso se lee como «el gate oscila» y sobrevive meses. Aparece en PRs sin camino causal al fichero que falla.

**Fix:** derivar el nombre de lo que separa a los actores reales — el **worktree** (hash de la ruta), no el pid: el pid estrena nombre cada corrida y deja huérfanas si el proceso muere sin limpiar; el worktree reusa y su `DROP IF EXISTS` recoge lo anterior.

**Prueba, no razonamiento:** lanzar dos corridas concurrentes y comparar exit codes. Si fallan LAS DOS, es determinista, no un flake — «nunca me ha pasado» solo significa que los relojes no se cruzaron.

Ver [[gh-pr-merge-delete-branch-falla-local-si-main-en-otro-worktree]] · [[triaje-seguro-ramas-worktrees-sesiones-paralelas]]
