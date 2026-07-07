---
title: git worktree add sin cd inmediato — bash sigue en el cwd previo, no en el nuevo worktree
date: 2026-07-07
source: claude-code-session
tags: [claude-code, git, worktrees, gotchas]
---

Si borras un worktree (`git worktree remove --force`) mientras el cwd de Bash
apuntaba ahí, y luego creas uno NUEVO con `git worktree add <path> -b <rama>
origin/main` sin hacer `cd` explícito al nuevo path, los comandos Bash
siguientes NO fallan con "no such directory" — silenciosamente caen de vuelta
al **checkout principal del repo**, en la rama que sea que tuviera activa
(potencialmente de otra sesión paralela).

Consecuencia real: `npm run lint`/`typecheck` "limpios" eran falsos positivos
(comprobaban código sin mis cambios, que solo existían en el worktree vía
Edit/Write con rutas absolutas). `supabase migration list --linked` también
mintió sobre qué migraciones faltaban por aplicar.

Fix: tras CUALQUIER `git worktree add`, primer comando siempre `cd
<path-worktree> && pwd && git branch --show-current` para confirmar antes de
correr nada más. No asumir que el cwd sigue al `git worktree add`.
