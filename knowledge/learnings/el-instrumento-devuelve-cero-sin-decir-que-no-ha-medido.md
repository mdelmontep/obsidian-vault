---
title: el instrumento devuelve cero sin decir que no ha medido
date: 2026-08-16
source: claude-code-session
tags: [shell, zsh, git, metodo, instrumentacion]
---

Tres veces en una sesión, tres mecanismos distintos, el mismo resultado: un barrido devolvió
un número plausible **sin haber medido nada**, y ninguno dio error.

- `git grep -E '^\s*(it|test)\('` → **0 coincidencias**. La ERE de `git grep` **no soporta `\s`**
  y no avisa. Con `-P`, 4473. (`[[:space:]]` también vale.)
- Clasificador de ramas: `files=$(git diff --name-only …)` y luego `git diff A B -- $files`.
  **zsh NO divide en palabras una variable sin comillas** (bash sí), así que los 13 ficheros
  viajaban como **un solo pathspec** con saltos de línea → diff vacío SIEMPRE → «todo mergeado».
  Fix: `files=("${(@f)$(…)}")` y `-- "${files[@]}"`.
- `git show $b:test/x.ts` → `:t` es un **modificador de zsh** (basename) y se comió el nombre.
  Fix: `${b}:test/x.ts`.

**Regla**: todo barrido lleva **control en las dos direcciones** antes de creerse su resultado —
un caso que DEBE salir y otro que NO debe. Aquí lo destapó el control negativo: una rama que yo
sabía con trabajo fuera salía clasificada como «dentro». Hermano de
[[el-bucle-que-espera-con-pgrep-se-encuentra-a-si-mismo]] y de
[[el-exit-code-que-lees-no-es-el-del-comando-que-te-importa]].
