---
title: con Actions caído (billing), los git hooks locales son el único gate de lint/build en facturaia
date: 2026-06-25
source: claude-code-session
tags: [facturaia, ci, git-hooks, eslint, deploy]
---

El CI de GitHub Actions de facturaia está caído por billing → no corre lint/typecheck/build
en los PRs. Los hooks de `.githooks` (pre-commit: trinquete + lint + typecheck; pre-push: build)
son la ÚNICA red. Si un merge usa `--no-verify`, cuela lint/build roto a `main` sin que nadie
se entere.

Caso real (jun 2026): la feature SEPA devoluciones coló a `main` un `react-hooks/set-state-in-effect`
(eslint-plugin-react-hooks@7.1.1) en `facturas-view.tsx` → `npm run lint` global en rojo; lo
arrastraron varios PRs con `--no-verify` hasta el fix #482. Confirmado que NO era skew: el
`package-lock` fijaba la 7.1.1 exacta.

Reglas mientras Actions siga sin billing:
- `npm run lint` global en local antes de cualquier merge a main. NO `--no-verify` salvo
  emergencia documentada; si el hook falla por algo ajeno a tu diff, arréglalo en su propio PR primero.
- Para que el pre-push (build) pase en un worktree hay que usar node_modules REAL (`npm ci`),
  no symlink. Ver [[turbopack-rechaza-symlink-node-modules-en-worktree]].
