---
title: rules de proyecto (.claude/rules) no se comparten si .claude está gitignored
date: 2026-07-15
source: claude-code-session
tags: [claude-code, git, gobernanza, facturaia]
---

Al mover un inviolable de `CLAUDE.md` a un rule condicional (`<repo>/.claude/rules/x.md` con `paths:`), verifica ANTES `git check-ignore .claude/rules/x.md`. Muchos repos meten `.claude/` entero en `.gitignore` (para `settings.local.json`, `worktrees/`, etc.) → el rule NO se trackea, y el `CLAUDE.md` queda apuntando a un archivo que no existe en clones/CI/compañeros = **inviolable perdido en silencio** (caso FacturaIA 2026-07-15).

Vías:
- Compartir rules con el equipo → des-ignora solo la subcarpeta: `.claude/*` + `!.claude/rules/` (no basta `!.claude/rules/` con `.claude/` entero ignorado). Decisión de equipo (afecta a todos).
- Solo tu máquina → `~/.claude/rules/` (user-level, no versionado, no llega a compañeros).

Además (verificado en docs oficiales, `memory.md`): un rule con `paths:` que no casa en la sesión **no aparece** → mueve solo reglas file-scoped y de bajo riesgo (cosméticas). NUNCA inviolables transversales/de integridad (auth, filtros de query, series documentales): si un día no tocas ese path, desaparecen. Ver [[gate-agentico-que-no-dispara-suele-estar-inanido-no-mal-calibrado]] (mismo espíritu: lo condicional que no dispara pasa desapercibido).

Aplica igual a TODO el andamiaje, no solo rules: FacturaIA #1009 (2026-07-19) versionó `settings.json` + `commands/` + `agents/` + `hooks/` con el mismo split (`.claude/*` + `!` selectivo), dejando `settings.local.json`/`skills/`/`worktrees/` ignorados. **NUNCA pegar secretos en el allowlist de `settings.local.json`**: queda en disco en claro (había un `PGPASSWORD` y un JWT de n8n). El allowlist genérico va en `settings.json` versionado.

**Medido el 20-ago-2026, y refuerza el aviso de arriba con un mecanismo:** un `paths:` dispara cuando el modelo lee el fichero **con la herramienta `Read`**, y **NO cuando accede por Bash** (`cat`, `sed`, `grep`, `wc`). Verificado poniendo una marca única dentro del rule y buscándola en el transcript: `Read src/app.ts` la mete en contexto; `sed -n 1p src/app.ts` sobre el MISMO fichero, no. Con el ratio real de esta casa —Bash:Read **14:1**, y Bash como primera herramienta en 58 de 105 sesiones— la regla **llega tarde**: el 93 % de las sesiones de un repo usan `Read` alguna vez, el 7 % ninguna. Criterio: al `CLAUDE.md` lo que hay que saber **antes** de abrir nada; al rule el porqué que se consulta **mientras** se trabaja. Y nunca un `paths:` para algo que se ejecuta **sin tocar ficheros** (mergear una PR apilada, desplegar, renumerar una migración justo antes del merge). Ver [[donde-se-va-el-coste-de-claude-code-no-es-el-claude-md]].
