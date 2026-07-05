---
title: next build lock huérfano hace fallar el pre-push hook con mensaje engañoso
date: 2026-07-02
source: claude-code-session
tags: [git, nextjs, hooks, gotcha]
---

Un `git push` con hook que corre `npm run build` puede fallar con
"build con errores" / `tsc` quejándose de archivos `.next/dev/types/*.ts`
inexistentes — parece typecheck roto, pero es un **lock huérfano**: un
`next build` anterior (de un push cortado, ej. por timeout) sigue vivo en
background y `.next/lock` bloquea el build nuevo a medias, dejando el
`.next/dev` en estado inconsistente.

Diagnóstico: `ps aux | grep "next build"` — si aparece un proceso corriendo
y `.next/lock` existe, es esto, no un error de código.

Fix: **esperar a que el proceso termine solo** (nunca matarlo a ciegas si el
repo es compartido con otra sesión — podría ser su build, no el tuyo) +
`rm .next/lock` + reintentar el push.

Si YA lo mataste a media escritura, `.next` queda **corrupto** → el siguiente
build peta con `ENOENT .../_ssgManifest.js` (y `rm -rf .next` da "Directory not
empty" si aún se escribe). Fix: matar los procesos, `rm -rf .next`, rebuild limpio.

Tree en disputa (otra sesión te cambió la rama,
[[git-head-compartido-entre-sesiones-paralelas-sin-worktree]]): empuja tu rama por
su ref (`git push origin <rama>`, no toca HEAD).

Caché `.next` FRÍA en worktree recién creado: el `next build` del pre-push puede
tardar >9min (compilación + fase TypeScript + page-data, agravado si un
`package-lock.json` huérfano en el HOME confunde el workspace-root de Next y
escanea de más). Ya NO vale `--no-verify` (el classifier de auto-mode lo bloquea
salvo emergencia documentada). Fix: **calienta la caché** (corre `next build` una
vez hasta poblar `.next`) y luego lanza el `git push` en **background** (no atado
al timeout de foreground); el build re-usa la caché caliente y completa.

Relacionado: [[pre-commit-hook-oom-con-dev-server]].
