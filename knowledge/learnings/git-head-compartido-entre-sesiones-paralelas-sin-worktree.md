---
title: sin worktree por sesión, un checkout ajeno desvía tu próximo commit a su rama
date: 2026-07-02
source: claude-code-session
tags: [git, claude-code, workflow, gotcha]
---

Dos sesiones de Claude Code trabajando en el mismo repo sin `git worktree add`
comparten el mismo `.git`/HEAD físico. Si la otra sesión ejecuta
`git checkout -b <su-rama>` justo mientras tu HEAD está en tu rama, el HEAD
compartido cambia bajo tus pies — tu próximo `commit` aterriza en SU rama,
no en la tuya, sin ningún error visible.

Señal de alarma: `git branch --show-current` devuelve un nombre que no
reconoces justo después de un commit tuyo.

Fix sin dañar el trabajo ajeno: `git cherry-pick <tu-commit>` a tu rama
correcta, luego `git branch -f <rama-ajena> <commit-anterior-a-tu-cherry-pick>`
para devolver su puntero a donde estaba. Nunca `reset --hard` ni tocar su
working tree — solo el puntero de rama.

Corolario: **antes de "dejar el tree limpio en main"**, `git status` + `git branch
--show-current`. Si hay WIP sin commitear que NO es tuyo (rama de feature ajena, no
pusheada, ficheros con timestamp reciente), es una sesión viva — NO hagas
`checkout`/`stash -u` a ciegas (le borras los ficheros del disco). Déjalo y usa un
worktree propio desde `origin/main`.

**Y comprobarlo «antes del commit» llega tarde** (25-ago-2026, facturaia): la otra sesión
se llevó el checkout a `fix/tickets-soporte-25ago` mientras yo llevaba 20 minutos editando
ficheros en `main`. Lo vi de casualidad, al leer un `git status` que había pedido para otra
cosa. Había además un `UU .file-size-baseline.json` a medio resolver: un `npm run gate` ahí
habría medido un árbol en conflicto ajeno y su rojo o su verde no habrían significado nada.
Lo barato es mirar `git branch --show-current` **al empezar cada tanda de ediciones**, no solo
al ir a commitear; y ante WIP ajeno, sacar lo tuyo (untracked se copia y se borra) y seguir en
`git worktree add ~/wt-<tema> -b <rama> origin/main`.

Relacionado: [[merge-tree-precheck-cross-pr-y-squash-branch-cleanup]].
