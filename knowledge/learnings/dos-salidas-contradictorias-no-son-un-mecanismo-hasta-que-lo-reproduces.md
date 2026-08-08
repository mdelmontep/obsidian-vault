---
title: dos salidas contradictorias no son un mecanismo hasta que lo reproduces en un repo de prueba
date: 2026-08-08
source: claude-code-session
tags: [metodo, git, worktrees, verificacion, hooks]
---

`git stash show --stat "stash@{0}"` me dio **1 fichero** desde un worktree y **5 distintos** desde el
repo raíz. De ahí inferí «`refs/stash` es por worktree y `worktree remove` se lo lleva», y con esa
frase escribí un learning, una entrada en `hot.md`, una nota de proyecto, un mensaje de hook y estuve
a punto de shipear la regla. **Todo falso.** Un repo de prueba de 60 segundos lo refutó:

- `refs/stash` vive en el `.git` COMÚN (`.git/refs/stash`), compartido por todos los worktrees.
- Un stash creado en un worktree **se ve desde la raíz**.
- `git worktree remove --force` **NO lo destruye** (git 2.50.1).

Y lo que observé sigue **sin explicación**: el reflog de `refs/stash` no muestra ningún drop y los
índices no se movieron. Dejarlo como «no lo sé» es la única postura honesta; inventar el mecanismo es
lo que casi convierte una anomalía en cuatro documentos y un hook que mienten.

**La regla**: una anomalía justifica investigar, no publicar. Antes de escribir «X funciona así» —y
mucho más antes de convertirlo en hook— reprodúcelo en un repo desechable donde controles las
variables. Barato, rápido y es lo único que distingue un mecanismo de una coincidencia.

Lo que SÍ sobrevivió de todo aquello, porque estaba medido: `worktree remove --force` borra los
cambios sin commitear sin recuperación posible (tres tracks de agentes, 7-ago). Eso es la regla 6 de
`git-guard.sh`, con sus cinco casos en la suite. Ver [[claude-code-agentes-worktree-failure-modes]]
