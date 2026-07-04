---
title: gh pr merge puede "decir" merged sin fusionar — verifica state=MERGED, no el stdout
date: 2026-07-05
source: claude-code-session
tags: [github, gh-cli, gotcha]
---
`gh pr merge <n>` sobre un PR bloqueado (branch protection: review requerido o checks sin correr) NO fusiona: habilita auto-merge o falla, y su salida contiene la palabra "merged" ("Pull request will be automatically merged when requirements are met") → un `grep merged` da FALSO POSITIVO. Creí haber mergeado 12 PRs y `main` seguía intacto.
Verifica SIEMPRE el resultado real: `gh pr view <n> --json state -q .state` == "MERGED" (o `mergedAt != null`), nunca el texto del comando.
Con Actions caído + review requerido, el único merge posible es `gh pr merge <n> --admin --merge --delete-branch` (requiere admin). Antes de mergear: build agregado local verde de todo lo combinado; después: `git ls-remote origin refs/heads/main` cambió de SHA + build sobre el main real.
