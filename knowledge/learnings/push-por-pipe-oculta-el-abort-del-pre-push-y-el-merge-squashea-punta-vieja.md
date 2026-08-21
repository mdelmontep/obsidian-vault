---
title: un push por pipe devuelve el exit del pipe y gh pr merge squashea la punta vieja
date: 2026-08-12
source: claude-code-session
tags: [git, github, harness, gates]
---
`git push … | tail -3` devuelve el exit de `tail`, no del push: si el pre-push aborta
(gate del grafo, build, migraciones), el comando "termina bien", el background lo reporta
como éxito y la rama remota se queda en una punta vieja. `gh pr merge --squash` no avisa:
squashea lo que el remoto tenga, y main queda sin los commits de arreglos (y con los gates
que esos commits cerraban, en rojo).

Fix en dos capas:
1. Nunca encadenar un push a un pipe. Si hay que recortar salida: `git push …; echo EXIT=$?`.
2. Antes de `gh pr merge`, SIEMPRE: `git ls-remote origin refs/heads/<rama>` == `git rev-parse HEAD`.

Caso real (12-ago, facturaia #1662): 2 pushes abortados por el gate del grafo de deps
(módulo nuevo → grafo desfasado), squash con 1 de 4 commits, `perimetro.test.ts` en rojo
en main ~20 min, recuperación en #1664.

Variante sin pipe (21-ago, facturaia): el push corrió en segundo plano y el
ENVOLTORIO reportó su propio exit 0 mientras el pre-push abortaba por el grafo de
dependencias desfasado. Nada mentía: el envoltorio terminó bien. Lo que no subió
fue la rama. Por eso el punto 2 no es «además», es lo único que no depende de
quién te cuente el resultado: **compara la punta remota con la local**, siempre.
