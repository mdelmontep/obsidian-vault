---
title: hook merge-guard — bloquear gh pr merge si la punta remota no es HEAD
date: 2026-08-12
source: claude-code-session
tags: [claude-code, hooks, git]
---

Idea sin profundizar: la regla nueva de CLAUDE.md («antes de `gh pr merge`, `ls-remote` ==
HEAD») es regla dura escrita en prosa → candidata a hook PreToolUse Bash (matchear `gh pr
merge`, resolver la rama del PR, comparar `git ls-remote origin refs/heads/<rama>` contra
`git rev-parse <rama>` local; bloquear con mensaje si divergen o si hay commits locales sin
push). Caso real que lo motiva: #1662 (facturaia, 12-ago), squash con 1 de 4 commits.
Suite en `~/.claude/hooks/tests/` como el resto. Ver
[[push-por-pipe-oculta-el-abort-del-pre-push-y-el-merge-squashea-punta-vieja]].
