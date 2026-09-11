---
title: llevar a un PR el WIP de una rama ya squash-mergeada
date: 2026-09-11
source: claude-code-session agency-portal
tags: [git, worktrees, pr, squash]
---
«Todas las ramas están en main» **no** es «no falta nada»: comparar ramas es ciego al
trabajo sin commitear. Hoy `git diff --stat origin/main origin/feat/pizarra-agenda`
salió **vacío** (tres PRs squasheados esa mañana) y lo único pendiente de verdad —847
líneas, un día de trabajo— seguía sin commitear en el worktree. Lo encuentra:
`git worktree list --porcelain | awk '/^worktree /{print $2}' | while read w; do git -C "$w" status --porcelain | grep -E '<dominio>'; done`

Y para llevarlo a un PR **no se commitea sobre la punta vieja de su rama**: su
merge-base con `main` es anterior al squash, así que el PR volvería a mostrar los tres
PRs ya mergeados (70 ficheros en vez de 11). Se planta el WIP sobre main:

    git diff --stat <punta-vieja> origin/main -- <ficheros tocados>  # vacío = main no los tocó
    git checkout -b <nueva> origin/main                              # arrastra el WIP intacto

El `checkout` solo arrastra los cambios si esos ficheros son **idénticos** entre las dos
bases: el diff vacío es la precondición, no una cortesía.
Ver [[rescatar-el-wip-de-un-worktree-sin-commitear-ni-tocar-el-stash-compartido]] ·
[[tres-puntos-y-git-cherry-mienten-en-ramas-squash-mergeadas]]
