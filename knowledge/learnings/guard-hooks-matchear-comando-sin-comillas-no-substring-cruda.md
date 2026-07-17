---
title: hooks-guard de comandos — matchea sobre el comando SIN comillas, no substring cruda (falso positivo en --body/-m)
date: 2026-07-14
source: claude-code-session
tags: [claude-code, hooks, git, seguridad]
---
Un PreToolUse(Bash) que bloquea comandos peligrosos (git-guard: `reset --hard`, `push --force`, commit en main…) NO debe matchear por **substring sobre todo el comando**: un comando benigno cuyo *texto de argumento* menciona la frase da FALSO POSITIVO. Casos reales que se bloquearon solos: `gh pr create --body "… reset --hard …"` y `git commit -m "… push --force …"` (¡y me bloqueó mi propio `gh pr create` describiendo el fix!).

Fix: antes de matchear, **quita el contenido entre comillas** (un git peligroso real nunca va entre comillas):
```sh
scrubbed=$(printf '%s' "$cmd" | sed -e 's/"[^"]*"//g' -e "s/'[^']*'//g")
```
y corre TODOS los greps/case sobre `$scrubbed`. Solo hace el guard MÁS permisivo (ignora texto de args), nunca más débil ante un peligro real (que va sin comillas). Verifícalo con: FP entre comillas pasa · peligro real bloquea · `--force-with-lease` pasa.

Ojo: hay dos hooks con este patrón — el del repo (`.claude/hooks/`) y el global (`~/.claude/hooks/`); arregla LOS DOS. Ver [[subagente-feature-sin-cablear-composicion]] (verificar el efecto real, no solo el código).

Corolario (2026-07-17, hook que ENRUTA en vez de bloquear, [[fia-gate]]): para decidir "esto es un build de verdad" y no una mención en `git commit -m "…build…"` / `grep` / `echo`, quitar comillas se queda corto. Ancla a POSICIÓN de comando: trocea por `&&`/`||`/`;`/`|`/`&`, quita asignaciones de entorno del inicio (`FOO=bar `) y exige que el segmento EMPIECE por el objetivo (`^npm run build`). Así `cd x && npm run build` sí matchea y `echo "npm run build"` no.
