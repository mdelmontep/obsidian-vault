---
title: conflicto de rebase en un JSON generado (baseline/lockfile-like) se resuelve regenerando, nunca a mano
date: 2026-07-16
source: claude-code-session
tags: [git, rebase, ci, baseline]
---
Un fichero JSON que es SALIDA de un script (`.inline-style-baseline.json`,
`.design-debt-baseline.json`, cualquier trinquete/ratchet con `--write`) entra
en conflicto de rebase cuando 2 ramas paralelas lo tocan (cada una bajó un
contador distinto). NO edites el diff a mano — ese fichero no tiene semántica
propia, es un snapshot derivado del código. Resuelve: `git checkout --ours
<archivo>` (o `--theirs`, da igual, es temporal) para desbloquear el rebase,
`git rebase --continue`, y LUEGO corre el script generador (`npm run
ratchet:update` / `ratchet:design:update`) sobre el estado ya rebaseado +
`git commit --amend`. Mismo principio que un `package-lock.json` en conflicto:
resolver con el generador, no con merge manual de líneas JSON.

Al regenerar DENTRO de un merge, comprueba que `MERGE_HEAD` es el `origin/main` de
AHORA: en un repo con varias sesiones mergeando PRs, el `fetch` de hace 10 min ya
está viejo y el derivado sale mutilado (grafo de dependencias regenerado que PERDÍA
16 nodos que sí estaban en main, 30-jul). No se nota sin diffear contra
`git show origin/main:<archivo>` — ningún trinquete se queja de nodos AUSENTES.
Salida: `git merge --abort`, `fetch`, mergear el main actual y regenerar entonces.

Relacionado: si el script usa `git ls-files` para listar qué contar, un
`.module.css` NUEVO no aparece hasta que esté en el índice — `git add -A`
antes de correr el ratchet o el conteo sale falso (por defecto, no por bug).
