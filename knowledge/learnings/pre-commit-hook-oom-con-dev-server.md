---
title: pre-commit hook con build se queda sin memoria si hay dev server vivo
date: 2026-06-26
source: claude-code-session
tags: [git, claude-code, hooks]
---

Un hook `pre-commit` que corre `lint → typecheck → build` puede morir por OOM
(`Killed`, signal 9) si a la vez hay un `npm run dev` (Next/Turbopack) corriendo.
El hook captura el `Killed` y lo reporta como **"lint con errores"** → falso
positivo que manda a depurar lint inexistente.

Pistas de que es OOM y no lint real: el commit ya pasó lint limpio antes en la
sesión; el hook se corta siempre en el mismo paso pesado; mensaje genérico sin
fichero/línea.

Fix: matar el dev server antes de commitear — `lsof -ti:3000 | xargs kill` (+
cerrar navegadores headless de QA). Reintentar. Aplica a cualquier repo con hook
pesado + proceso de dev/build paralelo, no solo este.

Relacionado: [[actions-sin-billing-hooks-locales-unico-gate]].
