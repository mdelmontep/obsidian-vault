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
