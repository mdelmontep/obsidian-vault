---
title: git mv sobre archivo untracked falla pero renombra igual
date: 2026-07-01
source: claude-code-session
tags: [git, gotcha]
---

`git mv origen destino` sobre un archivo **untracked** (nunca añadido al índice) devuelve
`fatal: not under version control, source=...` con exit code ≠0 — pero **ejecuta el rename
en disco igualmente** antes de fallar al intentar actualizar el índice de git.

Si asumes que el comando no hizo nada por el error y reintentas con `mv origen destino`,
falla con "No such file or directory" porque el origen ya no existe — el archivo está en
`destino`, no se perdió.

Fix: si `git mv` falla sobre un untracked, comprobar primero si el destino ya existe
(`ls destino`) antes de reintentar nada. Para archivos tracked, `git mv` SÍ falla limpio sin
efectos secundarios — el bug es específico de la rama untracked del comando.
