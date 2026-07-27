---
title: un subagente reporta "hecho, todo verde" código que no compila o que no está
date: 2026-07-27
source: claude-code-session
tags: [agentes-paralelos, verificacion, code-review]
---
Dos casos reales en la misma sesión (agh-iberica, 7 frentes en paralelo):

1. Fix reportado como aplicado que **no compilaba**: declaraba la dependencia nueva e importaba 4 símbolos, pero dejó la función objetivo **byte a byte igual** → imports sin usar (lint rojo) y un símbolo importado que **no estaba exportado** en su origen (typecheck rojo).
2. Informe con «15 passed» de un fix **que no existía en ningún worktree** (`grep` del símbolo → 0). Lo que se commiteó bajo su mensaje era trabajo de otra sesión ([[stash-es-compartido-entre-worktrees-y-rompe-sesiones-paralelas]]).

**Checklist tras CADA subagente, antes de dar por bueno nada:**
- `git show --stat HEAD` → ¿los ficheros son los suyos y solo los suyos?
- `grep -c <símbolo nuevo>` en el fichero que dice haber tocado → ¿existe de verdad?
- Rojo-primero **repetido por ti**: `git checkout origin/main -- <src>`, correr el test, restaurar. Si no se pone rojo, el test no prueba el fix.
- Gate completo tú mismo. El informe del agente no es evidencia; el diff ejecutado sí.

Corolario de reparto: el trabajo del agente no es «el fix», es «el fix + la prueba de que el fix hace falta». Sin lo segundo, es una hipótesis con formato de entrega.
