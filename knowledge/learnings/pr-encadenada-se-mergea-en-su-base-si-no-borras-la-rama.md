---
title: una PR encadenada se mergea en su BASE, no en main, si no borras la rama base al mergear la primera
date: 2026-07-27
source: claude-code-session
tags: [git, github, gh-cli, stacked-prs, verificacion]
---
Con dos PRs apiladas (B sale de la rama de A), GitHub **solo reapunta B a `main` si la rama de A se BORRA** al mergear A. Si mergeas A con `gh pr merge --squash` sin `--delete-branch`, la rama sigue existiendo y B **se mergea dentro de ella**: sale `MERGED`, con su commit y todo, y **no está en `main`**.

Caso real (agh-iberica, 2026-07-27): PR #597 quedó «mergeada» dentro de `fix/584-…`. Lo detecté porque `git show origin/main:<fichero> | grep -c <símbolo del fix>` daba **0**. Nadie más lo habría notado hasta echar en falta la conducta en prod.

**Reglas:**
- Mergear siempre con `--delete-branch`, o `gh pr edit <B> --base main` **antes** de mergear A.
- Tras cada merge, verificar en el destino, no en el estado de la PR: `git show origin/main:<fichero> | grep -c <símbolo>`. «MERGED» no significa «en main».
- Al rescatar: **no** mergees la rama base a `main` por atajo — si nació antes de otro merge, arrastra la AUSENCIA de ese trabajo y lo revierte (aquí habría borrado el fix de #587). Cherry-pick del commit sobre `main` al día, gate, PR nueva.
- `--delete-branch` falla si un worktree tiene la rama: es benigno (el remoto ya se borró), pero **rompe una cadena con `&&`** y el segundo merge no se ejecuta. Verificar uno a uno.

Ver [[triaje-seguro-ramas-worktrees-sesiones-paralelas]] · [[stash-es-compartido-entre-worktrees-y-rompe-sesiones-paralelas]]
